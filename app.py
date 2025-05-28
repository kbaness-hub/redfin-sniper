import os
import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load environment variables
load_dotenv()

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TO_PHONE = os.getenv("TO_PHONE")

# Email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Keywords and cities
KEYWORDS = ["duplex", "in-law", "fixer"]
CITIES = [
    "https://www.redfin.com/city/29470/IL/Chicago",
    "https://www.redfin.com/city/29920/IL/Oak-Brook",
    "https://www.redfin.com/city/10471/IL/Lake-Forest",
]

# Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# CSV file for storing seen listings
CSV_FILE = "matches.csv"


def load_seen_links():
    try:
        with open(CSV_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()


def save_seen_links(links):
    with open(CSV_FILE, "a", newline="") as f:
        for link in links:
            f.write(link + "\n")


def get_driver():
    chrome_options = Options()
    # hrome_options.add_argument("--headless")  # older headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    # ensure full content fits
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


def scrape_redfin(city_url):
    city_name = city_url.split('/')[-1].replace('-', ' ')
    print(f"\n📍 Checking Redfin listings for: {city_name}...")

    matches = []
    driver = get_driver()
    try:
        driver.get(city_url)

        # Wait until listing cards appear or timeout after 15 seconds
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.HomeCardContainer"))
        )

        cards = driver.find_elements(By.CSS_SELECTOR, "div.HomeCardContainer")
        print(f"🔎 Found {len(cards)} listing cards in city: {city_name}")

        for card in cards:
            try:
                link_tag = card.find_element(By.TAG_NAME, "a")
                url = link_tag.get_attribute("href")
                text = card.text.lower()

                if any(keyword in text for keyword in KEYWORDS):
                    price = card.find_element(By.CSS_SELECTOR, ".homecardV2Price").text if card.find_elements(
                        By.CSS_SELECTOR, ".homecardV2Price") else "Price not found"
                    stats = card.find_element(By.CSS_SELECTOR, ".stats").text if card.find_elements(
                        By.CSS_SELECTOR, ".stats") else "Beds/Baths not found"
                    matches.append(
                        {"url": url, "price": price, "beds_baths": stats})
            except Exception:
                continue

    except Exception as e:
        print("❌ Error scraping city:", e)
    finally:
        driver.quit()

    return matches


def send_sms_alert(message_body: str) -> None:
    try:
        client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE,
            to=TO_PHONE
        )
        print("📱 Text alert sent!")
    except Exception as e:
        print("❌ SMS failed:", e)


def send_email_alert(matches: list) -> None:
    if not matches:
        return

    body_lines = []
    for match in matches:
        body_lines.append(f"{match.get('price', 'Price not found')} | "
                          f"{match.get('beds_baths', 'Beds/Baths not found')}\n"
                          f"{match['url']}\n")

    msg = EmailMessage()
    msg["Subject"] = "New Redfin Listings Match Found!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("\n".join(body_lines))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email alert sent!")
    except Exception as e:
        print("❌ Failed to send email alert:", e)


if __name__ == "__main__":
    print(f"🕒 Starting scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    seen_links = load_seen_links()
    new_links = []
    matches = []

    for city in CITIES:
        found = scrape_redfin(city)
        for match in found:
            if match["url"] not in seen_links:
                matches.append(match)
                new_links.append(match["url"])

    if matches:
        print(f"\n⚠️ Alert: 🏠 {len(matches)} Redfin match(es) found!")
        alert_message = f"New Redfin match(es):\n" + \
            "\n".join(match['url'] for match in matches)

        # SMS sending is disabled until Twilio number is fully verified
        # send_sms_alert(alert_message)

        send_email_alert(matches)
        save_seen_links(new_links)
        print(f"💾 Saved {len(new_links)} new match(es) to matches.csv")
    else:
        print("❌ No matches this time.")
