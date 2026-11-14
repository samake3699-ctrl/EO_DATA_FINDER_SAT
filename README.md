# EO Data Finder

**Earth Observation Satellite Data Discovery and Experimental Environmental Monitoring**

**Student:** Adama SAMAKE  
**Group:** M80-103CB-26  
**University:** Moscow Aviation Institute (MAI)  
**Course:** Agile Methodologies  
**Project type:** Individual semester project

## 1. Project Overview

EO Data Finder is a web application designed to help users search, review, and manage Earth Observation satellite products.

The project focuses initially on Sentinel-2 Level-2A products from the Copernicus Data Space catalogue, using Sikasso, Mali, as the pilot study area.

Its long-term objective is to support vegetation monitoring and experimental drought-risk analysis using satellite imagery and environmental data.

Development follows an incremental Agile approach, with features implemented, tested, demonstrated, and reviewed during successive sprints.

## 2. Main Objectives

- Simplify the discovery of relevant satellite products.
- Search products using acquisition dates and cloud coverage.
- Retrieve authentic Sentinel-2 product metadata.
- Display and select available satellite products.
- Store selected product metadata in a local database.
- Prepare an interactive environment for vegetation and drought analysis.
- Progressively introduce real satellite imagery processing.

## 3. Sprint Development Progress

### Sprint 1 — Product and Foundation

**Period:** October 5–18, 2026  
**Status:** Completed

Sprint 1 established the product concept and the initial React application.

**Main achievements:**

- React and Vite development environment.
- Satellite search form.
- Geographic area and date selection.
- Cloud coverage input and validation.
- Demonstration Sentinel-2 product catalogue.
- Simulated environmental analysis preview.
- Initial Agile backlog and GitHub Project Board.

The first sprint used demonstration data without accessing the real Copernicus catalogue.

**Deliverables:**

- [Sprint 1 Report](SPRINT_1.md)
- [Sprint 1 Demonstration Video](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/releases/tag/sprint-1)

### Sprint 2 — Functional MVP

**Period:** October 19 – November 1, 2026  
**Status:** Completed

Sprint 2 transformed the initial frontend prototype into an integrated application.

**Main achievements:**

- Python FastAPI backend.
- SQLite database and SQLAlchemy integration.
- React-to-FastAPI communication.
- Date and cloud coverage filtering.
- Product selection and analysis navigation.
- Improved interface organization.
- 14 automated backend tests passed.

The satellite catalogue still used demonstration records.

**Deliverables:**

- [Sprint 2 Source Code](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s2-prep)
- [Sprint 2 Report](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/blob/s2-prep/SPRINT_2.md)
- [Sprint 2 Demonstration Video](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/releases/tag/sprint-2)

### Sprint 3 — Real Copernicus Integration

**Period:** November 2–15, 2026  
**Status:** Completed

Sprint 3 introduced real Sentinel-2 product metadata retrieval through the Copernicus Data Space catalogue.

**Main achievements:**

- Integration with the official Copernicus OData API.
- Search for real Sentinel-2 Level-2A products.
- Acquisition date and cloud coverage filters.
- Display of authentic product identifiers and metadata.
- Storage of selected product metadata in SQLite.
- Duplicate product detection.
- Connection to the experimental Analysis Workspace.
- 18 automated backend tests passed.
- Verification of retrieved metadata against the official Copernicus catalogue.

**Important:** The application retrieves real satellite product metadata, but NDVI, rainfall anomaly, and drought-risk indicators remain simulated.

**Deliverables:**

- [Sprint 3 Source Code](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s3-prep)
- [Sprint 3 Report](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/blob/s3-prep/SPRINT_3.md)
- [Sprint 3 Demonstration Video — 4 min 57 s](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/releases/tag/sprint-3)

### Sprint 4 — Geospatial Visualization and Satellite Processing

**Status:** In development

Sprint 4 focuses on further improving the geospatial interface and developing the foundations for real satellite data retrieval and processing.

The Sprint 4 work is maintained separately from the completed Sprint 3 release.

[View Sprint 4 Development Branch](https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT/tree/s4-prep)

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite, SQLAlchemy |
| Satellite catalogue | Copernicus Data Space OData API |
| Automated testing | Pytest, FastAPI TestClient |
| Package management | pnpm |
| Version control | Git and GitHub |
| Agile management | GitHub Projects |
| Geospatial development | Leaflet and React-Leaflet (Sprint 4) |

## 5. Application Architecture

The Sprint 3 application uses the following workflow:

**Search:** React → FastAPI → Copernicus Data Space → React

**Product storage:** React → FastAPI → SQLAlchemy → SQLite

Copernicus supplies real satellite product metadata. SQLite stores metadata for selected products.

The application does not yet store or scientifically process complete Sentinel-2 image products as part of the completed Sprint 3 deliverable.

## 6. Running the Application Locally

### Clone the repository

```powershell
git clone https://github.com/samake3699-ctrl/EO_DATA_FINDER_SAT.git
cd EO_DATA_FINDER_SAT
```

The default `main` branch retains the initial frontend foundation. To run the integrated Sprint 3 implementation, switch to its development branch:

```powershell
git switch s3-prep
```

### Start the frontend

```powershell
pnpm install
pnpm dev
```

Open the URL displayed by Vite, normally:

`http://localhost:5173`

### Start the backend

Open a second PowerShell terminal:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Backend address:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

Both frontend and backend servers must be running for the integrated workflow.

Live Copernicus searches also require an internet connection.

## 7. Testing and Validation

From the `backend` directory of the Sprint 3 branch, run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

**Documented test results:**

- Sprint 2: 14 automated tests passed.
- Sprint 3: 18 automated tests passed.

The test suite covers API behavior, search filters, metadata handling, and duplicate detection.

Automated tests use controlled test data and mocked external catalogue responses where appropriate. Live Copernicus integration was also checked separately.

## 8. Current Limitations

- The completed Sprint 3 search focuses on the Sikasso pilot area.
- Live searches return a limited number of matching products.
- SQLite stores satellite product metadata, not complete satellite imagery.
- NDVI and rainfall anomaly calculations are not yet validated using real imagery and rainfall data.
- Drought-risk results remain experimental and simulated.
- The application is not an operational drought warning or forecasting service.

These limitations are intentionally documented to distinguish implemented functionality from future scientific capabilities.

## 9. Agile Project Management

The project uses an iterative development workflow supported by GitHub Issues and GitHub Projects.

The board organizes work through:

**Backlog → Todo → In Progress → Testing → Done**

Sprint reports document objectives, implementation results, testing, retrospective findings, and learning outcomes.

[View the Public Agile Project Board](https://github.com/users/samake3699-ctrl/projects/1/views/1)

## 10. Future Development

Future work will focus on:

- Retrieving the necessary Sentinel-2 spectral bands.
- Processing authentic satellite imagery using Python.
- Computing NDVI from real Sentinel-2 observations.
- Integrating rainfall datasets such as CHIRPS.
- Evaluating vegetation and experimental drought-risk indicators.
- Improving geographic visualization and analysis results.
- Expanding testing, reliability, and application usability.

These activities are development objectives and should not be interpreted as completed Sprint 3 capabilities.

---
