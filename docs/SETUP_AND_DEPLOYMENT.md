# Setup & Deployment Guide

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (optional)
- Virtual environment (recommended)

---

## Local Development Setup

### 1. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
pip list
```

Should show: fastapi, uvicorn, pandas, scikit-learn, pydantic, numpy

---

## Running the Application

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Using Uvicorn
```bash
uvicorn backend.app:app --reload
```

### Option 3: Production (no auto-reload)
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

---

## Access the Application

**Frontend Dashboard:** http://localhost:8000

**API Documentation (Swagger):** http://localhost:8000/docs

**API Documentation (ReDoc):** http://localhost:8000/redoc

**Health Check:** http://localhost:8000/health

---

## Data File Requirements

The application expects `cc_deliquency.csv` in `backend/data/` folder.

**Required columns:**
- Customer ID
- DPD Bucket Next Month
- Recent Spend Change %
- Utilisation %
- Cash Withdrawal %
- Avg Payment Ratio
- Min Due Paid Frequency
- Merchant Mix Index
- Credit Limit

**Current file:** Included in `backend/data/`

---

## Configuration

Edit `backend/app/core/config.py` to adjust:

- **Risk Thresholds**: RISK_HIGH_THRESHOLD, RISK_MEDIUM_THRESHOLD
- **Signal Detection**: Spend decline %, utilization %, cash withdrawal %, etc.
- **Intervention Costs**: Cost per tier intervention
- **Model Parameters**: Learning rate, number of estimators
- **API Settings**: API version, title, CORS origins

Example: Change high-risk threshold from 3 to 2
```python
RISK_HIGH_THRESHOLD = 2  # Changed from 3
```

Re-run application → new threshold applies

---

## Troubleshooting

### Issue: "Module not found: fastapi"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: "CSV file not found"
**Solution**: Ensure `cc_deliquency.csv` is in `backend/data/` folder
```bash
# File path should be: backend/data/cc_deliquency.csv
```

### Issue: "Port 8000 already in use"
**Solution**: Use different port
```bash
python run.py  # Edit run.py to change port (default 8000)
# OR
uvicorn backend.app:app --port 8001
```

### Issue: "CORS error from frontend"
**Solution**: Check CORS configuration in `backend/app/main.py`
```python
allow_origins=["*"]  # Allow all (dev only!)
```

### Issue: Model fails to train
**Solution**: Check data quality
- Ensure CSV columns match config
- Check for missing values
- Verify data types

---

## Performance Optimization

### 1. Model Caching
Currently retrains on every restart. For large datasets:
```python
# In model_trainer.py
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(gb_model, f)
```

### 2. Data Caching
Cache processed data:
```python
# In data_loader.py
df.to_pickle('data_cache.pkl')
df = pd.read_pickle('data_cache.pkl')
```

### 3. Database
For production, replace CSV with database:
- PostgreSQL, MySQL, or MongoDB
- Use SQLAlchemy ORM
- Connection pooling

---

## Production Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0"]
```

Run:
```bash
docker build -t credit-risk .
docker run -p 8000:8000 credit-risk
```

### Using Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/backend/data
```

Run:
```bash
docker-compose up
```

---

## Environment Variables (Production)

Add to `.env` file:
```
ENV=production
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
```

Load in `backend/app/core/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv('ENV', 'development')
```

---

## Logging

Add logging in `backend/app/main.py`:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.error("Error occurred")
```

---

## Monitoring & Alerts

For production monitoring:
1. **Application Monitoring**: New Relic, DataDog
2. **Error Tracking**: Sentry
3. **Performance**: AWS CloudWatch
4. **Uptime**: UptimeRobot

---

## Security Checklist

- [ ] Add authentication (JWT, OAuth2)
- [ ] Add rate limiting
- [ ] Enable HTTPS/SSL
- [ ] Validate all inputs
- [ ] Sanitize API responses
- [ ] Use environment variables for secrets
- [ ] Regular security audits
- [ ] Keep dependencies updated

---

## Backup & Disaster Recovery

1. **Data Backup**:
   ```bash
   # Daily backup to cloud storage
   aws s3 cp backend/data/cc_deliquency.csv s3://my-bucket/backup/
   ```

2. **Model Backup**:
   ```bash
   # Save trained model
   pickle.dump(model, open('model_backup.pkl', 'wb'))
   ```

3. **Code Backup**: Use Git with remote repository

---

## CI/CD Pipeline

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest
      - run: python -m black --check .
```

---

## Useful Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install safety
safety check

# Code formatting
pip install black
black backend/

# Linting
pip install pylint
pylint backend/
```

---

## System Requirements

**Minimum:**
- RAM: 512 MB
- CPU: 1 core
- Disk: 500 MB

**Recommended (Production):**
- RAM: 2 GB+
- CPU: 2+ cores
- Disk: 10 GB+
- Fast SSD for data

---

## Support & Troubleshooting

For issues:
1. Check logs: `backend/logs/app.log`
2. Test health endpoint: `/health`
3. Verify data: `backend/data/cc_deliquency.csv`
4. Check configuration: `backend/app/core/config.py`

---

*Last Updated: December 2025*
