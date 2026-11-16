
# LogFlow AI

**An open-source logistics automation platform built with Python, FastAPI, React and OpenClaw.**

LogFlow AI is an independent software engineering portfolio project focused on automating logistics data processing, identifying operational inconsistencies and providing useful insights through a web dashboard.

The project simulates a logistics operation involving multiple units, shipment reports, pending deliveries and operational discrepancies.

> **Project status:** Active development — shipment modeling, business rules, synthetic data generation and Pandas reconciliation implemented.

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
| TypeScript | Frontend development |
| Playwright | Browser automation in a simulated environment |
| OpenClaw | Automation orchestration |
| Pytest | Automated testing |

## 🏗️ Planned Architecture

The application is planned around the following components:

1. Data ingestion: importing Excel and CSV reports.
2. Data normalization: standardizing columns, dates and statuses.
3. Reconciliation: comparing reports and identifying inconsistencies.
4. Persistence: storing shipments, events and execution history.
5. API: exposing operational data through FastAPI.
6. Dashboard: presenting indicators and discrepancies.
7. Automation: coordinating scheduled processes.
8. AI assistance: generating explanatory summaries without replacing deterministic business rules.

## 📂 Project Structure

```text
backend/
├── app/
│   ├── domain/
│   │   └── shipment.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── types.py
│   │   └── models/
│   │       ├── operation_unit.py
│   │       ├── shipment.py
│   │       └── report_import.py
│   ├── repositories/
│   │   └── shipment_repository.py
│   └── services/
│       ├── shipment_service.py
│       ├── reconciliation_service.py
│       └── persistence_service.py
├── scripts/
│   ├── generate_demo_data.py
│   ├── run_reconciliation.py
│   └── inspect_database.py
└── tests/
    ├── conftest.py
    └── unit/
```

The structure will evolve as new components are implemented.


```markdown
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

### Generate synthetic logistics reports

```bash
uv run python -m backend.scripts.generate_demo_data
```

### Run the reconciliation process

```bash
uv run python -m backend.scripts.run_reconciliation
```
### Run the reconciliation pipeline

On Windows PowerShell:

```bash
$env:PYTHONPATH="backend"

uv run python -m backend.scripts.generate_demo_data

uv run python -m backend.scripts.run_reconciliation

uv run python -m backend.scripts.inspect_database
```
### Run automated tests

```bash
uv run pytest -v
```

The application is still under development. Instructions for running the complete system will be added as the components become available.

The generated reports are stored in data/samples/.

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
- [ ] Implement complete Excel and CSV ingestion
- [ ] Develop REST API with FastAPI
- [ ] Build React dashboard
- [ ] Create simulated logistics portal
- [ ] Implement browser automation with Playwright
- [ ] Integrate OpenClaw orchestration
- [ ] Add AI-assisted summaries
- [ ] Implement integration and end-to-end tests
- [ ] Publish a demonstrable version

## 🧪 Demo and Data

The project uses synthetic logistics data and a simulated environment.

It is not connected to real carriers, private logistics systems or production customer databases.

A demonstration mode for sample data and user-provided spreadsheets is planned.

## 👨‍💻 Development

This project is being developed incrementally, documenting architectural decisions, implementation choices and lessons learned along the way.

Contributions, suggestions and technical feedback are welcome.

## 📄 License

License to be defined.
