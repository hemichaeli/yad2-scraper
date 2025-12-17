# sites.py - הגדרות האתרים לסריקה
# ============================================
# קובץ זה מכיל את רשימת האתרים לסריקה.
# ניתן להוסיף, להסיר או לשנות אתרים בקלות.
# ============================================

SITES = [
    # ==========================================
    # אתרי נשק יד שניה
    # ==========================================
    {
        "name": "BlueGun",
        "url": "https://bluegun.co.il/explore-classic/",
        "type": "dynamic",
        "search_url": "https://bluegun.co.il/explore-classic/?type=cars&category=%25d7%2590%25d7%25a7%25d7%2593%25d7%2597%25d7%2599%25d7%259d-%25d7%2599%25d7%25932&sort=latest",
        "base_url": "https://bluegun.co.il",
        "enabled": True,  # שנה ל-False כדי להשבית
    },
    {
        "name": "Gun2",
        "url": "https://gun2.co.il/",
        "type": "static",
        "search_url": "https://gun2.co.il/",
        "base_url": "https://gun2.co.il",
        "glock_page": "https://gun2.co.il/weapon-brand/%d7%92%d7%9c%d7%95%d7%a7/",
        "enabled": True,
    },
    {
        "name": "GunTrade",
        "url": "https://guntrade.co.il/",
        "type": "static",
        "search_url": "https://guntrade.co.il/%d7%9c%d7%95%d7%97-%d7%99%d7%932/",
        "base_url": "https://guntrade.co.il",
        "enabled": True,
    },
    {
        "name": "Yad2 נשק",
        "url": "https://www.yad2.co.il/products/weapons?category=27",
        "type": "api",
        "api_url": "https://gw.yad2.co.il/search-products/search",
        "base_url": "https://www.yad2.co.il",
        "enabled": True,
    },
    {
        "name": "Yad2 Market נשק",
        "url": "https://market.yad2.co.il/collections/%D7%9B%D7%9C%D7%99-%D7%A0%D7%A9%D7%A7",
        "type": "static",
        "search_url": "https://market.yad2.co.il/collections/%D7%9B%D7%9C%D7%99-%D7%A0%D7%A9%D7%A7",
        "base_url": "https://market.yad2.co.il",
        "enabled": True,
    },

    # ==========================================
    # אתרים נוספים (מושבתים כברירת מחדל)
    # הסר את ה-# והשנה enabled ל-True להפעלה
    # ==========================================
    
    # {
    #     "name": "Yad2 כללי",
    #     "url": "https://www.yad2.co.il/products/all",
    #     "type": "static",
    #     "search_url": "https://www.yad2.co.il/products/all",
    #     "base_url": "https://www.yad2.co.il",
    #     "enabled": False,
    # },
    # {
    #     "name": "Yad2 רכב",
    #     "url": "https://www.yad2.co.il/vehicles/cars",
    #     "type": "static",
    #     "search_url": "https://www.yad2.co.il/vehicles/cars",
    #     "base_url": "https://www.yad2.co.il",
    #     "enabled": False,
    # },
    # {
    #     "name": "Yad2 נדלן",
    #     "url": "https://www.yad2.co.il/realestate/forsale",
    #     "type": "static",
    #     "search_url": "https://www.yad2.co.il/realestate/forsale",
    #     "base_url": "https://www.yad2.co.il",
    #     "enabled": False,
    # },
]


def get_enabled_sites():
    """מחזיר רק את האתרים הפעילים"""
    return [site for site in SITES if site.get("enabled", True)]


def add_site(name, url, base_url, site_type="static", enabled=True, **kwargs):
    """הוספת אתר חדש לרשימה"""
    new_site = {
        "name": name,
        "url": url,
        "type": site_type,
        "search_url": kwargs.get("search_url", url),
        "base_url": base_url,
        "enabled": enabled,
    }
    new_site.update(kwargs)
    SITES.append(new_site)
    return new_site
