# Redfin Real Estate Deal Sniper 🏠📬

This Python application scrapes Redfin for real estate listings in specified cities and alerts you via **email** (and optionally SMS) when a listing matches your desired keywords.

## 🚀 Features

- Scrapes Redfin for multiple cities
- Filters listings based on keywords like `duplex`, `in-law`, `fixer`
- Sends alerts by **email** with listing details and links
- Optional SMS alerts via Twilio (disabled by default)
- Avoids duplicate alerts by tracking previously seen listings
- Clean code and professional logging
- Follows PEP 8 and public-safe best practices

## 🔧 Requirements

- Python 3.7+
- Redfin website access
- Gmail account (for email alerts)
- Twilio account (optional for SMS alerts)

## 📦 Installation

1. **Clone the repo:**
```bash
git clone https://github.com/yourusername/redfin-sniper.git
cd redfin-sniper
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** in the root directory:
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
> ⚠️ For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your normal login.

4. **Run the script:**
```bash
python app.py
```

## 🛠 Configuration

### Keywords:
Change the `KEYWORDS` list in `app.py`:
```python
KEYWORDS = ["duplex", "in-law", "fixer"]
```

### Cities:
Edit the `CITIES` list with your desired Redfin city URLs:
```python
CITIES = [
    "https://www.redfin.com/city/29470/IL/Chicago",
    "https://www.redfin.com/city/29502/IL/Oak-Brook",
]
```

## 📧 Email Output Example
```
$450,000 | 3 Beds 2 Baths
https://www.redfin.com/IL/Chicago/123-Main-St/home/1234567
```

## 📱 Optional: Enable SMS
In `app.py`, uncomment this line:
```python
# send_sms_alert(alert_message)
```
Ensure your Twilio number is verified and supports SMS.

## 🧠 Future Ideas
- Deploy to cloud with daily or hourly checks
- Export listings to a CSV or Google Sheet
- Web dashboard with Flask or Streamlit

## 📁 Files
- `app.py` – main application
- `matches.csv` – log of all seen listings
- `.env` – secret credentials (ignored by Git)

## 🔐 Security Notes
- Never commit `.env` to GitHub
- `.gitignore` already excludes it
- Email and SMS credentials are securely loaded

## 🤝 License
This project is open-source and free for personal or educational use. Contributions welcome!
