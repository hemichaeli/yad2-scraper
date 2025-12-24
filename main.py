#!/usr/bin/env python3
# main.py - הסקריפט הראשי

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Set
from scraper import GunScraper
from notifier import Notifier
from config import SEEN_ITEMS_FILE

# קבצים
STATUS_FILE = "status.json"


def generate_item_id(item: Dict) -> str:
    """יוצר מזהה ייחודי לפריט"""
    unique_string = f"{item['site']}:{item['url']}:{item['title']}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def load_seen_items() -> Set[str]:
    """טוען פריטים שכבר נראו"""
    try:
        if os.path.exists(SEEN_ITEMS_FILE):
            with open(SEEN_ITEMS_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("items", []))
    except Exception as e:
        print(f"Error loading seen items: {e}")
    return set()


def save_seen_items(items: Set[str]) -> None:
    """שומר פריטים שנראו"""
    try:
        with open(SEEN_ITEMS_FILE, "w") as f:
            json.dump({
                "items": list(items),
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        print(f"Error saving seen items: {e}")


def load_status() -> Dict:
    """טוען סטטוס המערכת"""
    try:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {
        "enabled": True,
        "last_weekly_notification": None,
        "created_at": datetime.now().isoformat()
    }


def save_status(status: Dict) -> None:
    """שומר סטטוס המערכת"""
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)
    except Exception as e:
        print(f"Error saving status: {e}")


def should_send_daily_status() -> bool:
    """בודק אם צריך לשלוח הודעת סטטוס יומית (רק ב-20:30 שעון ישראל)"""
    from datetime import timezone, timedelta
    
    # שעון ישראל UTC+2 (חורף) / UTC+3 (קיץ)
    israel_tz = timezone(timedelta(hours=2))
    now_israel = datetime.now(israel_tz)
    
    # בודק אם השעה היא בין 20:00 ל-21:00
    return 20 <= now_israel.hour < 21


def filter_new_items(results: List[Dict], seen_items: Set[str]) -> List[Dict]:
    """מסנן רק פריטים חדשים"""
    new_items = []
    for item in results:
        item_id = generate_item_id(item)
        if item_id not in seen_items:
            new_items.append(item)
    return new_items


def get_notification_settings(status: Dict) -> Dict:
    """מקבל הגדרות התראות - מ-status.json או מ-environment variables"""
    settings = {
        "telegram_chat_id": status.get("telegram_chat_id") or os.environ.get("TELEGRAM_CHAT_ID"),
        "notify_email": status.get("notify_email") or os.environ.get("NOTIFY_EMAIL"),
    }
    return settings


def main():
    """הפונקציה הראשית"""
    print("=" * 50)
    print(f"🔫 YAD2 Scraper")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # טוען סטטוס
    status = load_status()
    ui_url = os.environ.get("UI_URL", "https://yad2-scraper-config.netlify.app")
    
    # מקבל הגדרות התראות מ-status.json או מ-environment
    notification_settings = get_notification_settings(status)
    
    # בודק אם המערכת מכובה
    if not status.get("enabled", True):
        print("⏸️ הסורק מושבת. הפעל אותו דרך ה-UI.")
        return
    
    # טוען פריטים שכבר נראו
    seen_items = load_seen_items()
    print(f"📋 {len(seen_items)} פריטים שכבר נראו")
    
    # סורק את כל האתרים
    scraper = GunScraper()
    all_results = scraper.scrape_all()
    
    print(f"\n📊 סה\"כ נמצאו: {len(all_results)} תוצאות")
    
    # יוצר notifier עם הגדרות מותאמות
    notifier = Notifier(
        telegram_chat_id=notification_settings.get("telegram_chat_id"),
        notify_email=notification_settings.get("notify_email")
    )
    
    if all_results:
        # מסנן רק פריטים חדשים
        new_items = filter_new_items(all_results, seen_items)
        print(f"🆕 פריטים חדשים: {len(new_items)}")
        
        if new_items:
            # שולח התראות
            success = notifier.notify(new_items)
            
            if success:
                # מעדכן את רשימת הפריטים שנראו
                for item in new_items:
                    seen_items.add(generate_item_id(item))
                save_seen_items(seen_items)
                print("✅ התראות נשלחו בהצלחה!")
                
                # מאפס את ההודעה השבועית כי שלחנו הודעה
                status["last_weekly_notification"] = datetime.now().isoformat()
            else:
                print("⚠️ בעיה בשליחת ההתראות")
    else:
        print("❌ לא נמצאו תוצאות")
    
    # בודק אם צריך לשלוח הודעת סטטוס יומית (רק בסריקת 20:00)
    if should_send_daily_status():
        print("📅 שולח הודעת סטטוס יומית...")
        notifier.send_daily_status(ui_url)
    
    # שומר סטטוס
    save_status(status)
    
    print("\n" + "=" * 50)
    print("✅ הסריקה הסתיימה")
    print("=" * 50)


if __name__ == "__main__":
    main()
