### Raja Ticket Auto-Reservation Bot

Python Selenium bot to search Raja trains and notify via Telegram when a matching ticket is found, with optional auto-advance to the purchase page.

### Quick start

- **Python**: 3.12
- **Chrome**: provided via `nixpacks.toml` or installed on host

1) Copy `.env.example` to `.env` and set values:

```bash
cp .env.example .env
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run:

```bash
python main.py
```

### Configuration (.env)

- **TELEGRAM_TOKEN**, **TELEGRAM_CHAT_ID**: optional, for notifications
- **COOKIES_PATH**: path to Raja cookies JSON (exported from browser)
- Search params: `ADULT`, `CHILD`, `INFANT`, `FROM_STATION`, `TO_STATION`, `GO_DATE`, etc.
- Filters: `MAX_PRICE`, `BLACKLIST_KEYWORDS`

### Cookies

Place exported cookies JSON at `raja_cookies.json` or update `COOKIES_PATH`. Bot runs without cookies if file is missing.

### Notes

- Uses Selenium Manager, no manual chromedriver path needed.
- Headless Chrome is enabled by default.
- Adds small random delay between polls to reduce bot detection.
