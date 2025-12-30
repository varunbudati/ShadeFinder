import osmnx as ox
from pysolar.solar import get_altitude, get_azimuth
from shapely.geometry import Polygon
from datetime import datetime, timezone
import math

# 1. Setup Location (Salmiya, Kuwait)
lat, lon = 29.3375, 48.0791 
dist = 500 # meters around the point

# 2. Fetch Buildings
# Tags for building footprints and heights
buildings = ox.features_from_point((lat, lon), tags={'building': True}, dist=dist)

# 3. Get Sun Position
now = datetime.now(timezone.utc)
altitude = get_altitude(lat, lon, now)
azimuth = get_azimuth(lat, lon, now)

def calculate_shadow(row):
    # Default height to 10m if data is missing
    height = float(row.get('height', 10))
    
    # Shadow math: length = height / tan(altitude)
    if altitude > 0:
        shadow_len = height / math.tan(math.radians(altitude))
    else:
        shadow_len = 0 # Night time
        
    # Angle is opposite to sun azimuth
    shadow_angle = (azimuth + 180) % 360
    
    # Logic to project the footprint polygon by shadow_len 
    # (Simplified for this snippet)
    return f"Shadow length: {shadow_len:.2f}m at {shadow_angle:.2f}°"

# Apply to first 5 buildings to test
print(f"Sun Altitude: {altitude:.2f}°, Azimuth: {azimuth:.2f}°")
print(buildings[['name', 'building:levels']].head())

