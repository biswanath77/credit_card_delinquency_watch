 # Early Risk Signals – Credit Card Delinquency Watch System

A lightweight, modular system that identifies **early behavioral signals** of credit card delinquency using engineered features and a machine learning model.  
The project includes a **FastAPI backend**, **ML scoring engine**, and an interactive **frontend dashboard**.

---

## ⭐ Key Features
- Early-warning indicators (utilization, spending decline, payment ratio, cash withdrawals)
- ML-based 3-class delinquency prediction (Clean, Early Risk, High Risk)
- Real-time scoring API (FastAPI)
- Interactive dashboard for customer insights & risk visualization
- Clean, modular folder structure for easy development

---
## 🌐 Live Deployment
- The Early Risk Signals – Credit Card Delinquency Watch System is live and accessible online:
## 👉 https://credit-card-delinquency-watch.onrender.com/
**Note: Please wait for a moment for the website to load properly if loading for the first time.**

What You Can Do on the Live App

- View Dashboard Analytics
  Risk tier distribution, delinquency insights, and system-level stats.

- Explore Customers
  Search, filter, and inspect customer-level risk details.

- Use the Scoring Tool
  Input behavioral indicators and generate real-time risk scores, probability estimates, and early warning signal explanations.

---
## 📘 Documentation Index
- **Project Documentation:**	docs/Credit_Card_Delinquency_Watch_Documentation.pdf
- API usage:	docs/API_DOCUMENTATION.md
- Deployment guide:	docs/SETUP_AND_DEPLOYMENT.md
- Developer guide:	docs/DEVELOPER_GUIDE.md
  
---

## 📁 Project Structure
```
credit_card_delinquency_watch/
├── backend/
│ ├── app/ # API, services, scoring engine, ML model loader
│ ├── data/ # Raw dataset and processed files
│ └── main.py # FastAPI entry point
│
├── frontend/
│ └── public/index.html # Dashboard UI (HTML/CSS/JS)
│
├── docs/ # Additional documentation 
├── notebooks/ # Jupyter notebooks (EDA, training)
├── screenshots/ # Snapshots images 
├── run.py # Application launcher
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

```
---
## 🚀 Quick Start
```
1. Create Virtual Environment
python -m venv .venv
2. Activate Environment
Windows:
.venv\Scripts\activate
macOS / Linux:
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Application
python run.py

5. Access System
Dashboard → http://localhost:8000

API Docs → http://localhost:8000/docs
```
---
## 🧠 Core Machine Learning Model
```
Algorithm: Gradient Boosting Classifier
Classes:

0 – Clean

1 – Early Delinquency

2 – High Delinquency

🔌 Core API Endpoints
Endpoint	Method	Description
/api/v1/score-customer	POST	Score a single customer
/api/v1/customers	GET	Fetch all customers with risk tiers
/api/v1/risk-distribution	GET	Returns dataset-level risk distribution
/api/v1/signals	GET	Returns behavioral signal breakdown

```
---
## 🐳 Docker Deployment
```
Build Start Docker:
docker compose up --build

Stop and Remove:
docker compose down
```
---

##  🧱 Technology Stack
```
Backend: FastAPI, Uvicorn

Frontend: HTML, CSS, JavaScript

ML: scikit-learn

Visualization: Chart.js

Deployment: Docker / Docker Compose
```
---
##  📝 Version History
```
Version	Date	Changes
v1.0	Dec 2025	Initial release with complete backend, ML model, and dashboard
```
---

## 📌 Notes for Developers
```
Modify thresholds in:
backend/app/core/config.py

Add new features/signals in:
backend/app/services/feature_engineering.py

Retrain the model using notebooks in:
notebooks/
