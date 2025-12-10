# Project Structure Guide

## Overview
This project follows a **modular, scalable architecture** with clear separation of concerns. The structure is designed for:
- **Easy maintenance** - Each component has a single responsibility
- **Scalability** - New features can be added without affecting existing code
- **Developer collaboration** - Clear folder organization helps multiple developers understand the codebase
- **Testability** - Decoupled modules are easier to test

---

## Folder Structure

```
credit_card_delinquency_watch/
├── backend/                          # Backend application
│   ├── app/                         # Main application package
│   │   ├── __init__.py             # Package initialization
│   │   ├── main.py                 # App creation & startup
│   │   ├── services.py             # Business logic layer
│   │   ├── core/                   # Core modules
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Configuration & constants
│   │   │   ├── data_loader.py      # Data loading & preprocessing
│   │   │   └── model_trainer.py    # ML model training
│   │   ├── models/                 # Pydantic data models
│   │   │   └── __init__.py         # API request/response schemas
│   │   └── api/                    # API routes
│   │       ├── __init__.py
│   │       └── routes.py           # API endpoints
│   └── data/                        # Data files (CSV)
│
├── frontend/                         # Frontend application
│   └── public/
│       └── index.html              # Interactive dashboard
│
├── docs/                            # Documentation
│   └── (detailed guides here)
│
├── run.py                           # Entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project overview
└── Early_Risk_Signals_Analysis.ipynb # Analysis notebook
```

---

## Component Descriptions

### Backend Architecture

#### `backend/app/core/` - Core Modules
**Purpose**: Handle data and model operations

- **config.py**: 
  - Centralized configuration management
  - All thresholds, costs, and parameters in one place
  - Makes tuning values easy (no hunting through code)

- **data_loader.py**: 
  - Loads CSV data
  - Engineers 5 behavioral risk signals
  - Calculates risk scores
  - Creates target variable

- **model_trainer.py**: 
  - Gradient Boosting model training
  - Feature importance analysis
  - Probability predictions

#### `backend/app/api/` - API Layer
**Purpose**: Handle HTTP requests/responses

- **routes.py**: 
  - 8 REST endpoints for portfolio analysis
  - Customer scoring
  - ROI calculations
  - Dashboard data

#### `backend/app/models/` - Data Schemas
**Purpose**: Input/output validation

- Pydantic models for type safety
- Automatic API documentation
- Data validation

#### `backend/app/services.py` - Business Logic
**Purpose**: Core business operations

- **RiskScoringService**: Portfolio & signal analysis
- **InterventionService**: Cost & ROI calculations
- **CustomerService**: Individual customer scoring

#### `backend/app/main.py` - Application Factory
**Purpose**: Application initialization

- Creates FastAPI instance
- Initializes services on startup
- Mounts frontend
- Health check endpoint

### Frontend

#### `frontend/public/index.html`
- Interactive dashboard with 3 tabs
- Real-time charts using Chart.js
- Customer search & filtering
- Risk scoring calculator
- Responsive design

### Entry Point

#### `run.py`
- Simple entry point: `python run.py`
- Alternative: `uvicorn backend.app:app --reload`

---

## Data Flow

```
1. START (run.py)
   ↓
2. CREATE APP (main.py)
   ↓
3. LOAD DATA (data_loader.py)
   - Load CSV
   - Engineer signals
   - Calculate risk scores
   ↓
4. TRAIN MODEL (model_trainer.py)
   - Gradient Boosting
   - Feature importance
   ↓
5. INITIALIZE SERVICES (services.py)
   - RiskScoringService
   - InterventionService
   - CustomerService
   ↓
6. MOUNT ROUTES (routes.py)
   - 8 API endpoints active
   ↓
7. FRONTEND LOADED
   - Dashboard ready
   - Real-time data from API
```

---

## Design Principles

### 1. **Separation of Concerns**
- Data operations → `data_loader.py`
- ML operations → `model_trainer.py`
- Business logic → `services.py`
- HTTP handling → `routes.py`

### 2. **Configuration Management**
- All hardcoded values in `config.py`
- Easy to adjust thresholds without touching logic
- Single source of truth

### 3. **Dependency Injection**
- Services initialized in `main.py`
- Passed to routes
- Decouples components
- Easier testing

### 4. **Type Safety**
- Pydantic models for validation
- Type hints throughout
- Better IDE support
- Automatic API docs

### 5. **Minimal Files**
- No unnecessary abstractions
- ~10 core Python files
- Clean, readable code
- Easy to navigate

---

## Adding New Features

### Add a New Signal

1. **Define thresholds** in `config.py`
   ```python
   NEW_SIGNAL_THRESHOLD = 0.5
   ```

2. **Engineer signal** in `data_loader.py`
   ```python
   df_features['signal_new'] = (df_features['column'] > NEW_SIGNAL_THRESHOLD).astype(int)
   signal_cols.append('signal_new')
   ```

3. **Done!** Risk scores auto-update

### Add a New API Endpoint

1. **Add function** in `services.py`
   ```python
   def new_analysis(self) -> Dict:
       return {...}
   ```

2. **Add route** in `routes.py`
   ```python
   @router.get("/new-endpoint")
   async def new_endpoint():
       return risk_service.new_analysis()
   ```

3. **Add to dashboard** in `frontend/public/index.html`

---

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | FastAPI | Fast, modern API framework |
| ML | scikit-learn | Gradient Boosting model |
| Data | pandas, numpy | Data processing |
| Frontend | HTML/CSS/JS | Interactive dashboard |
| Charts | Chart.js | Data visualization |
| HTTP | axios | Frontend API calls |

---

## Environment Variables
None required! All configuration is in `config.py`

---

## Files Modified vs Created

**Kept:**
- `cc_deliquency.csv` → moved to `backend/data/`
- `Early_Risk_Signals_Analysis.ipynb` → kept at root for reference
- `requirements.txt` → reused, no changes

**Created:**
- 10 new Python modules (backend structure)
- 1 new frontend file (responsive dashboard)
- Documentation (this guide + others)

**Removed:**
- `app.py` (replaced by modular structure)
- `index.html` (moved to `frontend/public/`)

---

## Next Steps for Developers

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run application**: `python run.py`
3. **Access dashboard**: http://localhost:8000
4. **Add features**: Follow patterns in existing modules
5. **Update config**: Modify `backend/app/core/config.py`
6. **Extend API**: Add methods in `services.py`, routes in `routes.py`

---

*For detailed setup, deployment, and API documentation, see other guides.*
