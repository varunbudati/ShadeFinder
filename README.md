# ShadeFinder

## Project Overview
ShadeFinder helps users find walking routes with the most shade, using sun position calculations and map data.

### Architecture Breakdown
- **backend/**: FastAPI server, sun/shadow logic, pathfinding
- **frontend/**: React app, Mapbox integration, UI components

#### Backend
- `main.py`: FastAPI entry point
- `solar_logic.py`: Sun position & shadow math
- `routing.py`: Pathfinding (A* algorithm)
- `requirements.txt`: Python dependencies

#### Frontend
- `src/components/`: MapView, TimeSlider, RoutePanel
- `src/hooks/`: Custom hooks for Mapbox integration
- `public/`: Static assets
- `package.json`: Frontend dependencies


### How to run
- Backend (FastAPI server):
cd /Users/varunbudati/Documents/GitHub/ShadeFinder/backend
source ../../venv/bin/activate
uvicorn main:app --reload

- Frontend (Vite React app):
cd /Users/varunbudati/Documents/GitHub/ShadeFinder/frontend
npm run dev
