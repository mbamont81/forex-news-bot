import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_forexfactory():
    url = "https://www.forexfactory.com/calendar.php"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    current_date = datetime.now()
    month = current_date.strftime("%B")
    year = current_date.strftime("%Y")

    # Busca filas de la tabla de noticias
    for row in soup.select("tr.calendar__row"):
        try:
            time_cell = row.select_one("td.calendar__time")
            currency_cell = row.select_one("td.calendar__currency")
            impact_cell = row.select_one("td.calendar__impact span")
            event_cell = row.select_one("td.calendar__event")

            # Extraer datos limpios
            time = time_cell.get_text(strip=True) if time_cell else ""
            currency = currency_cell.get_text(strip=True) if currency_cell else ""
            impact = impact_cell.get("title").lower() if impact_cell else "grey"
            event = event_cell.get_text(strip=True) if event_cell else ""

            if currency and event:
                events.append({
                    "date": current_date.strftime("%Y-%m-%d"),  # puedes ajustarlo si quieres fechas exactas
                    "time": time,
                    "currency": currency,
                    "impact": impact,
                    "event": event
                })
        except Exception as e:
            print("Error parsing row:", e)

    # Guardar CSV
    if events:
        df = pd.DataFrame(events)
        output_path = f"news/{month}_news.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ Archivo actualizado: {output_path}")
    else:
        print("⚠️ No se encontraron eventos")

if __name__ == "__main__":
    scrape_forexfactory()
