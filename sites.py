# sites.py - רשימת אתרים לסריקה
# נוצר אוטומטית על ידי YAD2 Scraper UI

SITES = [
    {
        "name": "BlueGun",
        "url": "https://bluegun.co.il/explore-classic/",
        "base_url": "https://bluegun.co.il",
        "enabled": true,
    },
    {
        "name": "Gun2",
        "url": "https://gun2.co.il/",
        "base_url": "https://gun2.co.il",
        "enabled": true,
    },
    {
        "name": "GunTrade",
        "url": "https://guntrade.co.il/",
        "base_url": "https://guntrade.co.il",
        "enabled": true,
    },
    {
        "name": "Yad2 נשק",
        "url": "https://www.yad2.co.il/products/weapons?category=27",
        "base_url": "https://www.yad2.co.il",
        "enabled": true,
    },
    {
        "name": "Yad2 Market נשק",
        "url": "https://market.yad2.co.il/collections/%D7%9B%D7%9C%D7%99-%D7%A0%D7%A9%D7%A7",
        "base_url": "https://market.yad2.co.il",
        "enabled": true,
    },
    {
        "name": "Yad2 כללי",
        "url": "https://www.yad2.co.il/products/all",
        "base_url": "https://www.yad2.co.il",
        "enabled": true,
    },
    {
        "name": "Yad2 רכב",
        "url": "https://www.yad2.co.il/vehicles/cars",
        "base_url": "https://www.yad2.co.il",
        "enabled": true,
    },
    {
        "name": "Yad2 נדלן",
        "url": "https://www.yad2.co.il/realestate/forsale",
        "base_url": "https://www.yad2.co.il",
        "enabled": true,
    },
]

def get_enabled_sites():
    """מחזיר רק אתרים פעילים"""
    return [site for site in SITES if site.get("enabled", True)]

def get_site_by_name(name):
    """מחזיר אתר לפי שם"""
    for site in SITES:
        if site["name"] == name:
            return site
    return None
