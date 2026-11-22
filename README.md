# University Admission Notification Bot

A simple Python bot that watches official Bangladeshi university admission
pages, asks Google Gemini whether online applications are currently open, and
sends a Telegram notification when a new application window opens.

It checks every 30 minutes by default and stores what it has already notified in
`notified.json`.

---

## What the bot does

1. Downloads the admission notice/portal pages listed in `universities.py`.
2. Follows nearby admission-related links (up to 5 pages per university).
3. Sends the page text and links to Gemini for strict extraction.
4. Notifies you on Telegram only when:
   - Gemini says the online application is **open**, and
   - the status is `open`, and
   - today is not before the start date, and
   - today is not after the deadline.
5. Skips announcements that were already notified.
6. Sends an **update** if a previously notified deadline or application link
   changes.
7. A new session (for example `2026-2027` instead of `2025-2026`) creates a new
   notification.

The bot does **not** use a database, dashboard, web framework, or scheduler
service.

---

## Project files

```text
admission-notification/
├── main.py
├── universities.py
├── .env
├── .env.example
├── requirements.txt
├── notified.json
├── README.md
├── .github/workflows/admission-check.yml
└── bot.log              # created automatically
```

- `universities.py` — the list of universities and official URLs.
- `notified.json` — previously notified admission windows.
- `bot.log` — rotating log file (created when the bot runs).
- `.env` — secrets. It is ignored by Git.

---

## Windows 10 setup

Open **PowerShell** and go to the project folder:

```powershell
cd D:\xampp\htdocs\admission-notification
```

### 1. Check Python

Python 3.10 or newer is required. Python 3.12 is recommended.

```powershell
python --version
```

If Python is not installed, install it from
<https://www.python.org/downloads/windows/> and tick **Add python.exe to PATH**
during installation.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

### 3. Install the packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Playwright is used for the GST admission portal, which blocks ordinary HTTP
requests.

---

## Create a Telegram bot with BotFather

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Give the bot a display name, for example `University Admission Alerts`.
4. Give it a username ending in `bot`, for example
   `my_admission_alerts_bot`.
5. BotFather replies with a token like:
   `123456789:AAExampleTokenDoNotShare`.
   Copy this into `TELEGRAM_BOT_TOKEN`.
6. Open your new bot's chat and press **Start** (or send `/start`). A bot cannot
   message you first unless you have started the chat.

Do not post the token publicly. Anyone with it can control the bot.

---

## Get your Telegram Chat ID

### Method 1 — built-in helper

After putting `TELEGRAM_BOT_TOKEN` in `.env`, run:

```powershell
.\.venv\Scripts\python.exe main.py --get-chat-id
```

The bot prints its `@username`, then waits up to 60 seconds for a message.
Open the exact bot whose username was printed, press **Start**, and the chat ID
appears in the terminal. Send a message in a group if you want that group's ID.

Note: a newly created bot does **not** reply to `/start` by itself. There is no
reply until the bot code is running, so use `getUpdates` or this helper instead
of waiting for an automatic reply.

### Method 2 — `getUpdates` (works for your personal account)

1. Send a message such as `hello` to your bot.
2. Open this URL in a browser, replacing `<TOKEN>` with your bot token:

   ```text
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

3. Find `"chat":{"id":123456789,...}` in the JSON. The number is your chat ID.
   For a personal chat it is a positive number.
4. Put it in `TELEGRAM_CHAT_ID`.

### Method 3 — use a helper bot

Send `/start` to **@userinfobot** on Telegram. It replies with your numeric ID.
Use that number as `TELEGRAM_CHAT_ID`.

For a group, add your bot to the group, send a message in the group, then use
`getUpdates`; the group chat ID is usually a negative number.

---

## Get a Gemini API key

1. Go to <https://aistudio.google.com/apikey>.
2. Sign in with a Google account.
3. Create an API key.
4. Put it in `GEMINI_API_KEY`.

The default model is `gemini-3.5-flash-lite`, which is inexpensive for this
kind of extraction task. You can change it in `.env` with `GEMINI_MODEL`.

---

## Fill in `.env`

Open `.env` in Notepad:

```powershell
notepad .env
```

Set the three required values:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Optional settings:

```dotenv
GEMINI_MODEL=gemini-3.5-flash-lite
CHECK_INTERVAL_MINUTES=30
REQUEST_TIMEOUT_SECONDS=25
MAX_PAGES_PER_UNIVERSITY=5
PLAYWRIGHT_FALLBACK=true
```

Save the file.

---

## Test the setup

### Test Telegram

```powershell
python main.py --test-telegram
```

You should receive `✅ Admission Bot connected!` in Telegram.

### Test one monitoring cycle without sending notifications

```powershell
python main.py --once --dry-run
```

This still uses Gemini, but it prints the notifications it *would* send and does
not modify `notified.json`. Use it to check the results first.

### Run one real check

```powershell
python main.py --once
```

A currently open admission window may be notified immediately on the first run.

### Start continuous monitoring

```powershell
python main.py
```

The bot checks immediately, then every 30 minutes. Stop it with `Ctrl+C`.

---

## Add or remove universities

Edit `universities.py`. Each entry uses this shape:

```python
{
    "id": "example",
    "name": "Example University",
    "urls": [
        "https://www.example-university.edu.bd/admission",
        "https://admission.example-university.edu.bd/",
    ],
    # "needs_javascript": True,  # only for JavaScript-heavy portals
},
```

Guidelines:

- Use the official admission notice page and/or the application portal.
- `id` must be unique and should stay stable; it is part of the saved keys.
- Add as many URLs as you need, but keep the list small.
- The bot follows admission-related links found on these pages, up to
  `MAX_PAGES_PER_UNIVERSITY`.
- Set `"needs_javascript": True` only if the site requires a browser to show
  its admission content. Playwright must be installed for this to take effect.
- Restart the bot after editing the file.

The included list covers exactly these seven sources:

1. Jahangirnagar University
2. Bangladesh University of Professionals (BUP)
3. University of Chittagong
4. University of Rajshahi
5. Khulna University
6. Comilla University
7. GST / Guccho Integrated Admission

Website addresses and page layouts can change, so verify the URLs occasionally.

---

## Playwright / JavaScript-rendered websites

Most pages work with `requests` + BeautifulSoup. The GST admission portal
requires a real browser, so Playwright and Chromium are required:

```powershell
pip install playwright
playwright install chromium
```

The code automatically falls back to Playwright when a page is blocked (for
example HTTP 403), has almost no text, or its university entry has
`"needs_javascript": True`. If Playwright is not installed, the bot logs a
message and continues with the other universities.

To disable the fallback completely:

```dotenv
PLAYWRIGHT_FALLBACK=false
```

---

## How duplicate prevention works

`notified.json` contains a record per university + session + programme:

```json
{
  "announcements": {
    "du|2026-2027|undergraduate": {
      "university": "University of Dhaka",
      "session": "2026-2027",
      "program": "Undergraduate",
      "status": "Application Started",
      "start_date": "2026-11-11",
      "deadline": "2026-11-25",
      "apply_url": "https://admission.eis.du.ac.bd/en",
      "notice_url": "https://www.du.ac.bd/du_post_details/notice/29148",
      "source_url": "https://www.du.ac.bd/notice",
      "first_notified_at": "2026-11-22T10:30:00+06:00",
      "last_notified_at": "2026-11-22T10:30:00+06:00"
    }
  }
}
```

- Same university/session/programme → no second notification.
- Deadline or application-link change → update notification.
- New session → new key → new notification.
- A failed Telegram send is **not** saved, so it is retried next cycle.

You can reset all notification history while the bot is stopped by replacing the
contents of `notified.json` with:

```json
{
  "announcements": {}
}
```

Do not delete `notified.json` while the bot is running.

---

## Logs and troubleshooting

The console and `bot.log` show each step. Common issues:

### `Missing configuration in .env`

Fill in all required values in `.env`. Make sure there are no spaces around the
`=` unless they are part of the value.

### Telegram returns `401 Unauthorized`

The bot token is wrong or was revoked. Create a new token with BotFather.

### Telegram returns `400 Bad Request: chat not found`

- You have not pressed **Start** in the bot's chat.
- The chat ID is wrong.
- For a group, add the bot to the group and get the negative group ID.

### `429` from Gemini

The API rate limit or quota was reached. The bot waits/retries, but repeated
`429` messages mean you should reduce the university list, use a key with more
quota, or increase `CHECK_INTERVAL_MINUTES`.

### Gemini returns a model `404` or "model not found"

The configured `GEMINI_MODEL` is not available to your API key. Open
<https://ai.google.dev/gemini-api/docs/models> and set `GEMINI_MODEL` in `.env`
to a currently available model.

### A university returns `403`, `404`, or no content

Many university sites block non-browser requests or change URLs. Make sure
Playwright and Chromium are installed, verify the URL in `universities.py`, or
remove that university. Errors for one source do not stop the others.

### No notification for an open admission

Check `bot.log` for:

- page-fetch errors,
- Gemini saying the status is `upcoming`, `closed`, or `unknown`,
- a date rejection because the deadline has passed,
- "Already notified".

The AI is deliberately conservative. Always verify the official notice.

### The bot only runs while the terminal is open

That is expected. Closing the terminal or pressing `Ctrl+C` stops the Python
process. To run it in the background on Windows, you can use Task Scheduler with
the action:

```text
Program:   D:\xampp\htdocs\admission-notification\.venv\Scripts\python.exe
Arguments: main.py
Start in:  D:\xampp\htdocs\admission-notification
```

Set it to **Run only when user is logged on** if you want to see the console.

---

## Option: run for free with GitHub Actions

The included workflow at `.github/workflows/admission-check.yml` checks the
universities every 30 minutes even when your PC is off.

### Setup

1. Create a GitHub repository and push this project to it:

   ```powershell
   cd D:\xampp\htdocs\admission-notification
   git init
   git add .
   git status --short
   git commit -m "Initial admission bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

   Check `git status --short` before committing: `.env`, `.venv`, and `bot.log`
   must not appear.

2. **Never commit `.env`.** It is already ignored by `.gitignore`.
3. In GitHub, open **Settings → Secrets and variables → Actions → New repository
   secret** and add:
   - `GEMINI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Open the **Actions** tab, select **University admission check**, and click
   **Run workflow** once to test it.
5. After a successful run, it will run from the schedule every 30 minutes.

The workflow:

- installs Python, the requirements, and Chromium,
- runs `python main.py --once`,
- commits `notified.json` back to the repository when it changes,
- uploads `bot.log` as a workflow artifact.

The state commit is why duplicate prevention still works across separate
Actions runs.

### Important limitations

- GitHub's schedule is **best-effort**. Runs may be delayed by several minutes
  during busy periods.
- The workflow needs **write permission** for repository contents. Branch
  protection rules can block the `notified.json` commit.
- Public repositories receive free standard-runner minutes. Private repositories
  have a monthly free-minute limit; Playwright makes each run take several
  minutes, so frequent checks can exhaust it.
- GitHub may disable scheduled workflows after 60 days of repository
  inactivity.
- Some university sites may block GitHub's cloud IP addresses. Check the
  workflow log if a site stops working.
- A small always-on VPS is still more reliable than Actions for 24/7 monitoring.

---

## Cost and reliability notes

- Every check uses one Gemini request per university whose pages are fetched.
  With 7 sources and a 30-minute interval, that is up to 336 requests per day.
  Adjust the list or interval if your API quota/cost is a concern.
- Gemini is called through its REST API using `requests`; no extra Gemini SDK is
  required.
- Gemini's answer is an extraction, not an official confirmation. Websites can
  be ambiguous, outdated, or blocked. Verify dates and links on the official
  university site before applying.
- If a university publishes dates only inside a PDF, the bot can see the PDF
  link but cannot read the PDF text. Add an HTML notice page for that university
  when possible.
- This bot only monitors pages you configure. It does not search the whole web.
- Keep the computer awake and connected for continuous monitoring.
- Respect each website's terms of use and do not lower the request interval to
  an abusive level.

---

## Quick command summary

```powershell
# One-time setup
cd D:\xampp\htdocs\admission-notification
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
notepad .env

# Verify
python main.py --get-chat-id
python main.py --test-telegram
python main.py --once --dry-run
python main.py --once

# Normal operation
python main.py
```
