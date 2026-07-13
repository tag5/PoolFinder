# https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/
# https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/01.csv.gz

import io
import os
import glob
import csv
import math
import requests
from PIL import Image

def get_satellite_view(lat, lon, output_file):
    span_m = 50 # Zoom
    dlat = (span_m / 2) / 111_320
    dlon = (span_m / 2) / (111_320 * math.cos(math.radians(lat)))
    bbox = f"{lat - dlat},{lon - dlon},{lat + dlat},{lon + dlon}"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetMap",
        "LAYERS": "ORTHOIMAGERY.ORTHOPHOTOS",
        "CRS": "EPSG:4326", # WGS84
        "BBOX": bbox,
        "WIDTH": 512,
        "HEIGHT": 512,
        "FORMAT": "image/jpeg",
        "STYLES": "",
    }
    print(params)
    r = requests.get('https://data.geopf.fr/wms-r/wms', params=params)
    r.raise_for_status()
    Image.open(io.BytesIO(r.content)).save(output_file)

csv_files = glob.glob(os.path.join('/csv/', "*.csv"))
for csv_file in csv_files:
  print(csv_file)
  with open(csv_file, newline="") as f:
    for row in csv.DictReader(f):
      lon = row["longitude"]
      lat = row["latitude"]

      if not lon or not lat:
        continue

      output_file = os.path.join('/images/', row["id_mutation"] + ".webp")
      if os.path.exists(output_file):
        continue

      get_satellite_view(float(lat), float(lon), output_file)
