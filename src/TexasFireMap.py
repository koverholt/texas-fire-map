import Algorithmia
import pytz
import pandas as pd
from datetime import datetime, timedelta

TIMEZONE = "US/Central"


def get_fire_incidents(fetch_date):
    for i in range(1, 45):
        try:
            file_string = (
                "https://fsapps.nwcg.gov/afm/data/lg_fire/lg_fire_nifc_"
                + str(fetch_date)
                + ".csv"
            )
            df = pd.read_csv(file_string)
            df = df[df["fire_number"].str.startswith("TX-")]
            break
        except:
            fetch_date = fetch_date - timedelta(days=1)

    num_fire_incidents = len(df)
    total_fire_area = int(sum(df["area"]))
    formatted_fire_area = '{:,}'.format(total_fire_area)

    if df.empty:
        df = df.append(
            {
                "latitude": "",
                "longitude": "",
                "fire_name": "",
                "fire_number": "",
                "area": 0,
                "report_date": "",
            },
            ignore_index=True,
        )

    return df, num_fire_incidents, total_fire_area, formatted_fire_area, fetch_date


fetch_date = datetime.now(pytz.timezone(TIMEZONE)).date()

(
    fire_incidents,
    num_fire_incidents,
    total_fire_area,
    formatted_fire_area,
    fetch_date,
) = get_fire_incidents(fetch_date)

result = {
    "fire_incidents": fire_incidents.to_json(orient="records"),
    "num_fire_incidents": num_fire_incidents,
    "total_fire_area": total_fire_area,
    "formatted_fire_area": formatted_fire_area,
    "fetch_date": fetch_date.strftime("%B %-d, %Y")
}


def apply(input):
    print(result)
    return result


if __name__ == "__main__":
    apply(input)
