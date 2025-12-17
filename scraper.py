# scraper.py - מודול סריקת האתרים

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from config import SEARCH_TERMS, USER_AGENT, REQUEST_TIMEOUT
from sites import get_enabled_sites


class GunScraper:
    """סורק אתרי יד שניה - מחלץ פרטי מודעה מלאים"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
        })

    def search_in_text(self, text: str) -> bool:
        """בודק אם הטקסט מכיל אחת ממילות החיפוש"""
        if not text:
            return False
        text_lower = text.lower()
        for term in SEARCH_TERMS:
            if term.lower() in text_lower:
                return True
        return False

    def _extract_price(self, text: str) -> str:
        """מנסה לחלץ מחיר מטקסט"""
        if not text:
            return "לא צוין"
        patterns = [
            r"(\d{1,3}(?:,\d{3})*)\s*₪",
            r"₪\s*(\d{1,3}(?:,\d{3})*)",
            r"(\d{1,3}(?:,\d{3})*)\s*ש[״\']?ח",
            r"(\d{4,5})\s*(?:שקל|שח)",
            r"מחיר[:\s]*(\d{1,3}(?:,\d{3})*)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return f"₪{match.group(1)}"
        return "לא צוין"

    def _extract_phone(self, text: str) -> str:
        """מנסה לחלץ מספר טלפון מטקסט"""
        if not text:
            return ""
        patterns = [
            r"(0\d{1,2}[-\s]?\d{7})",
            r"(05\d[-\s]?\d{7})",
            r"(\d{3}[-\s]?\d{7})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return ""

    def _extract_location(self, text: str, soup: BeautifulSoup = None) -> str:
        """מנסה לחלץ מיקום"""
        if soup:
            location_elem = soup.find(class_=re.compile(r"(location|city|area|address)", re.I))
            if location_elem:
                return location_elem.get_text().strip()[:50]
        return ""

    def _clean_text(self, text: str, max_length: int = 200) -> str:
        """מנקה טקסט מתווים מיותרים"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > max_length:
            text = text[:max_length] + "..."
        return text

    def scrape_bluegun(self) -> List[Dict]:
        """סורק את אתר BlueGun"""
        results = []
        sites = get_enabled_sites()
        site = next((s for s in sites if s["name"] == "BlueGun"), None)
        if not site:
            return results
        
        try:
            response = self.session.get(site["search_url"], timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # מחפש כרטיסי מודעות
            cards = soup.find_all(["article", "div", "a"], class_=re.compile(r"(card|listing|item|product)", re.I))
            
            for card in cards:
                card_text = card.get_text()
                if self.search_in_text(card_text):
                    link = card.find("a", href=True) if card.name != "a" else card
                    title_elem = card.find(["h2", "h3", "h4", "span"], class_=re.compile(r"(title|name)", re.I))
                    desc_elem = card.find(["p", "div"], class_=re.compile(r"(desc|content|text)", re.I))
                    
                    href = link.get("href", "") if link else ""
                    full_url = href if href.startswith("http") else site["base_url"] + href
                    
                    results.append({
                        "site": "BlueGun",
                        "title": self._clean_text(title_elem.get_text() if title_elem else card_text[:80]),
                        "url": full_url or site["url"],
                        "price": self._extract_price(card_text),
                        "description": self._clean_text(desc_elem.get_text() if desc_elem else "", 300),
                        "phone": self._extract_phone(card_text),
                        "location": self._extract_location(card_text, card),
                    })
            
            # בדיקה כללית של הדף
            if not results and self.search_in_text(soup.get_text()):
                results.append({
                    "site": "BlueGun",
                    "title": "נמצאה התאמה באתר - בדוק ידנית",
                    "url": site["url"],
                    "price": "לא צוין",
                    "description": "נמצאה התאמה למילות החיפוש בדף. מומלץ לבדוק את האתר.",
                    "phone": "",
                    "location": "",
                })
                    
        except Exception as e:
            print(f"❌ Error scraping BlueGun: {e}")
        
        return results

    def scrape_gun2(self) -> List[Dict]:
        """סורק את אתר Gun2 - מחלץ פרטים מלאים"""
        results = []
        sites = get_enabled_sites()
        site = next((s for s in sites if s["name"] == "Gun2"), None)
        if not site:
            return results
        
        try:
            urls_to_check = [site["url"], site.get("glock_page", "")]
            
            for url in urls_to_check:
                if not url:
                    continue
                    
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Gun2 משתמש במבנה ספציפי לכרטיסים
                cards = soup.find_all(["article", "div"], class_=re.compile(r"(card|listing|product|weapon|jet-listing)", re.I))
                
                for card in cards:
                    card_text = card.get_text()
                    if self.search_in_text(card_text):
                        link = card.find("a", href=True)
                        title_elem = card.find(["h2", "h3", "h4", "a"])
                        
                        # חילוץ פרטים ספציפיים מ-Gun2
                        price_elem = card.find(string=re.compile(r"מחיר"))
                        phone_elem = card.find(string=re.compile(r"טלפון|נייד"))
                        city_elem = card.find(string=re.compile(r"עיר"))
                        
                        href = link.get("href", "") if link else ""
                        full_url = href if href.startswith("http") else site["base_url"] + href
                        
                        results.append({
                            "site": "Gun2",
                            "title": self._clean_text(title_elem.get_text() if title_elem else "Glock 45 MOS"),
                            "url": full_url or url,
                            "price": self._extract_price(card_text),
                            "description": self._clean_text(card_text, 300),
                            "phone": self._extract_phone(card_text),
                            "location": self._extract_location(card_text, card),
                        })
                
                if not results and self.search_in_text(soup.get_text()):
                    results.append({
                        "site": "Gun2",
                        "title": "נמצאה התאמה באתר - בדוק ידנית",
                        "url": url,
                        "price": "לא צוין",
                        "description": "נמצאה התאמה למילות החיפוש.",
                        "phone": "",
                        "location": "",
                    })
                    
        except Exception as e:
            print(f"❌ Error scraping Gun2: {e}")
        
        return results

    def scrape_guntrade(self) -> List[Dict]:
        """סורק את אתר GunTrade"""
        results = []
        sites = get_enabled_sites()
        site = next((s for s in sites if s["name"] == "GunTrade"), None)
        if not site:
            return results
        
        try:
            response = self.session.get(site["search_url"], timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            listings = soup.find_all(["article", "div", "li"], class_=re.compile(r"(post|listing|item|card|product)", re.I))
            
            for listing in listings:
                listing_text = listing.get_text()
                if self.search_in_text(listing_text):
                    link = listing.find("a", href=True)
                    title_elem = listing.find(["h2", "h3", "h4", "a"])
                    
                    href = link.get("href", "") if link else ""
                    full_url = href if href.startswith("http") else site["base_url"] + href
                    
                    results.append({
                        "site": "GunTrade",
                        "title": self._clean_text(title_elem.get_text() if title_elem else "Glock 45 MOS"),
                        "url": full_url or site["url"],
                        "price": self._extract_price(listing_text),
                        "description": self._clean_text(listing_text, 300),
                        "phone": self._extract_phone(listing_text),
                        "location": self._extract_location(listing_text, listing),
                    })
            
            if not results and self.search_in_text(soup.get_text()):
                results.append({
                    "site": "GunTrade",
                    "title": "נמצאה התאמה באתר - בדוק ידנית",
                    "url": site["url"],
                    "price": "לא צוין",
                    "description": "נמצאה התאמה למילות החיפוש.",
                    "phone": "",
                    "location": "",
                })
                    
        except Exception as e:
            print(f"❌ Error scraping GunTrade: {e}")
        
        return results

    def scrape_yad2(self) -> List[Dict]:
        """סורק את אתר Yad2 - כולל כניסה לדפים פנימיים"""
        results = []
        sites = get_enabled_sites()
        site = next((s for s in sites if s["name"] == "Yad2 נשק"), None)
        if not site:
            return results
        
        try:
            response = self.session.get(site["url"], timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Yad2 יכול להיות דינמי, מחפשים כרטיסי מוצר
            cards = soup.find_all(["div", "article"], class_=re.compile(r"(feed-item|product|card|item)", re.I))
            
            for card in cards:
                card_text = card.get_text()
                if self.search_in_text(card_text):
                    link = card.find("a", href=True)
                    title_elem = card.find(["h2", "h3", "span"], class_=re.compile(r"(title|name)", re.I))
                    
                    href = link.get("href", "") if link else ""
                    full_url = href if href.startswith("http") else site["base_url"] + href
                    
                    # מנסה לחלץ מחיר וטלפון מהכרטיס
                    price = self._extract_price(card_text)
                    phone = self._extract_phone(card_text)
                    location = self._extract_location(card_text, card)
                    description = self._clean_text(card_text, 300)
                    
                    # אם חסר מידע, ננסה להיכנס לדף הפנימי
                    if full_url and (price == "לא צוין" or not phone):
                        try:
                            inner_data = self._fetch_inner_page(full_url)
                            if inner_data:
                                if price == "לא צוין" and inner_data.get("price"):
                                    price = inner_data["price"]
                                if not phone and inner_data.get("phone"):
                                    phone = inner_data["phone"]
                                if not location and inner_data.get("location"):
                                    location = inner_data["location"]
                                if inner_data.get("description"):
                                    description = inner_data["description"]
                        except:
                            pass
                    
                    results.append({
                        "site": "Yad2",
                        "title": self._clean_text(title_elem.get_text() if title_elem else "Glock 45 MOS"),
                        "url": full_url or site["url"],
                        "price": price,
                        "description": description,
                        "phone": phone,
                        "location": location,
                    })
            
            if not results and self.search_in_text(soup.get_text()):
                results.append({
                    "site": "Yad2",
                    "title": "נמצאה התאמה באתר - בדוק ידנית",
                    "url": site["url"],
                    "price": "לא צוין",
                    "description": "נמצאה התאמה למילות החיפוש.",
                    "phone": "",
                    "location": "",
                })
                
        except Exception as e:
            print(f"❌ Error scraping Yad2: {e}")
        
        return results

    def _fetch_inner_page(self, url: str) -> Optional[Dict]:
        """נכנס לדף פנימי של מודעה ומחלץ פרטים נוספים"""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text()
            
            result = {}
            
            # חילוץ מחיר
            price_elem = soup.find(class_=re.compile(r"(price|cost|מחיר)", re.I))
            if price_elem:
                result["price"] = self._extract_price(price_elem.get_text())
            else:
                result["price"] = self._extract_price(page_text)
            
            # חילוץ טלפון - מחפש בכל הדף
            result["phone"] = self._extract_phone(page_text)
            
            # חילוץ מיקום
            location_elem = soup.find(class_=re.compile(r"(location|city|area|address|עיר|מיקום)", re.I))
            if location_elem:
                result["location"] = self._clean_text(location_elem.get_text(), 50)
            
            # חילוץ תיאור מפורט
            desc_elem = soup.find(class_=re.compile(r"(description|content|details|תיאור|פרטים)", re.I))
            if desc_elem:
                result["description"] = self._clean_text(desc_elem.get_text(), 500)
            
            return result
            
        except Exception as e:
            print(f"⚠️ Could not fetch inner page {url}: {e}")
            return None

    def scrape_yad2_market(self) -> List[Dict]:
        """סורק את אתר Yad2 Market"""
        results = []
        sites = get_enabled_sites()
        site = next((s for s in sites if s["name"] == "Yad2 Market נשק"), None)
        if not site:
            return results
        
        try:
            response = self.session.get(site["search_url"], timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            products = soup.find_all(["div", "article"], class_=re.compile(r"(product|item|card)", re.I))
            
            for product in products:
                product_text = product.get_text()
                if self.search_in_text(product_text):
                    link = product.find("a", href=True)
                    title_elem = product.find(["h2", "h3", "span"])
                    
                    href = link.get("href", "") if link else ""
                    full_url = href if href.startswith("http") else site["base_url"] + href
                    
                    results.append({
                        "site": "Yad2 Market",
                        "title": self._clean_text(title_elem.get_text() if title_elem else "Glock 45 MOS"),
                        "url": full_url or site["url"],
                        "price": self._extract_price(product_text),
                        "description": self._clean_text(product_text, 300),
                        "phone": self._extract_phone(product_text),
                        "location": self._extract_location(product_text, product),
                    })
            
            if not results and self.search_in_text(soup.get_text()):
                results.append({
                    "site": "Yad2 Market",
                    "title": "נמצאה התאמה באתר - בדוק ידנית",
                    "url": site["url"],
                    "price": "לא צוין",
                    "description": "נמצאה התאמה למילות החיפוש.",
                    "phone": "",
                    "location": "",
                })
                    
        except Exception as e:
            print(f"❌ Error scraping Yad2 Market: {e}")
        
        return results

    def scrape_all(self) -> List[Dict]:
        """סורק את כל האתרים הפעילים ומחזיר תוצאות"""
        all_results = []
        enabled_sites = get_enabled_sites()
        
        print(f"📡 סורק {len(enabled_sites)} אתרים...")
        
        # מפה בין שמות אתרים לפונקציות סריקה
        scraper_map = {
            "BlueGun": self.scrape_bluegun,
            "Gun2": self.scrape_gun2,
            "GunTrade": self.scrape_guntrade,
            "Yad2 נשק": self.scrape_yad2,
            "Yad2 Market נשק": self.scrape_yad2_market,
        }
        
        for site in enabled_sites:
            site_name = site["name"]
            if site_name in scraper_map:
                print(f"  🔍 סורק {site_name}...")
                try:
                    results = scraper_map[site_name]()
                    all_results.extend(results)
                    if results:
                        print(f"     ✅ נמצאו {len(results)} תוצאות")
                    else:
                        print(f"     ⚪ לא נמצאו תוצאות")
                except Exception as e:
                    print(f"     ❌ שגיאה: {e}")
        
        # מסיר כפילויות לפי URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)
        
        return unique_results


if __name__ == "__main__":
    scraper = GunScraper()
    results = scraper.scrape_all()
    
    if results:
        print(f"\n{'='*50}")
        print(f"📊 נמצאו {len(results)} תוצאות:")
        print('='*50)
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r['site']}")
            print(f"    📦 {r['title']}")
            print(f"    💰 {r['price']}")
            if r.get('description'):
                print(f"    📝 {r['description'][:100]}...")
            print(f"    🔗 {r['url']}")
    else:
        print("\n❌ לא נמצאו תוצאות")
