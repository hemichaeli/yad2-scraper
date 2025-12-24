# config.py - הגדרות המעקב
# נוצר אוטומטית על ידי YAD2 Scraper UI

import os

# מילות חיפוש
SEARCH_TERMS = [
    "glock 45 mos",
    "גלוק 45 מוס",
    "גלוק 45 מ.ו.ס",
    "glock45 mos",
    "גלוק45 מוס",
    "glock 45mos",
    "45 mos",
    "45 מוס",
    "מילה לחיפוש",
]

# הגדרות Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# הגדרות Email
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "")

# הגדרות SMTP
EMAIL_SERVER_TYPE = os.environ.get("EMAIL_SERVER_TYPE", "custom")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "true").lower() == "true"

# הגדרות כלליות
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30
SEEN_ITEMS_FILE = "seen_items.json"
NOTIFY_ON_NO_RESULTS = False
