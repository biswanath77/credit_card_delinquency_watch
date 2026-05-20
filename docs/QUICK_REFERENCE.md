# 🎯 Quick Reference Guide

## Folder Structure at a Glance

```
📦 credit_card_delinquency_watch/
│
├─ 🎨 frontend/
│  └─ public/
│     └─ index.html              ← Dashboard (Charts, Customer List, Scoring)
│
├─ 🔧 backend/
│  ├─ app/
│  │  ├─ core/
│  │  │  ├─ config.py           ← All settings & thresholds
│  │  │  ├─ data_loader.py      ← Load CSV & engineer signals
│  │  │  └─ model_trainer.py    ← Train Gradient Boosting model
│  │  │
│  │  ├─ api/
│  │  │  └─ routes.py           ← 8 API endpoints
│  │  │
│  │  ├─ models/
│  │  │  └─ __init__.py         ← Request/response schemas
│  │  │
│  │  ├─ services.py            ← Business logic (Scoring, ROI, etc)
│  │  └─ main.py                ← App startup & initialization
│  │
│  └─ data/
│     └─ cc_deliquency.csv       ← Customer data
│
├─ 📚 docs/
│  ├─ PROJECT_STRUCTURE.md       ← Architecture & design
│  ├─ API_DOCUMENTATION.md       ← All endpoints with examples
│  ├─ SETUP_AND_DEPLOYMENT.md    ← How to run & deploy
│  ├─ DEVELOPER_GUIDE.md         ← How to add features
│  └─ RESTRUCTURING_SUMMARY.md   ← This project's changes
│
├─ ▶️ run.py                      ← Start here: python run.py
├─ 📋 requirements.txt            ← Dependencies
└─ 📖 README.md                  ← Project overview
```

---

## 🚀 Getting Started (Copy-Paste)

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python run.py

# 5. Open browser
# http://localhost:8000
```

---

## 📊 Dashboard at a Glance

### Tab 1: 📊 Dashboard
- Total customers
- Delinquent accounts count
- Risk tier breakdown (HIGH, MEDIUM, LOW)
- Risk score distribution chart
- Tier distribution chart

### Tab 2: 👥 Customers
- Search by customer ID
- Filter by risk tier
- View full customer list
- See delinquency status

### Tab 3: 🔧 Scoring Tool
- Input customer metrics
- Calculate risk score
- Get delinquency probability
- View intervention recommendations

---

## 🔌 API Quick Reference

```bash
# Portfolio summary
curl http://localhost:8000/api/v1/portfolio-summary

# Get all signals
curl http://localhost:8000/api/v1/signals

# List customers (filter by tier)
curl "http://localhost:8000/api/v1/customers?tier=HIGH"

# Score a customer (POST)
curl -X POST http://localhost:8000/api/v1/score-customer \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"C001","Utilisation %":75,...}'

# ROI analysis
curl http://localhost:8000/api/v1/intervention-roi

# Full API docs
http://localhost:8000/docs
```

---

## 🧠 5 Risk Signals

| Signal | Condition | Meaning |
|--------|-----------|---------|
| Spend Decline | Recent spend < -10% | Less spending ability |
| High Utilization | Utilization > 80% | Financial stress |
| Payment Decline | Payment ratio < 40% | Can't pay minimum |
| Cash Surge | Cash withdrawal > 15% | Need for liquidity |
| Low Merchant Mix | Diversity < 0.4 | Reduced spending |

**Risk Score = # of triggered signals**
- 3+ signals → HIGH RISK (45% delinquency)
- 2 signals → MEDIUM RISK (18% delinquency)
- ≤1 signal → LOW RISK (2% delinquency)

---

## 🔧 Common Tasks

### Change Risk Threshold
**File**: `backend/app/core/config.py`
```python
RISK_HIGH_THRESHOLD = 2  # Change from 3
```

### Adjust Signal Detection
**File**: `backend/app/core/config.py`
```python
SPEND_DECLINE_THRESHOLD = -15  # Change from -10
```

### Add New Endpoint
1. **Add method** in `backend/app/services.py`
2. **Add route** in `backend/app/api/routes.py`
3. **Restart app** → Test via `/docs`

### Update Dashboard
1. **Edit** `frontend/public/index.html`
2. **Add button** to navigation
3. **Add JavaScript function** to load/display
4. **Refresh browser**

---

## 📚 Documentation Map

| Need | Read This | Time |
|------|-----------|------|
| "How does it work?" | PROJECT_STRUCTURE.md | 10 min |
| "What APIs exist?" | API_DOCUMENTATION.md | 10 min |
| "How do I run it?" | SETUP_AND_DEPLOYMENT.md | 5 min |
| "How do I add features?" | DEVELOPER_GUIDE.md | 15 min |
| "What changed?" | RESTRUCTURING_SUMMARY.md | 5 min |

---

## 🚢 Deployment

### Local (Development)
```bash
python run.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### Docker
```bash
docker build -t credit-risk .
docker run -p 8000:8000 credit-risk
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Port 8000 in use" | Edit `run.py`, change port |
| "CSV not found" | Move `cc_deliquency.csv` to `backend/data/` |
| "API not responding" | Check console output, verify data loaded |

---

## 💡 Pro Tips

1. **Use FastAPI docs**: http://localhost:8000/docs
2. **Watch the logs**: Check console for errors/warnings
3. **Test with Postman**: Import and test endpoints easily
4. **Keep config.py clean**: All settings in one place
5. **Follow the patterns**: Look at existing code as examples

---

## 📞 Key Files at a Glance

### Need to...

**Add a new risk signal?**
→ `backend/app/core/config.py` + `backend/app/core/data_loader.py`

**Add a new API endpoint?**
→ `backend/app/services.py` + `backend/app/api/routes.py`

**Change risk thresholds?**
→ `backend/app/core/config.py`

**Update the dashboard?**
→ `frontend/public/index.html`

**Understand the architecture?**
→ `docs/PROJECT_STRUCTURE.md`

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Run `python run.py` without errors
- [ ] Access http://localhost:8000
- [ ] See dashboard load with data
- [ ] Click "Customers" tab, see list
- [ ] Click "Scoring Tool", enter values, click button
- [ ] Check API docs at http://localhost:8000/docs
- [ ] Try `/api/v1/portfolio-summary` endpoint

---

## 🎯 What's Inside

```
Line Count by Component:
├─ config.py              50 lines  (Configuration)
├─ data_loader.py        120 lines  (Data & Feature Engineering)
├─ model_trainer.py       80 lines  (ML Model)
├─ services.py           250 lines  (Business Logic)
├─ routes.py             100 lines  (API Endpoints)
├─ models/__init__.py     60 lines  (Schemas)
├─ main.py               100 lines  (App Setup)
└─ index.html            600 lines  (Dashboard)
─────────────────────────
  Total               ~1,350 lines  ✅ Clean & Focused!
```

---

## 🎓 Learning Path

1. **5 min**: Read this guide
2. **10 min**: Read `PROJECT_STRUCTURE.md`
3. **5 min**: Run `python run.py`
4. **10 min**: Explore dashboard
5. **10 min**: Read `API_DOCUMENTATION.md`
6. **15 min**: Read `DEVELOPER_GUIDE.md`
7. **Go!**: Try adding a feature

---

**Everything you need is documented. Start exploring! 🚀**

---

*Last Updated: December 2025*
