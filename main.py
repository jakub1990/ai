import requests
from bs4 import BeautifulSoup
import time

# --- KONFIGURACJA ---
# Wklej tutaj swój adres Webhooka z Make.com
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/odxy45ta2dm9xrxm4yzpod3m7lfvvdj7"
# Adres RSS TechCrunch Robotics
RSS_URL = "https://techcrunch.com/category/robotics/feed/"

def fetch_robotics_news():
    print("Pobieranie newsów z TechCrunch Robotics...")
    response = requests.get(RSS_URL)
    
    # Używamy lxml lub xml, żeby sparsować kanał RSS
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all('item', limit=3) # Pobieramy 3 najnowsze
    
    for item in items:
        title = item.title.text
        link = item.link.text
        # Wyciągamy krótki opis, usuwając tagi HTML
        summary = BeautifulSoup(item.description.text, "html.parser").text
        
        data = {
            "title": title,
            "link": link,
            "summary": summary
        }
        
        # Wysyłka do Make.com
        try:
            res = requests.post(MAKE_WEBHOOK_URL, json=data)
            if res.status_code == 200:
                print(f"Sukces: Wysłano artykuł: {title}")
            else:
                print(f"Błąd Make.com: Status {res.status_code}")
        except Exception as e:
            print(f"Błąd wysyłki: {e}")
        
        # Mała przerwa, żeby nie przeciążyć serwerów
        time.sleep(1)

if __name__ == "__main__":
    fetch_robotics_news()

