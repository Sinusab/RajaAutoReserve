from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Configurable settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
COOKIES_PATH = os.getenv("COOKIES_PATH", "raja_cookies.json")

# Search params
ADULT = os.getenv("ADULT", "1")
CHILD = os.getenv("CHILD", "0")
INFANT = os.getenv("INFANT", "0")
MOVE_TYPE = os.getenv("MOVE_TYPE", "1")
IS_CHARTER = os.getenv("IS_CHARTER", "false")
FROM_STATION = os.getenv("FROM_STATION", "191")
TO_STATION = os.getenv("TO_STATION", "1")
GO_DATE = os.getenv("GO_DATE", "14040119")
TICKET_TYPE = os.getenv("TICKET_TYPE", "Family")
RETURN_DATE = os.getenv("RETURN_DATE", "")
NUM_PASSENGER = os.getenv("NUM_PASSENGER", "1")
MODE = os.getenv("MODE", "Train")
DESC_TRAVEL = os.getenv("DESC_TRAVEL", "%D9%82%D8%B7%D8%A7%D8%B1%20%D9%85%D8%B4%D9%87%D8%AF%20%D8%A8%D9%87%20%D8%AA%D9%87%D8%B1%D8%A7%D9%86")

# Filtering settings
MAX_PRICE = int(os.getenv("MAX_PRICE", "10000000"))
BLACKLIST_KEYWORDS = [
    k.strip() for k in os.getenv("BLACKLIST_KEYWORDS", "اتوبوسی,سالنی").split(",") if k.strip()
]

def log(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp} UTC] {message}")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram not configured. Skipping notification.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        log(f"Failed to send Telegram message: {e}")

def build_search_url():
    return (
        "https://www.raja.ir/search"
        f"?adult={ADULT}&child={CHILD}&infant={INFANT}"
        f"&movetype={MOVE_TYPE}&ischarter={IS_CHARTER}"
        f"&fs={FROM_STATION}&ts={TO_STATION}&godate={GO_DATE}"
        f"&tickettype={TICKET_TYPE}&returndate={RETURN_DATE}"
        f"&numberpassenger={NUM_PASSENGER}&mode={MODE}&desctravel={DESC_TRAVEL}"
    )

# Setup Chrome with Selenium Manager (no explicit chromedriver path)
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")

try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    log(f"Failed to start Chrome: {e}")
    raise

# Load cookies if provided
driver.get("https://www.raja.ir")
if os.path.exists(COOKIES_PATH):
    try:
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Selenium requires domain/path fields to be present appropriately
                driver.add_cookie(cookie)
        log("Cookies loaded from file and applied")
        driver.refresh()
        log(f"Main page refreshed with cookies: {driver.current_url}")
    except Exception as e:
        log(f"Failed to load/apply cookies: {e}")
else:
    log("No cookies file found. Continuing without cookies.")

SEARCH_URL = build_search_url()
log(f"Search URL: {SEARCH_URL}")

# Loop to check for tickets
while True:
    driver.get(SEARCH_URL)
    log(f"Search link refreshed: {driver.current_url}")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "train-result"))
        )
        log("Results page loaded")
    except TimeoutException as e:
        log(f"Error loading results: {e}")
        driver.refresh()
        sleep(5)
        continue

    try:
        train_results = driver.find_elements(By.CLASS_NAME, "train-result")
        log(f"Number of trains found: {len(train_results)}")
        for result in train_results:
            try:
                train_name = result.find_element(By.CLASS_NAME, "train-name").text
            except Exception:
                train_name = ""
            try:
                wagon_type = result.find_element(By.CLASS_NAME, "wagon-type").text
            except Exception:
                wagon_type = ""
            log(f"Train name: {train_name}, Wagon type: {wagon_type}")

            is_blacklisted = any(
                kw and (kw in train_name or kw in wagon_type) for kw in BLACKLIST_KEYWORDS
            )
            if is_blacklisted:
                log(f"Skipped due to blacklist: {train_name} / {wagon_type}")
                continue

            try:
                capacity = result.find_element(By.CLASS_NAME, "field-value").text
            except Exception:
                capacity = ""
            log(f"Capacity: {capacity}")

            if "تمام شد" in capacity or "0" == capacity.strip():
                log(f"No capacity for {train_name}")
                continue

            try:
                price_element = result.find_element(By.CLASS_NAME, "price")
                price_text = price_element.text.replace(",", "").strip()
                price = int("".join(ch for ch in price_text if ch.isdigit()))
            except Exception:
                price = MAX_PRICE
            log(f"Price: {price} Rials")

            if price > MAX_PRICE:
                log(f"Price exceeds limit for {train_name}: {price} > {MAX_PRICE}")
                continue

            try:
                reserve_button = WebDriverWait(result, 8).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "lock-btn"))
                )
                reserve_button.click()
                log(f"Reserve clicked: {train_name}")

                continue_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-block"))
                )
                continue_button.click()
                log("Continue purchase clicked")

                purchase_link = driver.current_url
                message = (
                    "Ticket found!\n"
                    f"Train: {train_name}\n"
                    f"Price: {price} Rials\n"
                    f"Purchase link: {purchase_link}"
                )
                send_telegram_message(message)
                log("Notification sent. Exiting...")
                driver.quit()
                raise SystemExit(0)
            except Exception as e:
                log(f"Error reserving train {train_name}: {e}")

        delay = 3 + random.uniform(0, 3)
        log(f"No suitable tickets found. Refreshing in {delay:.1f} seconds...")
        sleep(delay)
    except Exception as e:
        log(f"Error finding trains: {e}")
        driver.refresh()
        sleep(5)

driver.quit()
