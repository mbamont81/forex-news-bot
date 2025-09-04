import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_investing():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Error accediendo a Investing.com: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    events = []
    current_date = datetime.now()
    month = current_date.strftime("%B")

    # Buscar filas de la tabla de eventos
    for row in soup.select("tr.js-event-item"):
        try:
            time_cell = row.select_one("td.time")
            currency_cell = row.select_one("td.left.flagCur span")
            impact_cell = row.select("td.sentiment span")
            event_cell = row.select_one("td.event")

            time = time_cell.get_text(strip=True) if time_cell else ""
            currency = currency_cell.get_text(strip=True) if currency_cell else ""
            event = event_cell.get_text(strip=True) if event_cell else ""

            # Impacto: basado en número de "bullish icons" (1-3)
            impact = "grey"
            if impact_cell:
                stars = len(impact_cell)
                if stars == 1:
                    impact = "yellow"
                elif stars == 2:
                    impact = "orange"
                elif stars >= 3:
                    impact = "red"

            if currency and event:
                events.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "time": time,
                    "currency": currency,
                    "impact": impact,
                    "event": event
                })
        except Exception as e:
            print("Error parsing row:", e)

    # Guardar siempre CSV
    output_path = f"news/{month}_news.csv"
    if events:
        df = pd.DataFrame(events)
        df.to_csv(output_path, index=False)
        print(f"✅ Archivo actualizado: {output_path} con {len(events)} eventos")
    else:
        df = pd.DataFrame(columns=["date","time","currency","impact","event"])
        df.to_csv(output_path, index=False)
        print(f"⚠️ No se encontraron eventos, se creó un CSV vacío: {output_path}")


if __name__ == "__main__":
    scrape_investing()
