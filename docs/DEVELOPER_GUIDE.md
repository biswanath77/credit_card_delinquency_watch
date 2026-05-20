# Developer Guide

## For New Team Members

Welcome! This guide will help you understand and extend the Early Risk Signals system.

---

## Quick Start (5 minutes)

1. **Setup environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Start application**
   ```bash
   python run.py
   ```

3. **Visit dashboard**
   Open http://localhost:8000

---

## Code Organization

### Three Main Layers

```
FRONTEND (HTML/CSS/JS)
    ↓
ROUTES (FastAPI endpoints)
    ↓
SERVICES (Business logic)
    ↓
CORE (Data & ML models)
```

### Data Flow Example: Scoring a Customer

```
1. Frontend sends POST /score-customer
   ↓
2. Route handler in routes.py receives request
   ↓
3. Calls customer_service.score_customer()
   ↓
4. Service calculates risk score using signals
   ↓
5. Calls model_trainer.predict_proba()
   ↓
6. Returns JSON with recommendations
   ↓
7. Frontend displays results
```

---

## Common Tasks

### Task 1: Add a New Risk Signal

**Goal**: Detect if customer has unusual transaction frequency

**Step 1**: Add threshold to `config.py`
```python
# backend/app/core/config.py
TRANSACTION_FREQUENCY_THRESHOLD = 10  # Low activity
```

**Step 2**: Engineer signal in `data_loader.py`
```python
# In DataLoader.engineer_signals() method
df_features['signal_low_transaction_freq'] = (
    df_features['Monthly Transactions'] < TRANSACTION_FREQUENCY_THRESHOLD
).astype(int)
signal_cols.append('signal_low_transaction_freq')
```

**Step 3**: Update risk score calculation
- Automatic! The signal is included in `signal_cols`
- Risk scores recalculate on restart

**Step 4**: Test via API
```bash
GET /api/v1/signals
```

### Task 2: Adjust Risk Thresholds

**Change when customer is "HIGH RISK"** from 3+ signals to 2+ signals

**File**: `backend/app/core/config.py`
```python
RISK_HIGH_THRESHOLD = 2  # Was 3
```

**Impact**: Automatic ✓
- Risk tier recalculates
- Portfolio summary updates
- ROI analysis adjusts

### Task 3: Add New API Endpoint

**Goal**: Get risk distribution by age group

**Step 1**: Add method in `services.py`
```python
# In RiskScoringService class
def get_risk_by_age_group(self) -> Dict:
    """Analyze risk distribution by customer age"""
    age_groups = {
        '18-25': self.df[(self.df['Age'] >= 18) & (self.df['Age'] < 25)],
        '26-35': self.df[(self.df['Age'] >= 26) & (self.df['Age'] < 35)],
        # ... more groups
    }
    
    result = {}
    for group_name, group_data in age_groups.items():
        result[group_name] = {
            'count': len(group_data),
            'high_risk_pct': (group_data['risk_tier'] == 'HIGH').sum() / len(group_data) * 100,
            'avg_delinquency_rate': group_data['is_delinquent'].mean() * 100
        }
    return result
```

**Step 2**: Add route in `routes.py`
```python
@router.get("/risk-by-age-group")
async def risk_by_age_group():
    """Get risk distribution by age group"""
    return risk_service.get_risk_by_age_group()
```

**Step 3**: Test
```bash
curl http://localhost:8000/api/v1/risk-by-age-group
```

### Task 4: Update Frontend Dashboard

**Goal**: Add ROI chart to dashboard

**File**: `frontend/public/index.html`

**Step 1**: Add button to navigation
```html
<button class="nav-btn" onclick="showSection('roi')">💰 ROI Analysis</button>
```

**Step 2**: Add section HTML
```html
<div id="roi" class="section">
    <div class="stats-grid" id="roiStats"></div>
    <div class="chart-container">
        <h2>ROI by Risk Tier</h2>
        <div class="chart-wrapper">
            <canvas id="roiChart"></canvas>
        </div>
    </div>
</div>
```

**Step 3**: Add JavaScript functions
```javascript
async function loadROI() {
    const response = await axios.get(`${API_BASE}/intervention-roi`);
    // Update statsGrid
    // Create roiChart
}
```

---

## Testing

### Unit Testing Example

Create `backend/tests/test_services.py`:
```python
import pytest
from backend.app.services import RiskScoringService

def test_portfolio_summary():
    # Create mock data
    df = pd.DataFrame({...})
    service = RiskScoringService(df, signal_cols=['signal_1', 'signal_2'])
    
    # Test
    result = service.get_portfolio_summary()
    
    # Assert
    assert result['total_customers'] > 0
    assert 'tier_breakdown' in result
```

Run tests:
```bash
pip install pytest
pytest backend/tests/
```

---

## Debugging

### Enable Debug Logging

Add to `backend/app/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.debug(f"Loading {len(app.state.df)} records")
    logger.debug(f"Signals: {app.state.signal_cols}")
```

### Inspect Data in Python

```python
import pandas as pd
df = pd.read_csv('backend/data/cc_deliquency.csv')
print(df.head())
print(df.info())
print(df.describe())
```

### Check API Response

```python
import requests
import json

response = requests.get('http://localhost:8000/api/v1/portfolio-summary')
data = response.json()
print(json.dumps(data, indent=2))
```

---

## Performance Tips

### 1. Cache Expensive Operations

```python
# In services.py
from functools import lru_cache

class RiskScoringService:
    @lru_cache(maxsize=1)
    def get_portfolio_summary(self):
        # Expensive calculation
        return {...}
```

### 2. Use Vectorized Operations

```python
# ❌ SLOW - Loop
for i in range(len(df)):
    df.loc[i, 'risk_score'] = sum(df.loc[i, signals])

# ✅ FAST - Vectorized
df['risk_score'] = df[signals].sum(axis=1)
```

### 3. Profile Code

```bash
pip install line_profiler
kernprof -l -v backend/app/services.py
```

---

## Code Style

### Follow PEP 8
```bash
pip install black pylint
black backend/  # Auto-format
pylint backend/  # Check style
```

### Type Hints
```python
# ❌ No hints
def score_customer(data):
    return {...}

# ✅ With hints
from typing import Dict, List
def score_customer(data: Dict) -> Dict:
    return {...}
```

### Docstrings
```python
def engineer_signals(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Engineer behavioral risk signals
    
    Args:
        df: Input DataFrame with customer data
    
    Returns:
        Tuple of (DataFrame with signals, list of signal names)
    
    Example:
        >>> df, signals = engineer_signals(raw_df)
        >>> print(len(signals))
        5
    """
```

---

## Git Workflow

### Branch Naming
```bash
git checkout -b feature/add-age-signal
git checkout -b bugfix/fix-roi-calculation
git checkout -b docs/update-api-guide
```

### Commit Messages
```bash
# Good
git commit -m "Add transaction frequency signal to risk detection"

# Bad
git commit -m "updated stuff"
```

### Pull Request Template
```
## Description
What changes does this PR introduce?

## Related Issues
Closes #123

## Testing
How was this tested?

## Screenshots
(if applicable)
```

---

## Deployment Checklist

Before deploying to production:

- [ ] All tests pass: `pytest`
- [ ] No linting errors: `pylint backend/`
- [ ] Code formatted: `black backend/`
- [ ] API documented: All endpoints have docstrings
- [ ] Security check: `safety check`
- [ ] Dependencies updated: `pip list`
- [ ] `.env` configured: All secrets in environment
- [ ] CORS configured: Production domain only
- [ ] Logging enabled: Check logs in production
- [ ] Monitoring set up: Error tracking, performance monitoring
- [ ] Backup configured: Data backed up regularly

---

## Common Mistakes to Avoid

❌ **Don't:**
- Hardcode values (put in `config.py`)
- Skip type hints
- Modify global state
- Leave print statements in code
- Commit secrets to git

✅ **Do:**
- Use configuration files
- Add type hints
- Use dependency injection
- Use logging
- Use `.gitignore` for secrets

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pandas Docs**: https://pandas.pydata.org/
- **scikit-learn Docs**: https://scikit-learn.org/
- **Python Style Guide (PEP 8)**: https://pep8.org/

---

## Getting Help

1. Check documentation: `docs/` folder
2. Search code: Look for similar patterns
3. Read error messages carefully
4. Ask team members in team chat
5. Create GitHub issue with full context

---

*Last Updated: December 2025*
