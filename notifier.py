# notifier.py - מודול שליחת התראות

import smtplib
import ssl
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    NOTIFY_EMAIL,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USE_SSL,
)


class Notifier:
    """שולח התראות מפורטות בטלגרם ובמייל"""

    def send_telegram(self, message: str) -> bool:
        """שולח הודעה לטלגרם"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("⚠️ Telegram credentials not configured")
            return False

        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("✅ Telegram message sent successfully")
            return True
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
            return False

    def send_email(self, subject: str, body: str) -> bool:
        """שולח מייל - תומך בשרתים שונים"""
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not NOTIFY_EMAIL:
            print("⚠️ Email credentials not configured")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = NOTIFY_EMAIL

            # גרסת טקסט פשוט
            text_content = self._html_to_text(body)
            text_part = MIMEText(text_content, "plain", "utf-8")
            
            # גרסת HTML
            html_body = f"""
            <!DOCTYPE html>
            <html dir="rtl" lang="he">
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        direction: rtl; 
                        background: #f5f5f5;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 10px;
                        padding: 20px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h2 {{
                        color: #333;
                        border-bottom: 2px solid #007bff;
                        padding-bottom: 10px;
                    }}
                    .result {{ 
                        border: 1px solid #e0e0e0; 
                        padding: 15px; 
                        margin: 15px 0; 
                        border-radius: 8px;
                        background: #fafafa;
                        transition: all 0.3s;
                    }}
                    .result:hover {{
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .site {{ 
                        color: #007bff; 
                        font-size: 12px; 
                        font-weight: bold;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    .title {{ 
                        font-size: 18px; 
                        font-weight: bold; 
                        margin: 10px 0;
                        color: #333;
                    }}
                    .price {{ 
                        color: #28a745; 
                        font-size: 20px;
                        font-weight: bold;
                        margin: 10px 0;
                    }}
                    .description {{
                        color: #666;
                        font-size: 14px;
                        margin: 10px 0;
                        line-height: 1.5;
                    }}
                    .link {{
                        display: inline-block;
                        background: #007bff;
                        color: white !important;
                        padding: 10px 20px;
                        border-radius: 5px;
                        text-decoration: none;
                        margin-top: 10px;
                    }}
                    .link:hover {{
                        background: #0056b3;
                    }}
                    .footer {{
                        color: #888;
                        font-size: 12px;
                        margin-top: 20px;
                        padding-top: 15px;
                        border-top: 1px solid #eee;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    {body}
                </div>
            </body>
            </html>
            """
            html_part = MIMEText(html_body, "html", "utf-8")
            
            msg.attach(text_part)
            msg.attach(html_part)

            # שליחה - תומך ב-SSL וב-TLS
            if SMTP_USE_SSL:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())
            else:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())
            
            print("✅ Email sent successfully")
            return True
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

    def _html_to_text(self, html: str) -> str:
        """ממיר HTML לטקסט פשוט"""
        import re
        text = re.sub(r'<br\s*/?>', '\n', html)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def format_results(self, results: List[Dict]) -> tuple:
        """מעצב את התוצאות להודעה מפורטת עם כל פרטי המודעה"""
        if not results:
            return "", ""

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # ==========================================
        # הודעת Telegram - מפורטת עם לינק
        # ==========================================
        telegram_msg = f"🔔 <b>התראה: נמצאו {len(results)} תוצאות!</b>\n"
        telegram_msg += f"⏰ {now}\n"
        telegram_msg += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, r in enumerate(results, 1):
            telegram_msg += f"<b>📍 [{i}] {r['site']}</b>\n"
            telegram_msg += f"━━━━━━━━━━━━━━\n"
            telegram_msg += f"📦 <b>{r['title']}</b>\n"
            
            if r.get('price') and r['price'] != "לא ידוע":
                telegram_msg += f"💰 <b>{r['price']}</b>\n"
            
            if r.get('description'):
                desc = r['description'][:150] + "..." if len(r.get('description', '')) > 150 else r.get('description', '')
                telegram_msg += f"📝 {desc}\n"
            
            if r.get('location'):
                telegram_msg += f"📍 {r['location']}\n"
            
            if r.get('phone'):
                telegram_msg += f"📞 {r['phone']}\n"
            
            telegram_msg += f"\n🔗 <a href=\"{r['url']}\">לצפייה במודעה</a>\n\n"

        telegram_msg += "━━━━━━━━━━━━━━━━━━━━\n"
        telegram_msg += "🤖 YAD2 Scraper - סריקה אוטומטית"

        # ==========================================
        # הודעת Email - מעוצבת עם כל הפרטים
        # ==========================================
        email_body = f"<h2>🔔 התראה: נמצאו {len(results)} תוצאות!</h2>"
        email_body += f"<p style='color: #666;'>⏰ {now}</p>"
        
        for r in results:
            email_body += f"""
            <div class="result">
                <div class="site">📍 {r['site']}</div>
                <div class="title">📦 {r['title']}</div>
            """
            
            if r.get('price') and r['price'] != "לא ידוע":
                email_body += f'<div class="price">💰 {r["price"]}</div>'
            
            if r.get('description'):
                desc = r['description'][:300] + "..." if len(r.get('description', '')) > 300 else r.get('description', '')
                email_body += f'<div class="description">📝 {desc}</div>'
            
            if r.get('location'):
                email_body += f'<div class="description">📍 מיקום: {r["location"]}</div>'
            
            if r.get('phone'):
                email_body += f'<div class="description">📞 טלפון: {r["phone"]}</div>'
            
            email_body += f"""
                <a href="{r['url']}" class="link" target="_blank">🔗 לצפייה במודעה</a>
            </div>
            """

        email_body += """
        <div class="footer">
            🤖 YAD2 Scraper - סריקה אוטומטית<br>
            לשינוי הגדרות, ערוך את קובץ config.py
        </div>
        """

        return telegram_msg, email_body

    def notify(self, results: List[Dict]) -> bool:
        """שולח התראות בכל הערוצים"""
        if not results:
            print("ℹ️ No results to notify")
            return False

        telegram_msg, email_body = self.format_results(results)
        
        telegram_success = self.send_telegram(telegram_msg)
        email_success = self.send_email(
            subject=f"🔔 YAD2 Scraper: נמצאו {len(results)} תוצאות חדשות!",
            body=email_body
        )

        return telegram_success or email_success

    def send_test_notification(self) -> bool:
        """שולח התראת בדיקה"""
        test_results = [
            {
                "site": "בדיקה",
                "title": "מודעת בדיקה - הכל עובד!",
                "url": "https://example.com",
                "price": "₪1,234",
                "description": "זוהי מודעת בדיקה לוודא שהמערכת עובדת כראוי.",
                "location": "תל אביב",
                "phone": "050-1234567",
            }
        ]
        return self.notify(test_results)

    def send_daily_status(self, ui_url: str) -> bool:
        """שולח הודעת סטטוס יומית עם כפתור ON/OFF"""
        from datetime import datetime
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # הודעת Telegram עם כפתורים
        telegram_msg = f"✅ <b>YAD2 Scraper - פעיל</b>\n\n"
        telegram_msg += f"📅 {now}\n"
        telegram_msg += f"🔍 הסורק רץ ומחפש עבורך\n\n"
        telegram_msg += f"⚙️ <a href=\"{ui_url}\">ניהול | ON/OFF</a>"
        
        telegram_success = self.send_telegram(telegram_msg)
        
        # לא שולח מייל על סטטוס יומי - רק טלגרם
        return telegram_success


if __name__ == "__main__":
    # בדיקה
    notifier = Notifier()
    notifier.send_test_notification()
