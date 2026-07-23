# Enterprise Customer Segmentation AI Web Platform
### *Production Full-Stack Analytics Application & Machine Learning Engine*

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.104-009688.svg)](https://fastapi.tiangolo.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-v5.3-7952B3.svg)](https://getbootstrap.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-v1.2%2B-orange.svg)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Production-Passing-brightgreen.svg)]()
[![Documentation](https://img.shields.io/badge/Documentation-50%20Pages%20PDF-purple.svg)](Documentation.pdf)

---

## 📌 Executive Overview & Web Application Features

The **Enterprise Customer Segmentation AI Web Platform** is an end-to-end full-stack analytics application built for financial institutions to discover actionable customer personas within credit card portfolios. Built upon **8,950 customer profiles** across 18 financial metrics, the application delivers a modern responsive Glassmorphism dashboard interface, interactive Plotly 3D visualizers, automated REST APIs, and instant 50-page documentation downloads.

### 🌟 Key Web Application Highlights
- **Interactive Executive Dashboard**: Live KPI cards, Chart.js segment share donut plots, and financial metric comparison bars.
- **Dataset Explorer**: Paginated datatable supporting instant CUST_ID search, cluster filtering, and raw/processed CSV exports.
- **Clustering Analytics Lab**: Interactive WCSS Elbow Curve, Silhouette profile selector, and K-Means vs Hierarchical model comparison.
- **Customer Personas Hub**: Glassmorphism cards featuring data-driven persona stats, risk ratings, and McKinsey strategic recommendations.
- **Visualization Gallery**: Multi-category gallery with 3D Plotly interactive scatter plots, full-screen modal previews, and PNG downloads.
- **One-Click Download Hub**: Instant access to 50-page PDF/DOCX technical specifications, segmented CSV datasets, and executed Jupyter Notebooks.
- **OpenAPI Swagger Interface**: Complete REST API documentation at `/docs` and ReDoc at `/redoc`.
- **Dark/Light Theme Switcher**: Automatic theme toggle with state persistence in `localStorage`.

---

## 🏗️ System & Full-Stack Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        USER BROWSER / CLIENT                           │
│     Bootstrap 5.3 Glassmorphic UI • Chart.js 4.4 • Plotly 3D Embeds     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      NGINX REVERSE PROXY (Port 80)                     │
│               Gzip Compression • Static Caching & Proxy Pass           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     FASTAPI WEB SERVER (Port 8000)                     │
│  ┌───────────────────────────┐       ┌──────────────────────────────┐  │
│  │ Jinja2 HTML View Routers  │       │  REST API Router Controllers │  │
│  └─────────────┬─────────────┘       └──────────────┬───────────────┘  │
│                │                                    │                  │
│                ▼                                    ▼                  │
│  ┌───────────────────────────┐       ┌──────────────────────────────┐  │
│  │  Services Layer           │       │ SQLAlchemy SQLite Database   │  │
│  │  (Data & ML Services)     │       │ (ExecutionLogs & Downloads) │  │
│  └─────────────┬─────────────┘       └──────────────────────────────┘  │
└────────────────┼───────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   UNSUPERVISED MACHINE LEARNING ENGINE                 │
│   • Log1p Transform & StandardScaler Z-score Normalization             │
│   • K-Means Clustering (Optimal K=4, Silhouette: 0.2086, WCSS: 92,131)  │
│   • Hierarchical Ward Linkage Agglomerative Clustering                 │
│   • Principal Component Analysis (2D & 3D Spatial Projections)         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ Web Application Pages

| Page | URL Path | Key Features |
| :--- | :--- | :--- |
| **Landing Page** | [`/`](http://127.0.0.1:8000/) | Hero header, project overview, architectural flow, quick KPI stats counters |
| **Executive Dashboard** | [`/dashboard`](http://127.0.0.1:8000/dashboard) | Live KPI metrics, Chart.js donut chart, financial comparison bar chart, persona overview |
| **Dataset Explorer** | [`/dataset`](http://127.0.0.1:8000/dataset) | Paginated datatable with live CUST_ID search, cluster filter, statistical summary cards |
| **Clustering Lab** | [`/clusters`](http://127.0.0.1:8000/clusters) | Interactive Elbow Curve, Silhouette profile selector, metric table, model benchmark |
| **Customer Personas** | [`/personas`](http://127.0.0.1:8000/personas) | 4 Glassmorphism persona profile cards, risk levels, McKinsey strategic recommendations |
| **Visual Gallery** | [`/gallery`](http://127.0.0.1:8000/gallery) | 3D Plotly interactive embed, 12 publication graphics, modal preview, PNG export |
| **Reports & Exports** | [`/reports`](http://127.0.0.1:8000/reports) | Download hub for PDF, DOCX, CSV, and IPYNB deliverables |
| **About & Architecture**| [`/about`](http://127.0.0.1:8000/about) | Technology stack matrix, REST API routes list, developer info, Swagger links |

---

## 🔌 REST API Endpoints

FastAPI automatically generates interactive Swagger documentation accessible at **`http://127.0.0.1:8000/docs`**.

| Method | Endpoint Path | Description |
| :---: | :--- | :--- |
| `GET` | `/api/dataset` | Get paginated customer records with search & cluster filtering |
| `GET` | `/api/dataset/summary` | Get dataset feature summary statistics (mean, std, min, max) |
| `GET` | `/api/dataset/correlations` | Get Pearson correlation matrix values |
| `GET` | `/api/metrics` | Get K-Means evaluation metrics for K=2 to K=10 |
| `GET` | `/api/comparison` | Get algorithm benchmark comparison (K-Means vs Hierarchical) |
| `GET` | `/api/clusters` | Get cluster centroids and market share percentages |
| `GET` | `/api/personas` | Get detailed JSON persona specifications |
| `GET` | `/api/charts` | Get gallery metadata for all pre-generated 300 DPI graphics |
| `GET` | `/api/reports/download/{file_id}` | Stream file downloads (`pdf`, `docx`, `csv`, `notebook`, `readme`) |
| `GET` | `/api/system/health` | Get server uptime, memory usage, CPU %, and download count |

---

## 📊 Experimental ML Metric Evaluation

### K-Means Metric Evaluation ($K = 2 \dots 10$)

| K | WCSS / Inertia | Silhouette Score | Calinski-Harabasz Index | Davies-Bouldin Index |
| :---: | :---: | :---: | :---: | :---: |
| **2** | 119,113.49 | **0.2215** | 2,481.76 | 1.6706 |
| **3** | 101,330.45 | 0.2103 | 2,243.56 | 1.7115 |
| **4** | **92,131.16** | **0.2086** | **1,942.65** | **1.7047** |
| **5** | 84,764.15 | 0.1983 | 1,777.78 | 1.6058 |
| **6** | 77,909.01 | 0.2063 | 1,704.58 | 1.5217 |
| **7** | 73,635.31 | 0.1966 | 1,589.27 | 1.5629 |
| **8** | 69,848.25 | 0.1993 | 1,505.19 | 1.4821 |
| **9** | 66,812.96 | 0.1925 | 1,427.49 | 1.4849 |
| **10** | 64,003.40 | 0.1843 | 1,368.04 | 1.4634 |

---

## 🚀 Deployment & Installation

### Option 1: Local Python Execution
```bash
# 1. Clone repository
git clone https://github.com/enterprise-analytics/customer-segmentation-app.git
cd customer-segmentation-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch FastAPI Application
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open **`http://127.0.0.1:8000`** in your browser.

---

### Option 2: Docker & Docker Compose
```bash
# Build and launch multi-container stack (FastAPI Web App + Nginx Reverse Proxy)
docker-compose up --build -d
```
Access the application at **`http://localhost`** (Nginx Port 80) or **`http://localhost:8000`** (FastAPI Direct).

---

### Option 3: Cloud Deployment (Render / Heroku)
The repository includes pre-configured deployment files:
- **`Procfile`**: Process definition for Uvicorn execution
- **`render.yaml`**: Render Blueprint configuration
- **`runtime.txt`**: Python version declaration (`python-3.11.9`)

To deploy to Render, create a new Web Service connected to your GitHub repository. Render will automatically detect `render.yaml` and deploy.

---

## 📁 Complete Repository Directory Structure

```text
week 04 IT Simplera/
├── app/
│   ├── main.py                          # FastAPI Application Entrypoint
│   ├── api/
│   │   └── routers/
│   │       ├── views.py                 # Jinja2 HTML Page Controllers (8 Pages)
│   │       ├── dataset_api.py           # Dataset Pagination & Search API
│   │       ├── analytics_api.py         # K-Means, Silhouette & Centroids API
│   │       ├── reports_api.py           # File Download Controller API
│   │       └── system_api.py            # Health Check & DB Download Logs API
│   ├── core/
│   │   ├── config.py                    # Environment Configuration
│   │   ├── logging.py                   # Rotating Log Infrastructure
│   │   └── security.py                  # CORS & Security Headers Middleware
│   ├── database/
│   │   ├── models.py                    # SQLite Models (ExecutionLog, DownloadLog)
│   │   └── connection.py                # SQLAlchemy Session Management
│   ├── services/
│   │   ├── data_service.py              # Data Pagination & Query Service
│   │   └── ml_service.py                # Model Analytics & Persona Service
│   ├── templates/
│   │   ├── base.html                    # Master Layout Shell with Sidebar & Header
│   │   ├── index.html                   # 1. Landing Page
│   │   ├── dashboard.html               # 2. Executive Dashboard
│   │   ├── dataset.html                 # 3. Dataset Explorer
│   │   ├── clusters.html                # 4. Clustering Lab
│   │   ├── personas.html                # 5. Customer Personas Showcase
│   │   ├── gallery.html                 # 6. Visualization Gallery
│   │   ├── reports.html                 # 7. Reports & Download Hub
│   │   └── about.html                   # 8. About & Architecture Page
│   └── static/
│       ├── css/
│       │   ├── styles.css               # Glassmorphism Design System & Themes
│       │   └── animations.css           # Smooth Keyframes & Transitions
│       └── js/
│           ├── main.js                  # Sidebar & Toast Notifications
│           ├── theme.js                 # Dark/Light Mode LocalStorage Manager
│           ├── dashboard.js             # Chart.js Executive Graphs
│           └── charts.js                # Clustering Lab Line Plots
├── data/                                # Raw and Processed Datasets
├── charts/                              # Pre-generated 300 DPI Graphics & Plotly HTML
├── reports/                             # PDF, DOCX, CSV Summary Reports
├── notebooks/                           # Executed Jupyter Notebook
├── .github/workflows/ci-cd.yml          # GitHub Actions CI/CD Pipeline
├── Dockerfile                           # Multi-Stage Production Dockerfile
├── docker-compose.yml                   # Docker Compose Configuration
├── nginx.conf                           # Nginx Reverse Proxy & Static Cache Config
├── Procfile                             # Render / Heroku Web Process Declaration
├── render.yaml                          # Render Deployment Blueprint
├── runtime.txt                          # Python Version Specification
├── .env.example                         # Environment Variables Template
├── Documentation.docx                   # 50-Page Enterprise Technical Specification (DOCX)
├── Documentation.pdf                    # 50-Page Enterprise Technical Specification (PDF)
├── requirements.txt                     # Production Python Dependencies
├── LICENSE                              # MIT License
└── README.md                            # Application README Documentation
```

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
