# ShadeFinder 🛰️☀️

**ShadeFinder** is a geospatial project designed to solve a real-world environmental challenge: urban heat mitigation in extreme climates (specifically Kuwait - where I'm from). By combining solar physics with 3D architectural data, the application calculates and visualizes building-cast shadows in real-time to help pedestrians identify cooler walking corridors.

Fun Fact: Kuwait is one the hottest countries in the world, it was the hottest country in 2016.

---

## 🚀 Key Features
- **Real-Time Shadow Engine**: Implements trigonometric projection logic to calculate shadow geometry based on building heights and sun position.
- **Temporal Simulation**: Includes an interactive UI slider to simulate urban shading at any hour of the day.
- **3D Urban Rendering**: Visualizes city footprints and 3D building extrusions using high-performance Mapbox WebGL.
- **Live Climate Integration**: Fetches real-time temperature, humidity, and wind speed data for specific coordinates.

## 🛠️ Technical Stack
- **Backend**: Python (FastAPI), OSMnx (Geospatial Data), Pysolar (Solar tracking), Shapely (Geometric logic).
- **Frontend**: React.js, Mapbox GL JS, Axios.
- **Data Sources**: OpenStreetMap (OSM) for urban footprints, OpenWeatherMap for real-time climate metrics.

## 📐 How It Works
The application follows a client-server architecture to handle heavy geospatial computations on the backend:
1. **Data Ingestion**: The backend queries OpenStreetMap for building footprints and metadata (like `height` or `levels`) within a specific radius.
2. **Solar Calculation**: Using the `Pysolar` library, the system calculates the sun's exact **Altitude** and **Azimuth** based on the latitude, longitude, and requested time.
3. **Shadow Projection**: For every building footprint, the engine calculates a shadow length ($L$) using $L = height / \tan(altitude)$. The footprint is then translated into a new polygon projected opposite the sun's azimuth.
4. **Serialization**: The generated shadows are returned to the frontend as a **GeoJSON FeatureCollection** for efficient rendering.

## 🧠 Technical Challenges Solved
- **Handling Missing Metadata**: Developed a fallback mechanism to estimate building heights based on floor count (`building:levels`) when explicit height data was unavailable in OpenStreetMap.
- **Geospatial Coordinate Transformation**: Solved the challenge of translating physical shadow lengths (meters) into geographic coordinate shifts (Latitude/Longitude degrees) while accounting for the Earth's curvature at 29°N.
- **State-Driven Map Updates**: Integrated Mapbox sources with React state to ensure seamless re-rendering of 3D layers during real-time time-slider interactions.

## 📦 Setup and Installation

### Backend
1. Create a `.env` file in the `backend` folder and add your `OPENWEATHER_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
