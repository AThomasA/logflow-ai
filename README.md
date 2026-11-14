
# LogFlow AI

**An open-source logistics automation platform built with Python, FastAPI, React and OpenClaw.**

LogFlow AI is an independent software engineering portfolio project focused on automating logistics data processing, identifying operational inconsistencies and providing useful insights through a web dashboard.

The project simulates a logistics operation involving multiple units, shipment reports, pending deliveries and operational discrepancies.

> **Project status:** Initial development — architecture and project structure established.

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
logflow-ai/
├── backend/
├── docs/
├── data/
│   └── samples/
├── reports/
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

The structure will evolve as new components are implemented.

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

The application is still under development. Instructions for running the complete system will be added as the components become available.

## 🗺️ Roadmap

- [x] Initialize project structure
- [x] Configure Python environment with uv
- [ ] Generate synthetic logistics data
- [ ] Build shipment processing logic
- [ ] Implement Excel and CSV ingestion
- [ ] Implement data reconciliation
- [ ] Integrate SQLite and SQLAlchemy
- [ ] Develop REST API with FastAPI
- [ ] Build React dashboard
- [ ] Create simulated logistics portal
- [ ] Implement browser automation with Playwright
- [ ] Integrate OpenClaw orchestration
- [ ] Add AI-assisted summaries
- [ ] Implement automated tests
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
