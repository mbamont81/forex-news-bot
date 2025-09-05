import requests
from bs4 import BeautifulSoup

def debug_investing():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print("✅ Conexión correcta con Investing.com")
        print("📄 Primeros 1000 caracteres del HTML descargado:\n")
        print(response.text[:1000])  # mostramos solo los primeros 1000
    except Exception as e:
        print(f"⚠️ Error accediendo a Investing.com: {e}")

if __name__ == "__main__":
    debug_investing()
