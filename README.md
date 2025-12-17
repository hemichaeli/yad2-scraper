# 🔍 YAD2 Scraper

סורק אוטומטי לאתרי יד2 ואתרים נוספים עם התראות לטלגרם ואימייל.

## 🚀 התקנה

### שלב 1: GitHub
העלה את כל הקבצים **חוץ מ-ui.html** ל-Repository.

### שלב 2: Secrets
לך ל-Settings → Secrets → Actions והוסף:

| Secret | ערך |
|--------|-----|
| `TELEGRAM_BOT_TOKEN` | טוקן הבוט |
| `TELEGRAM_CHAT_ID` | Chat ID שלך |
| `EMAIL_ADDRESS` | אימייל לשליחה |
| `EMAIL_PASSWORD` | סיסמה |
| `NOTIFY_EMAIL` | אימייל לקבלת התראות |
| `SMTP_SERVER` | smtp.gmail.com |
| `SMTP_PORT` | 465 |
| `UI_URL` | לינק ל-Netlify |

### שלב 3: Netlify
העלה את `ui.html` בתור `index.html`

## 📅 סריקות
08:00, 14:00, 20:30 (שעון ישראל)

## 🔧 שימוש
פתח UI → ערוך הגדרות → שמור ל-GitHub
