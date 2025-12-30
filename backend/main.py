import requests
import os
from dotenv import load_dotenv
load_dotenv()
@app.get("/weather")
def get_current_weather(lat: float, lon: float):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        return {"error": "API key not set in environment"}
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return {
        "temp": response['main']['temp'],
        "humidity": response['main']['humidity'],
        "wind_speed": response['wind']['speed'],
        "description": response['weather'][0]['description']
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import osmnx as ox
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone
import math
from shapely.geometry import Polygon, mapping
from shapely.affinity import translate, scale

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def project_shadow(footprint, height, alt, az):
    """
    Calculates a shadow polygon based on building footprint and sun position.
    """
    if alt <= 0:
        return None  # No shadow at night
    
    # 1. Shadow length: L = h / tan(altitude)
    # We use a small multiplier to make coordinates match map scales
    shadow_len = height / math.tan(math.radians(alt))
    
    # 2. Shadow direction is opposite to sun azimuth
    # Mapbox/Math uses 0 at North, clockwise. 
    angle_rad = math.radians(az + 180)
    
    # 3. Calculate offset (how far the shadow moves from the building)
    dist_lat = (shadow_len * math.cos(angle_rad)) / 111320 # Approx meters to degrees
    dist_lon = (shadow_len * math.sin(angle_rad)) / (111320 * math.cos(math.radians(29)))

    # 4. Create shadow by shifting the footprint
    shadow_poly = translate(footprint, xoff=dist_lon, yoff=dist_lat)
    return shadow_poly


@app.get("/shadows")
def get_shadows(lat: float, lon: float, hour: int = None):
    now = datetime.now(timezone.utc)
    if hour is not None:
        now = now.replace(hour=int(hour), minute=0, second=0)
    alt = get_altitude(lat, lon, now)
    az = get_azimuth(lat, lon, now)

    # For testing during Kuwait night, let's "fake" a sunny afternoon altitude
    # Remove these two lines later for real-time accuracy!
    if alt <= 0: alt = 35.0  

    gdf = ox.features_from_point((lat, lon), tags={'building': True}, dist=500)

    shadows_geojson = []

    for _, row in gdf.iterrows():
        # Get height (default to 15m if missing)
        h = float(row.get('height', 15))

        shadow_poly = project_shadow(row['geometry'], h, alt, az)

        if shadow_poly:
            shadows_geojson.append({
                "type": "Feature",
                "geometry": mapping(shadow_poly),
                "properties": {"type": "shadow"}
            })

    return {
        "sun": {"altitude": alt, "azimuth": az},
        "shadows": {
            "type": "FeatureCollection",
            "features": shadows_geojson
        }
    }