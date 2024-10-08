import os
import pytz
import requests
import pandas as pd
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TIMEZONE = "US/Central"
# Data source URL
url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/IMSR_Incident_Locations_Most_Recent_View/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

def convert_to_iso8601(datetime_str):
    try:
        # Parse the given datetime string and convert it to date in ISO 8601 format
        dt = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
        return dt.date().isoformat()
    except (ValueError, TypeError):
        return None

def get_fire_incidents():
    try:
        # Fetch the GeoJSON data
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract relevant fields
        fire_incidents = [
            {
                "latitude": feature['geometry']['coordinates'][1],
                "longitude": feature['geometry']['coordinates'][0],
                "fire_name": feature['properties'].get("fire_name", ""),
                "fire_number": feature['properties'].get("incident_id", ""),
                "area": feature['properties'].get("size", 0),
                "report_date": convert_to_iso8601(feature['properties'].get("IrwinFireDiscoveryDateTime", ""))
            }
            for feature in data['features']
            if feature['properties'].get("incident_id", "").startswith("TX-")
        ]

        df = pd.DataFrame(fire_incidents)

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching data: {e}")
        df = pd.DataFrame()

    # If no valid data is present, handle it gracefully
    if df.empty or "area" not in df.columns:
        df = pd.DataFrame([{
            "latitude": "",
            "longitude": "",
            "fire_name": "",
            "fire_number": "",
            "area": 0,
            "report_date": "",
        }])
        num_fire_incidents = 0
    else:
        num_fire_incidents = len(df)

    # Summary calculations
    total_fire_area = int(df["area"].sum()) if "area" in df.columns else 0
    formatted_fire_area = '{:,}'.format(total_fire_area)

    return df, num_fire_incidents, total_fire_area, formatted_fire_area


@app.route('/')
def index():
    # Fetch and process fire incidents
    fire_incidents, num_fire_incidents, total_fire_area, formatted_fire_area = get_fire_incidents()

    # Fetch the current date
    fetch_date = datetime.now(pytz.timezone(TIMEZONE)).date()

    # Prepare result
    result = {
        "fire_incidents": fire_incidents.to_json(orient="records"),
        "num_fire_incidents": num_fire_incidents,
        "total_fire_area": total_fire_area,
        "formatted_fire_area": formatted_fire_area,
        "fetch_date": fetch_date.strftime("%B %-d, %Y")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
