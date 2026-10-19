# EO Data Finder

EO Data Finder is a web application designed to search, review, and explore Earth Observation satellite products, with an initial focus on Sentinel-2 imagery and environmental monitoring in Mali.

The project is developed incrementally using Agile principles, with new features delivered and evaluated during each sprint.

## Sprint 1 — Product and Foundation

The first sprint focused on establishing the product concept and developing an initial React prototype.

**Implemented features:**
- Geographic area selection.
- Start and end date inputs.
- Maximum cloud coverage input.
- Search form validation.
- Demonstration Sentinel-2 product catalogue.
- Simulated vegetation and drought-risk analysis preview.
- Initial user interface and GitHub project organization.

Sprint 1 established the frontend foundation and initial user workflow.

See [Sprint 1 Report](SPRINT_1.md).

## Sprint 2 — Functional MVP

Sprint 2 extends the initial frontend prototype into an integrated application using React, FastAPI, SQLAlchemy, and SQLite.

### Implemented features

**Backend and database**
- Python FastAPI backend.
- SQLite database using SQLAlchemy.
- Three demonstration Sentinel-2 product records.
- REST API endpoint: `GET /api/products`.
- Interactive API documentation through Swagger UI.

**Multi-criteria search**
- Acquisition start date filtering.
- Acquisition end date filtering.
- Maximum cloud coverage filtering.
- Pilot-area validation for Sikasso, Mali.
- React-to-FastAPI API integration.
- Search results retrieved from SQLite.

**Frontend improvements**
- Improved and more consistent interface design.
- Structured satellite product results table.
- Interactive product selection.
- Selected product metadata displayed in the analysis workspace.
- Clear messages when no products match the search criteria.
- Explicit labels for simulated environmental indicators.

**Software quality**
- 14 automated API tests using Pytest.
- Isolated in-memory SQLite database for automated tests.
- Input validation and API response testing.
- Successful React production build.

### Application architecture

`React + Vite → FastAPI → SQLAlchemy → SQLite`

The frontend sends search parameters to the FastAPI backend, which queries the SQLite database and returns matching product metadata.

## Technologies

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

**Testing and development**
- Pytest
- FastAPI TestClient
- Node.js
- pnpm
- Git and GitHub

## Run the project locally

### 1. Frontend

From the project root directory, install the dependencies:

```bash
pnpm install
```

Start the development server:

```bash
pnpm run dev
```

Open the local address displayed by Vite, normally:

`http://localhost:5173`

### 2. Backend (Windows PowerShell)

Open a second terminal and navigate to the backend directory:

```powershell
cd backend
```

If the Python virtual environment does not exist, create it:

```powershell
py -m venv .venv
```

Install backend dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Initialize the demonstration catalogue:

```powershell
.\.venv\Scripts\python.exe seed.py
```

Start FastAPI:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

**Backend API:** `http://127.0.0.1:8000`

**Swagger API documentation:** `http://127.0.0.1:8000/docs`

Both the frontend and backend servers must be running to use the integrated application.

## Automated tests

From the `backend` directory, execute:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_products.py -v
```

Sprint 2 test results: **14 tests passed**.

The tests use an isolated in-memory SQLite database instead of relying on the application's local development data.

## Current MVP limitations

- The product catalogue currently contains three demonstration Sentinel-2 records.
- Sikasso is the only supported pilot area; real spatial footprint filtering has not yet been implemented.
- Live Copernicus catalogue integration is not yet available.
- Real satellite band retrieval and processing are planned for future development.
- NDVI, rainfall anomaly, and drought-risk indicators are currently simulated.
- Environmental analysis outputs must not be interpreted as scientifically validated drought assessments or operational warnings.

## Agile project management

Development follows an iterative sprint-based workflow using GitHub Projects for task tracking and progress monitoring.

**Sprint reports:**
- [Sprint 1 — Product and Foundation](SPRINT_1.md)
- Sprint 2 — Functional MVP (report in preparation)

**GitHub Project Board:**
https://github.com/users/samake3699-ctrl/projects/1/views/1

## Future development

Planned improvements include live Sentinel-2 catalogue integration, satellite image processing, NDVI computation, rainfall data integration, and progressive development of the environmental analysis workflow.

These capabilities will be introduced and validated through future sprints.