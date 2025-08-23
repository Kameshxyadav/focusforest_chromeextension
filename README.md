# Focus Forest — Chrome MV3

A small extension that helps you focus. Start a session and a right-edge timer bubble appears on every tab. During focus, listed sites are blocked. If you visit one, the session ends. Optional Pomodoro and gentle reminders to hydrate and stretch.

## What it does

* Right-edge timer bubble that appears instantly and stays across tabs
* Start fixed-length sessions or Pomodoro (25/5 × 4 with 15-min long break)
* Domain blocking during focus (subdomains included)
* Health reminders every \~45 minutes
* Lightweight session history
* All data is stored locally

## Install (Developer Mode)

1. Clone or download this repository.
2. Open `chrome://extensions`, enable **Developer mode**.
3. Click **Load unpacked** and select the repo folder.
4. Click the extension icon and start a session.

> The bubble won’t show on restricted pages like `chrome://*`, the Chrome Web Store, the built-in PDF viewer, or some `file://` pages. Open any normal site to test.

## Usage

* Open the popup, choose a duration or enable Pomodoro, then start.
* The bubble shows the countdown on the right. Click it to reopen the popup.
* “Give Up” ends the session immediately.
* Opening a blocked site ends the session.

## Blocked sites

Open **Options** and list one domain per line (no protocol):

```
youtube.com
instagram.com
reddit.com
x.com
```

End and restart a session after editing this list so new rules apply.

## Project structure

```
manifest.json                # MV3 manifest
background.js                # session engine, blocking, alarms, notifications
bubble.js                    # right-edge timer bubble (content script)
popup.html / popup.css / popup.js
options.html / options.css / options.js
blocked.html                 # redirect page for blocked domains
icon16.png / icon32.png / icon48.png / icon128.png
```

No analytics. No network calls. Everything stays in your browser.

## Roadmap

* Stats dashboard and streaks
* Custom reminder intervals and sounds
* Export history (CSV)

## Contributing

Issues and pull requests are welcome. Keep changes focused and include reproduction steps if you’re fixing a bug.

