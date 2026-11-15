# Diseases Detection Platform — Full-Stack Application

The production web application and clinical workbench for the **Hybrid Quantum Machine Learning Platform for Early Disease Detection**.

The platform provides a complete clinical workflow: tabular dataset ingestion, automated data quality analysis, leakage-free preprocessing with an autonomous AI agent, interactive quantum circuit design, and model training/evaluation benchmarking classical algorithms against Variational Quantum Classifiers (VQC).

---

## Architecture Overview

The application is structured into decoupled frontend, backend, and database tiers orchestrated via Docker Compose:

```mermaid
flowchart TD
    subgraph Client ["Frontend Single Page App (React 18 + Vite)"]
        Browser["Clinician Browser"]
        ReactRouter["React Router DOM (Protected Routes)"]
        QueryClient["TanStack React Query Cache"]
        CircuitUI["Quantum Circuit Designer (SVG)"]
    end

    subgraph Gateway ["Nginx Web Server (Port 3000)"]
        Nginx["Nginx Reverse Proxy & Static Host"]
    end

    subgraph API ["Backend Web Service (FastAPI / Uvicorn Port 8000)"]
        FastAPI["FastAPI REST API (/api/v1)"]
        AuthModule["Auth & Security (JWT, Argon2id)"]
        DatasetModule["Dataset Ingestion & Schema Profiling"]
        AgentModule["AI Preprocessing Engine (LangGraph / Scikit)"]
        QMLModule["PennyLane VQC Simulator (QNode)"]
        CMLModule["Classical ML (Linear/RBF SVM, Logistic)"]
    end

    subgraph Database ["Database & Persistence Tier"]
        MongoDB[("MongoDB 6.0 (Beanie ODM)")]
        LocalDisk[("Mounted Artifact Storage (/app/artifacts)")]
    end

    Browser -->|Port 3000| Nginx
    Nginx --> ReactRouter
    ReactRouter --> QueryClient & CircuitUI
    QueryClient -->|REST API HTTPS / JWT| FastAPI
    
    FastAPI --> AuthModule & DatasetModule & AgentModule & QMLModule & CMLModule
    AuthModule & DatasetModule & AgentModule & QMLModule & CMLModule --> MongoDB
    DatasetModule & AgentModule & QMLModule --> LocalDisk
```

---

## Directory Structure

```text
Diseases_Detection_Paltform/
├── docker-compose.yml        # Multi-service stack (MongoDB, Redis, MinIO, Backend, Frontend)
├── README.md                 # Platform documentation
├── backend/                  # FastAPI asynchronous backend
│   ├── app/
│   │   ├── api/v1/           # REST endpoints: auth, datasets, prep, training, predictions
│   │   ├── core/             # Configuration, logging, JWT security
│   │   ├── database/models/  # 14 Beanie ODM MongoDB Document models
│   │   ├── ml/               # PennyLane VQC & Scikit-Learn SVM wrappers
│   │   ├── agents/           # Integrated AI Preprocessing Agent
│   │   └── services/         # Dataset, training, prediction, artifact services
│   ├── tests/                # Pytest unit and API integration tests
│   ├── Dockerfile            # Python 3.11 slim container build
│   └── requirements.txt      # Backend Python dependencies
└── frontend/                 # React 18 + Vite + TypeScript frontend
    ├── src/
    │   ├── api/              # Strongly typed Axios API client modules
    │   ├── components/       # CircuitDesigner, PreprocessingPlan, Navigation
    │   ├── context/          # AuthContext for session management
    │   ├── pages/            # Datasets, Preprocessing, Features, Models, Predictions
    │   └── router.tsx        # React Router route configuration
    ├── Dockerfile            # Multi-stage production container build (Node -> Nginx)
    ├── nginx.conf            # Nginx SPA fallback configuration
    └── package.json          # Node dependencies
```

---

## Technology Stack

| Tier | Technology | Purpose |
|---|---|---|
| **Frontend Framework** | React 18.3 + TypeScript | Interactive, type-safe clinical user interface |
| **Frontend Tooling** | Vite 5.3 + Tailwind CSS | Fast development server, CSS utility design tokens |
| **Frontend State** | TanStack React Query 5.50 | Server-state caching and background data synchronization |
| **Backend Framework** | FastAPI 0.111 + Uvicorn | High-concurrency asynchronous RESTful API |
| **Database ODM** | Beanie 1.26 + Motor 3.4 | Async ODM for MongoDB with Pydantic v2 schemas |
| **Database Engine** | MongoDB 6.0 | Document store for dataset versions, training runs, and models |
| **Quantum Computing** | PennyLane 0.38 | Parameterized quantum circuits, statevector & density matrix simulation |
| **Classical ML** | Scikit-learn 1.5 | Classical SVM baselines, SFS feature selection, data transformers |
| **Autonomous Agent** | LangGraph & Scikit-learn | Schema analysis, leakage-free transformation execution |
| **Containerization** | Docker & Docker Compose | Multi-container orchestration and environment isolation |

---

## Implemented Workflows

```mermaid
sequenceDiagram
    autonumber
    actor User as Researcher / Clinician
    participant Front as React Frontend
    participant API as FastAPI Backend
    participant Mongo as MongoDB
    participant Disk as Artifact Storage

    User->>Front: 1. Upload CSV Dataset
    Front->>API: POST /api/v1/datasets/{id}/versions
    API->>Disk: Store CSV file under /app/artifacts/
    API->>Mongo: Save DatasetVersion & Schema Profile
    API-->>Front: Return schema summary & target candidates

    User->>Front: 2. Generate Preprocessing Plan
    Front->>API: POST /api/v1/preprocessing/plan
    API-->>Front: Return 8-step transformation strategy

    User->>Front: 3. Configure Quantum Circuit & Train
    Front->>API: POST /api/v1/training (VQC: 6 qubits, 2 layers)
    API->>Disk: Split 70/15/15 & fit scaler strictly on train
    API->>API: Execute PennyLane VQC QNode gradient optimization
    API->>Disk: Save trained_model.joblib
    API->>Mongo: Record TrainingRun metrics & loss curves
    API-->>Front: Training complete notification

    User->>Front: 4. Calibrated Prediction & Triage
    Front->>API: POST /api/v1/predictions (patient inputs, threshold)
    API->>Disk: Load fitted transformers & quantum parameters
    API-->>Front: Return probability, risk tier, and provenance
```

---

## Quick Start (Docker Compose)

### 1. Prerequisites
- Docker Engine 24.0+
- Docker Compose v2.0+

### 2. Launch Stack
From this directory:
```bash
docker compose up --build -d
```

### 3. Verify Containers
```bash
docker compose ps
```

### 4. Service Endpoints
| Service | URL | Credentials |
|---|---|---|
| **Web Dashboard** | [http://localhost:3000](http://localhost:3000) | `hqml@gmail.com` / `12345678` |
| **FastAPI Swagger Docs** | [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs) | N/A |
| **API Health Probe** | [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) | N/A |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | `minioadmin` / `minioadmin` |
| **MongoDB** | `localhost:27017` | Standard connection |

To stop the platform:
```bash
docker compose down
```

---

## Local Development (Without Docker)

### Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\Activate.ps1 | On Unix: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Troubleshooting & Verification

- **Large Dataset Upload Failures (413 Request Entity Too Large):** Nginx has been configured with `client_max_body_size 100M;` and Axios client timeout is set to 5 minutes (`300,000ms`). Ensure Docker has sufficient memory allocated.
- **Vite Proxy in Docker:** Ensure `VITE_API_BASE_URL` is set to `http://localhost:8000/api/v1` (or your public backend URL) during frontend production builds.
