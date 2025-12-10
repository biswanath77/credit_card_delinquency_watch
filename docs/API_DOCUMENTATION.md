# API Endpoint Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "data_loaded": true,
  "model_trained": true
}
```

---

## 1. Portfolio Summary
```
GET /portfolio-summary
```

**Returns**: Overall portfolio statistics

**Response:**
```json
{
  "total_customers": 100,
  "total_delinquent": 15,
  "delinquency_rate": 15.0,
  "tier_breakdown": {
    "HIGH": 20,
    "MEDIUM": 35,
    "LOW": 45
  },
  "high_risk": {
    "count": 20,
    "delinquency_rate": 45.0
  },
  "medium_risk": {
    "count": 35,
    "delinquency_rate": 18.6
  },
  "low_risk": {
    "count": 45,
    "delinquency_rate": 2.2
  }
}
```

---

## 2. Risk Signals
```
GET /signals
```

**Returns**: Analysis of each behavioral risk signal

**Response:**
```json
[
  {
    "name": "Spend Decline",
    "code": "signal_spend_decline",
    "prevalence": 25,
    "prevalence_pct": 25.0,
    "delinquency_rate_when_present": 40.0,
    "delinquency_rate_when_absent": 10.0,
    "risk_lift": 4.0
  },
  ...
]
```

---

## 3. Risk Distribution
```
GET /risk-distribution
```

**Returns**: Risk score and tier distribution with metrics

**Response:**
```json
{
  "risk_score_distribution": {
    "0": 45,
    "1": 30,
    "2": 15,
    "3": 7,
    "4": 3,
    "5": 0
  },
  "tier_distribution": [
    {
      "tier": "HIGH",
      "count": 20,
      "percentage": 20.0,
      "delinquency_rate": 45.0,
      "avg_utilization": 82.5,
      "avg_payment_ratio": 35.2,
      "avg_spend_change": -8.5,
      "avg_cash_withdrawal": 18.5
    },
    ...
  ]
}
```

---

## 4. Score Customer (Individual)
```
POST /score-customer
```

**Request:**
```json
{
  "customer_id": "C001",
  "Utilisation %": 75.5,
  "Avg Payment Ratio": 45.0,
  "Min Due Paid Frequency": 35.0,
  "Merchant Mix Index": 0.6,
  "Cash Withdrawal %": 12.5,
  "Recent Spend Change %": -5.0,
  "signal_spend_decline": 0,
  "signal_high_utilization": 0,
  "signal_payment_decline": 0,
  "signal_cash_surge": 0,
  "signal_low_merchant_mix": 0
}
```

**Response:**
```json
{
  "customer_id": "C001",
  "risk_score": 2,
  "risk_tier": "MEDIUM",
  "delinquency_probability": 0.235,
  "triggered_signals": [
    "High Utilization"
  ],
  "recommendations": [
    "Automated email with account health summary",
    "Offer payment flexibility or rate reduction",
    "Push financial wellness resources",
    "Monitor monthly for 2 months"
  ],
  "confidence": 0.53
}
```

---

## 5. Get Customers List
```
GET /customers?tier=HIGH&limit=20
```

**Query Parameters:**
- `tier` (optional): HIGH, MEDIUM, LOW
- `limit` (optional, max 100): Number of customers to return

**Response:**
```json
[
  {
    "customer_id": "C001",
    "risk_tier": "HIGH",
    "risk_score": 3,
    "utilization": 85.2,
    "payment_ratio": 32.5,
    "spend_change": -12.5,
    "is_delinquent": true,
    "credit_limit": 50000
  },
  ...
]
```

---

## 6. Feature Importance
```
GET /feature-importance
```

**Returns**: Top 10 most important features for prediction

**Response:**
```json
[
  {
    "Feature": "signal_high_utilization",
    "Importance": 0.25
  },
  {
    "Feature": "Avg Payment Ratio",
    "Importance": 0.18
  },
  ...
]
```

---

## 7. Intervention ROI
```
GET /intervention-roi
```

**Returns**: Cost and ROI analysis for intervention strategy

**Response:**
```json
{
  "program_cost": {
    "high_tier": 400.0,
    "medium_tier": 262.5,
    "low_tier": 22.5,
    "total": 685.0
  },
  "prevented_defaults": 12.5,
  "revenue_protected": 62500.0,
  "net_benefit": 61815.0,
  "roi_percentage": 9023.0,
  "per_dollar_yield": 91.2
}
```

---

## 8. Dashboard Stats (All-in-One)
```
GET /dashboard-stats
```

**Returns**: Combined portfolio summary, ROI, and top signals

**Response:**
```json
{
  "portfolio": { ... },
  "roi": { ... },
  "top_signals": [
    { signal 1 },
    { signal 2 },
    { signal 3 }
  ]
}
```

---

## Error Responses

All errors return appropriate HTTP status codes:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Not found
- `500` - Server error

---

## Rate Limiting
No rate limiting currently implemented. For production, add rate limiting via FastAPI middleware.

---

## Authentication
No authentication currently implemented. For production, add JWT or OAuth2 via FastAPI security.

---

## CORS
Currently allows all origins. Update in `backend/app/main.py` for production:

```python
allow_origins=["https://yourdomain.com"]
```

---

## Testing the API

### Using cURL
```bash
curl http://localhost:8000/api/v1/portfolio-summary
```

### Using Python Requests
```python
import requests

response = requests.get('http://localhost:8000/api/v1/portfolio-summary')
print(response.json())
```

### Using Postman
Import the base URL and create requests for each endpoint.

---

## WebSocket (Future Enhancement)
Currently using REST. For real-time updates, consider adding WebSocket support:
- Push updates when new data arrives
- Real-time dashboard refresh
- Alert notifications

---

*Last Updated: December 2025*
