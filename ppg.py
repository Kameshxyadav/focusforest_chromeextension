import serial
import time
import numpy as np
import re
from scipy.signal import find_peaks, butter, filtfilt
from scipy.integrate import simpson

# ---------------- CONFIGURATION ----------------
COM_PORT = 'COM5'
BAUD_RATE = 115200
DURATION = 10  # seconds
OUTPUT_FILE = 'ppg_data_minmax.csv'
NORMALIZED_MIN = 500
NORMALIZED_MAX = 600
# ------------------------------------------------

# 🔧 Normalize using min-max
def min_max_normalize(value, min_val, max_val, new_min=NORMALIZED_MIN, new_max=NORMALIZED_MAX):
    if max_val == min_val:
        return new_min
    norm = (value - min_val) * (new_max - new_min) / (max_val - min_val) + new_min
    return max(new_min, min(new_max, norm))

# 👤 User input
age = input("Enter your age: ")
height = input("Enter your height (cm): ")
weight = input("Enter your weight (kg): ")

# 🔌 Connect to serial
print(f"Connecting to {COM_PORT} at {BAUD_RATE} baud...")
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(4)
ser.reset_input_buffer()

# 🧪 Collect data
print(f"Recording for {DURATION} seconds...")
start_time = time.time()
raw_data = []

while time.time() - start_time < DURATION:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        match = re.match(r"(\d+),(\d+)", line)
        if match:
            red = int(match.group(1))
            ir = int(match.group(2))
            raw_data.append((red, ir))

ser.close()
print(f"Collected {len(raw_data)} samples.")

if not raw_data:
    print("❌ No data collected. Check sensor or connection.")
    exit()

# 🔎 Separate RED and IR
red_values = [r for r, _ in raw_data]
ir_values = [i for _, i in raw_data]

# 🎚 Bandpass filter for IR signal
fs = 10  # Sampling frequency (Hz)
nyq = 0.5 * fs
low = 0.5 / nyq
high = 3.0 / nyq
b, a = butter(2, [low, high], btype='band')
filtered_ir = filtfilt(b, a, ir_values)

# ✅ Normalize raw IR (for storing) and filtered IR (for pulse analysis)
ir_min, ir_max = min(ir_values), max(ir_values)
norm_ir = [min_max_normalize(i, ir_min, ir_max) for i in ir_values]
mean_normalized_ir = np.mean(norm_ir)

filtered_min = min(filtered_ir)
filtered_max = max(filtered_ir)
norm_filtered_ir = [min_max_normalize(x, filtered_min, filtered_max) for x in filtered_ir]

# 🔍 Detect peaks
peaks, _ = find_peaks(norm_filtered_ir, distance=fs*0.5, prominence=5)
valleys, _ = find_peaks([-x for x in norm_filtered_ir], distance=fs*0.5, prominence=5)

# 🧠 Peak values
systolic_peak = np.mean([norm_filtered_ir[p] for p in peaks]) if peaks.size else np.nan
diastolic_peak = np.mean([norm_filtered_ir[v] for v in valleys]) if valleys.size else np.nan

# ❤ Heart rate
if len(peaks) > 1:
    intervals = np.diff(peaks) / fs
    heart_rates = 60 / intervals
    mean_heart_rate = np.mean(heart_rates)
else:
    mean_heart_rate = np.nan

# 🩸 Pulse area (area under 1 heartbeat)
if len(peaks) >= 2:
    areas = []
    for i in range(len(peaks) - 1):
        s, e = peaks[i], peaks[i+1]
        area = simpson(np.abs(norm_filtered_ir[s:e]), dx=1/fs)
        areas.append(area)
    pulse_area = np.mean(areas)
else:
    pulse_area = np.nan

# 📉 Mean DC component of IR (for reference)
dc_component = np.mean(ir_values)

# 🔁 Normalize RED too (just for CSV output)
red_min, red_max = min(red_values), max(red_values)
norm_red = [min_max_normalize(r, red_min, red_max) for r in red_values]

# 💾 Save to CSV
with open(OUTPUT_FILE, 'w') as f:
    f.write("Summary\n")
    f.write("Age,Height_cm,Weight_kg\n")
    f.write(f"{age},{height},{weight}\n\n")

    f.write("Heart_Rate_BPM,{}\n".format(round(mean_heart_rate, 2)))
    f.write("Systolic_Peak,{}\n".format(round(systolic_peak, 2)))
    f.write("Diastolic_Peak,{}\n".format(round(diastolic_peak, 2)))
    f.write("Mean_Normalized_PPG,{}\n".format(round(mean_normalized_ir, 2)))
    f.write("Pulse_Area,{}\n".format(round(pulse_area, 2)))
    f.write("DC_Component_Raw_IR,{}\n\n".format(round(dc_component, 2)))

    f.write("Data\n")
    f.write("Raw_RED,Raw_IR,Norm_RED,Norm_IR\n")
    for i in range(len(raw_data)):
        f.write(f"{red_values[i]},{ir_values[i]},{norm_red[i]},{norm_ir[i]}\n")

print(f"✅ Data saved to {OUTPUT_FILE}")