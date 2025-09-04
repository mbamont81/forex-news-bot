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
    month = datetime.now().strftime("%B")

    current_event_date = None

    # Recorre todas las filas de la tabla
    for row in soup.select("tr"):
        # Filas que son separadores de fecha
        date_cell = row.select_one("td.theDay")
        if date_cell:
            # Texto del estilo "Thursday, Sep 5, 2025"
            date_text = date_cell.get_text(strip=True)
            try:
                current_event_date = datetime.strptime(date_text, "%A, %b %d, %Y").strftime("%Y-%m-%d")
            except Exception:
                current_event_date = None
            continue

        # Filas que son eventos
        if "js-event-item" in row.get("class", []):
            try:
                time_cell = row.select_one("td.time")
                currency_cell = row.select_one("td.left.flagCur span")
                impact_cell = row.select("td.sentiment span")
                event_cell = row.select_one("td.event")

                time = time_cell.get_text(strip=True) if time_cell else ""
                currency = currency_cell.get_text(strip=True) if currency_cell else ""
                event = event_cell.get_text(strip=True) if event_cell else ""

                # Impacto: número de íconos "bullish"
                impact = "grey"
                if impact_cell:
                    stars = len(impact_cell)
                    if stars == 1:
                        impact = "yellow"
                    elif stars == 2:
                        impact = "orange"
                    elif stars >= 3:
                        impact = "red"

                if currency and event and current_event_date:
                    events.append({
                        "date": current_event_date,
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
