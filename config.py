# config.py - הגדרות המעקב
# ============================================
# קובץ זה מכיל את כל ההגדרות של הסורק.
# שנה את מילות החיפוש למוצר שאתה מחפש.
# ============================================

import os

# ==========================================
# 🔍 מילות חיפוש
# ==========================================
# הסורק יחפש כל אחת מהמילים האלה באתרים.
# הוסף או הסר מילים לפי הצורך.
# 
# דוגמאות לחיפושים שונים:
# - נשק: "glock 45 mos", "גלוק 19", "sig sauer"
# - רכב: "מאזדה 3", "טויוטה קורולה"
# - אלקטרוניקה: "iphone 15", "macbook pro"
# - ריהוט: "ספה פינתית", "שולחן אוכל"
# ==========================================

SEARCH_TERMS = [
    # חיפוש נוכחי: Glock 45 MOS
    "glock 45 mos",
    "גלוק 45 מוס",
    "גלוק 45 מ.ו.ס",
    "glock45 mos",
    "גלוק45 מוס",
    "glock 45mos",
    "45 mos",
    "45 מוס",
    
    # הוסף מילות חיפוש נוספות כאן:
    # "מילה לחיפוש",
]

# ==========================================
# 📱 הגדרות Telegram
# ==========================================
# הערכים נלקחים מ-GitHub Secrets או משתני סביבה.
# אין לכתוב את הערכים האמיתיים כאן!
# ==========================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ==========================================
# 📧 הגדרות Email
# ==========================================

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "")

# סוג שרת המייל (gmail / outlook / custom)
EMAIL_SERVER_TYPE = os.environ.get("EMAIL_SERVER_TYPE", "custom")

# הגדרות שרת מותאם אישית (לא Gmail)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "true").lower() == "true"

# ==========================================
# ⚙️ הגדרות כלליות
# ==========================================

# User Agent לבקשות HTTP
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Timeout לבקשות (בשניות)
REQUEST_TIMEOUT = 30

# קובץ לשמירת מוצרים שכבר נשלחו (למניעת כפילויות)
SEEN_ITEMS_FILE = "seen_items.json"

# האם לשלוח התראה גם כשאין תוצאות חדשות (לבדיקה)
NOTIFY_ON_NO_RESULTS = False
