5. **Read Guides** → `docs/` folder
6. **Add Features** → Follow patterns in existing code
7. **Test Changes** → Restart app, check dashboard

Early Risk Signals – Credit Card Delinquency Prediction System

A lightweight, modular system that identifies early behavioral signals of credit card delinquency using rule-based indicators and a machine learning model. Includes a backend API (FastAPI) and an interactive dashboard.

⭐ Key Features

Early warning signals (spending decline, utilization, payment behavior, cash usage)

ML-based 3-class delinquency prediction (Clean, Early, High Risk)

Real-time scoring API

Interactive dashboard for customer scoring & risk visualization

Modular, developer-friendly project structure

📁 Project Structure
credit_card_delinquency_watch/
├── backend/
│   ├── app/               # API, services, ML model loading
│   ├── data/              # Dataset and model files
│   └── main.py            # FastAPI entry point
│
├── frontend/
│   └── public/index.html  # Dashboard UI
│
├── docs/                  # Additional documentation (optional)
├── run.py                 # App launcher
└── requirements.txt
├── Dockerfile            
├── docker-compose.yml


🚀 Quick Start
1. Create Environment & Install Dependencies
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt

2. Run the Application
python run.py

3. Access the System

Dashboard: http://localhost:8000

API Documentation: http://localhost:8000/docs

🔌 Core API Endpoints
Endpoint	Method	Description
/api/v1/score-customer	POST	Score a single customer
/api/v1/customers	GET	Get all customers with risk tiers
/api/v1/risk-distribution	GET	Risk score distribution
/api/v1/signals	GET	Behavioral signal breakdown
📊 ML Model (Summary)

Algorithm: Gradient Boosting Classifier

Classes: 0 – Clean, 1 – Early, 2 – High Risk

Features: Utilization, payment ratio, cash withdrawal %, spend change %, merchant mix, engineered signals

🧱 Technology Stack

Backend: FastAPI, Uvicorn

Frontend: HTML, CSS, JavaScript

ML: scikit-learn

Charts: Chart.js

HTTP Client: Axios
## 💡 Questions?

1. **How does it work?** → `docs/PROJECT_STRUCTURE.md`
2. **How do I use the API?** → `docs/API_DOCUMENTATION.md`
3. **How do I deploy it?** → `docs/SETUP_AND_DEPLOYMENT.md`
4. **How do I add features?** → `docs/DEVELOPER_GUIDE.md`


## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 3, 2025 | Initial comprehensive framework |

---

## ✅ Deliverables Checklist

- ✅ **Analytical Framework**: 8-section Jupyter notebook with complete analysis
- ✅ **Problem Narrative**: Clear articulation of business challenge
- ✅ **Signal Framework**: 5 engineered behavioral indicators with effectiveness metrics
- ✅ **Risk Segmentation**: 3-tier customer classification (HIGH/MEDIUM/LOW)
- ✅ **Intervention Strategy**: Tier-specific action plans with expected impact
- ✅ **Financial Model**: ROI analysis showing 3,850% return
- ✅ **Implementation Roadmap**: 12-week deployment plan with 4 phases
- ✅ **Operational Guide**: Technical reference for data engineering & operations
- ✅ **Executive Summary**: Business case for stakeholder approval
- ✅ **Documentation**: Complete narrative covering all aspects

