
# LogFlow AI

**An open-source logistics automation portfolio project built with Python, FastAPI and React, with OpenClaw integration planned.**

LogFlow AI is an independent software engineering portfolio project focused on automating logistics data processing, identifying operational inconsistencies and providing useful insights through a web dashboard.

The project simulates a logistics operation involving multiple units, shipment reports, pending deliveries and operational discrepancies.

> **Project status:** Active development — synthetic data generation, Pandas reconciliation, SQLite persistence, shipment REST endpoints, and an initial React dashboard are implemented. Frontend/API integration still has known follow-up issues; see [Known Limitations](#known-limitations).

## 🎯 Project Goals

- Automate the processing of logistics reports.
- Import and validate Excel and CSV files.
- Normalize operational data from different sources.
- Identify pending shipments, delays and inconsistencies.
- Maintain an operational history.
- Provide logistics indicators through a web dashboard.
- Orchestrate scheduled tasks using OpenClaw.
- Explore AI-assisted operational summaries.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main backend language |
| uv | Python project and dependency management |
| Pandas | Data processing and reconciliation |
| FastAPI | REST API |
| SQLAlchemy | Database access and ORM |
| SQLite | Initial database |
| React | Frontend |
| JavaScript (JSX) | Frontend development |
| Vite | Frontend development server and build |
| Oxlint | Frontend linting |
| Playwright | Browser automation in a simulated environment |
| OpenClaw | Automation orchestration |
| Pytest | Automated testing |

## 🏗️ Architecture

The application is built around the following components:

1. Data generation and ingestion: synthetic CSV and Excel reports; user-provided file uploads remain planned.
2. Data normalization: standardizing columns, dates and statuses.
3. Reconciliation: comparing reports and identifying inconsistencies.
4. Persistence: storing shipments, operation units and report import history in SQLite.
5. API: exposing health and shipment queries through FastAPI.
6. Dashboard: a React prototype that reads shipment data from the API.
7. Automation: scheduled processing with OpenClaw remains planned.
8. AI assistance: explanatory summaries remain planned and must not replace deterministic business rules.

## 📂 Project Structure

```text
logflow-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── domain/shipment.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── types.py
│   │   │   └── models/
│   │   ├── repositories/shipment_repository.py
│   │   ├── schemas/shipment.py
│   │   └── services/
│   │       ├── shipment_service.py
│   │       ├── reconciliation_service.py
│   │       └── persistence_service.py
│   ├── scripts/
│   │   ├── generate_demo_data.py
│   │   ├── run_reconciliation.py
│   │   └── inspect_database.py
│   └── tests/
│       ├── conftest.py
│       └── unit/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── services/api.js
│   │   └── components/
│   └── package.json
└── data/
    └── samples/
```

## ✅ Implemented Features

### Shipment Domain

- Shipment data model using Python dataclasses.
- Shipment validation.
- Pending and dispatched status identification.
- Timezone-aware datetime validation.

### Business Rules

- Identification of pending shipments.
- Identification of delayed shipments.
- Configurable delay threshold.

### Synthetic Data Generation

- Generation of fictional logistics data.
- Simulation of multiple operational units.
- CSV and Excel report generation.
- Intentional simulation of duplicate and invalid records.

### Pandas Reconciliation

- Report column validation.
- Data normalization.
- Duplicate record identification.
- Invalid record identification.
- Comparison of received and dispatched reports.
- Detection of pending shipments.
- Detection of delayed shipments.
- Detection of dispatches without matching receipts.
- Detection of operational unit mismatches.

### Automated Tests

- Unit tests with Pytest.
- Shipment model validation.
- Business rule validation.
- Pandas reconciliation tests.
- Data quality validation.
- SQLAlchemy repository tests.
- SQLite persistence tests.
- Idempotency validation.

### Database Persistence

- SQLite database integration.
- SQLAlchemy 2.0 typed ORM models.
- Operation unit persistence.
- Shipment persistence.
- Report import history.
- SHA-256 file fingerprinting.
- Idempotent report import registration.
- Shipment upsert operations.
- UTC-aware datetime persistence.

### REST API

- FastAPI application with a health check endpoint.
- List all shipments.
- Filter persisted shipments by `pending` and `delayed` status.
- Pydantic response schema for shipment records.
- Development CORS configuration for the local Vite frontend.

### React Dashboard Prototype

- Dashboard cards for total, dispatched, pending and delayed shipments.
- Shipment table and all/pending/delayed filters.
- Loading, error, empty and retry UI states.
- API client for the three shipment list endpoints.

## 🚀 Getting Started

### Requirements

- Python 3.12
- uv
- Git

### Clone the repository

```bash
git clone https://github.com/AThomasA/logflow-ai.git
cd logflow-ai
```

### Set up the environment

```bash
uv sync
```

### Generate data and run reconciliation

On Windows PowerShell, from the repository root:

```powershell
$env:PYTHONPATH="backend"
uv run python -m backend.scripts.generate_demo_data
uv run python -m backend.scripts.run_reconciliation
uv run python -m backend.scripts.inspect_database
```

The generator writes synthetic CSV and Excel reports to `data/samples/`. Reconciliation reads the CSV reports and persists results in `data/logflow.db`.

### Run the API

The current frontend API client uses port `8001`. From the repository root, start the API on that port:

```powershell
uv run uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8001
```

Available routes:

```text
GET http://127.0.0.1:8001/api/health
GET http://127.0.0.1:8001/api/shipments
GET http://127.0.0.1:8001/api/shipments/pending
GET http://127.0.0.1:8001/api/shipments/delayed
```

Interactive API documentation is available at `http://127.0.0.1:8001/docs`.

### Run the frontend

In a second terminal:

```powershell
Set-Location frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Open the Vite URL shown in the terminal (normally `http://127.0.0.1:5173`). The backend must be running and populated with data.

To validate the frontend:

```powershell
npm run build
npm run lint
```

### Run automated tests

```powershell
uv run pytest -v
```

### Known Limitations

- `frontend/src/services/api.js` currently hard-codes `http://127.0.0.1:8001/api`; the API base URL should later be moved to frontend environment configuration.
- The API returns `received_at`, but the dashboard currently reads the misspelled `recived_at` property, so the receipt timestamp may display as `-`.
- The frontend build succeeds, but `npm run lint` currently reports unused asset imports in `frontend/src/App.jsx`.
- File upload, public deployment, authentication, scheduled processing, Playwright automation and AI summaries are not implemented yet.

Generated reports are stored in `data/samples/`.

All generated information is synthetic and intended for demonstration and testing purposes.


## 🗺️ Roadmap

- [x] Initialize project structure
- [x] Configure Python environment with uv
- [x] Implement shipment domain model
- [x] Implement shipment business rules
- [x] Generate synthetic logistics data
- [x] Generate CSV and Excel reports
- [x] Implement Pandas report reconciliation
- [x] Identify duplicate and invalid records
- [x] Implement initial automated tests
- [x] Integrate SQLite and SQLAlchemy
- [x] Persist operation units and shipments
- [x] Register imported reports
- [x] Implement initial idempotency controls
- [x] Build React dashboard
- [x] Develop REST API with FastAPI (health, all shipments, pending and delayed endpoints)
- [ ] Implement complete Excel and CSV ingestion
- [ ] Complete frontend/API integration and resolve current date-field and configuration issues
- [ ] Create simulated logistics portal
- [ ] Implement browser automation with Playwright
- [ ] Integrate OpenClaw orchestration
- [ ] Add AI-assisted summaries
- [ ] Implement integration and end-to-end tests
- [ ] Publish a demonstrable version

## 🧪 Demo and Data

The project uses synthetic logistics data and a simulated environment.

It is not connected to real carriers, private logistics systems or production customer databases.

A demonstration mode with synthetic sample data is available. Uploading user-provided spreadsheets is planned.

## 👨‍💻 Development

This project is being developed incrementally, documenting architectural decisions, implementation choices and lessons learned along the way.

Contributions, suggestions and technical feedback are welcome.

## 📄 License

License to be defined.
