# 🚆 RajaAutoReserve  
A fully automated **Raja.ir train ticket reservation watcher**, built using **Python**, **Selenium (Headless Chrome)**, and **Telegram Bot API**.

This bot continuously checks ticket availability for specific train routes and dates, filters out unwanted train types, evaluates ticket prices, and sends **real-time Telegram notifications** with the purchase link when eligible tickets become available.

---

## 🚀 Features

- Headless Chrome automation using Selenium  
- Smart page loading & auto-refresh  
- Cookie‑based login/session handling  
- Automatic train filtering (Bus/Salon wagons skipped)  
- Price threshold logic  
- Auto‑click reservation flow  
- Telegram notifications for detected tickets  
- Fully optimized for **Render**, **Railway**, and local execution  

---

## 📁 Project Structure

```
RajaAutoReserve/
│
├── main.py                # Core automation script
├── nixpacks.toml          # Deployment config for Render/Railway
├── raja_cookies.json      # Raja.ir session cookies (export manually)
└── requirements.txt       # Python dependencies
```

---

## 📦 Requirements

- Python 3.10+  
- Google Chrome (Headless)  
- Matching ChromeDriver version  
- Valid Raja.ir cookies  

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Set your Telegram bot credentials:

```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_target_chat_id
```

Linux/macOS:

```bash
export TELEGRAM_TOKEN=xxxx
export TELEGRAM_CHAT_ID=123456
```

Windows CMD:

```cmd
set TELEGRAM_TOKEN=xxxx
set TELEGRAM_CHAT_ID=123456
```

---

## 🍪 Raja.ir Session Cookies

The bot loads cookies from:

```
raja_cookies.json
```

To generate cookies:

1. Log in to **https://www.raja.ir**  
2. Open Developer Tools → Application → Cookies  
3. Export cookies as JSON  
4. Replace the contents of `raja_cookies.json`  

Cookies expire periodically; update them if login fails.

---

## ▶️ Running the Bot

Run locally:

```bash
python main.py
```

The bot will:

1. Load saved cookies  
2. Open the Raja.ir search URL  
3. Scrape available trains  
4. Apply filters (wagon type, capacity, price)  
5. Auto-select valid tickets  
6. Send Telegram alerts  
7. Exit after a successful detection  

---

## ☁️ Cloud Deployment (Render / Railway)

The project includes a `nixpacks.toml` that configures:

- Chrome installation  
- Selenium support  
- Python runtime  
- Headless mode stability  

This allows **single-click deploy** on Render or Railway.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  
Automating ticketing systems may violate terms of service.  
Use responsibly.

---

## 🤝 Contributing

Contributions, bug fixes, and improvements are welcome.  
Feel free to open issues or submit pull requests.

---

## 📝 License

MIT License.
