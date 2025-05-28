# Redfin Real Estate Deal Sniper

This Python application scrapes Redfin in real-time using Selenium to detect keyword-matching property listings and sends alerts via **email** (optionally SMS via Twilio). It’s designed to run locally or be cloud-deployable, and is fully safe to publish.

## Features

- Real-time scraping of JavaScript-rendered Redfin pages with **Selenium**
- Supports multiple cities
- Filters listings by keywords like `duplex`, `in-law`, `fixer`
- Sends **email alerts** using Gmail SMTP
- (Optional) Sends **SMS alerts** via Twilio
- Dedupes alerts using CSV
- Works on Windows using ChromeDriver
- Safe for GitHub – no secrets committed

## Requirements

- Python 3.7+
- Google Chrome (installed)
- ChromeDriver (matching version)

## Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/redfin-sniper.git
cd redfin-sniper
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up ChromeDriver
1. Visit https://googlechromelabs.github.io/chrome-for-testing/
2. Match your Chrome version (e.g. 137.x)
3. Download the `chromedriver-win64.zip`
4. Extract and place `chromedriver.exe` in the same folder as `app.py`

## Environment Variables

Create a `.env` file:
```
# Email Credentials
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TO_EMAIL=recipient_email@gmail.com

# Twilio Credentials (Optional)
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE=+1XXXXXXXXXX
TO_PHONE=+1YYYYYYYYYY
```
> Use an [App Password](https://myaccount.google.com/apppasswords) for Gmail

`.gitignore` already excludes `.env`

## Run the Scraper
```bash
python app.py
```
> You’ll see Chrome open each listing page as it searches for matches

## Customization

### Cities
Edit the `CITIES` list in `app.py`:
```python
CITIES = [
    "https://www.redfin.com/city/29470/IL/Chicago",
    "https://www.redfin.com/city/29920/IL/Oak-Brook",
    "https://www.redfin.com/city/10471/IL/Lake-Forest",
]
```

### Keywords
Update the `KEYWORDS` list:
```python
KEYWORDS = ["duplex", "in-law", "fixer"]
```

## Email Example Output
```
$450,000 | 3 Beds 2 Baths
https://www.redfin.com/IL/Chicago/123-Main-St/home/1234567
```

## SMS Alerts (Optional)
In `app.py`, uncomment:
```python
# send_sms_alert(alert_message)
```

## Future Ideas
- Deploy to cloud (PythonAnywhere, Render)
- Add logging + analytics
- GUI dashboard with Flask or Streamlit

## Files
- `app.py` – main application
- `.env` – credentials (excluded from git)
- `chromedriver.exe` – Chrome headless driver
- `matches.csv` – stores already-seen listings

## Portfolio Highlight
> Built a real estate intelligence tool using Python, Selenium, and email/SMS integrations to detect and deliver real-time listing opportunities from Redfin.

## License
This project is licensed under the [MIT License](LICENSE).

## Questions?
Feel free to fork this repo, suggest improvements, or reach out via [banesskate@gmail.com].
