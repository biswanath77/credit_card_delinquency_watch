// frontend/public/app.js

const API_BASE = window.API_BASE || '/api/v1';
let tierChart = null;
let scoreChart = null;

function activateNavButton(sectionId) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('btn-' + sectionId);
  if (btn) btn.classList.add('active');
}

async function showSection(sectionId, evt) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(sectionId).classList.add('active');
  activateNavButton(sectionId);

  if (sectionId === 'dashboard') {
    setTimeout(() => {
      loadDashboard();
      setTimeout(() => {
        try { if (tierChart) tierChart.resize(); } catch(e) {}
        try { if (scoreChart) scoreChart.resize(); } catch(e) {}
      }, 150);
    }, 120);
  } else if (sectionId === 'customers') {
    loadCustomers();
  } else if (sectionId === 'tools') {
    loadScoringTool();
  }
}

async function loadDashboard() {
  const statsGrid = document.getElementById('statsGrid');
  if (!statsGrid) return;
  statsGrid.innerHTML = '<div class="loading">Loading...</div>';
  try {
    const resp = await axios.get(`${API_BASE}/dashboard-stats`);
    const data = resp.data || {};
    const total_customers = data.portfolio?.total_customers ?? '—';
    const total_delinquent = data.portfolio?.total_delinquent ?? '—';
    const delinquency_rate = data.portfolio?.delinquency_rate ?? '—';
    const tier_breakdown = data.portfolio?.tier_breakdown || { HIGH: 0, MEDIUM: 0, LOW: 0 };

    const statsHTML = `
      <div class="stat-card"><h3>Total Customers</h3><div class="value">${total_customers}</div></div>
      <div class="stat-card danger"><h3>Delinquent Accounts</h3><div class="value">${total_delinquent}</div><div class="subtext">${delinquency_rate}% rate</div></div>
      <div class="stat-card warning"><h3>High Risk</h3><div class="value">${tier_breakdown.HIGH ?? 0}</div></div>
      <div class="stat-card success"><h3>Low Risk</h3><div class="value">${tier_breakdown.LOW ?? 0}</div></div>
    `;
    statsGrid.innerHTML = statsHTML;

    const tierCtx = document.getElementById('tierChart')?.getContext('2d');
    if (tierCtx) {
      if (tierChart) tierChart.destroy();
      tierChart = new Chart(tierCtx, {
        type: 'doughnut',
        data: {
          labels: ['High Risk','Medium Risk','Low Risk'],
          datasets: [{ data: [tier_breakdown.HIGH ?? 0, tier_breakdown.MEDIUM ?? 0, tier_breakdown.LOW ?? 0], backgroundColor: ['#dc2626','#f59e0b','#16a34a'] }]
        },
        options: { responsive:true, maintainAspectRatio:false }
      });
    }

    const distResp = await axios.get(`${API_BASE}/risk-distribution`);
    const scores = distResp.data?.risk_score_distribution || {};
    const labels = Object.keys(scores).sort();
    const values = labels.map(k => scores[k]);

    const scoreCtx = document.getElementById('scoreChart')?.getContext('2d');
    if (scoreCtx) {
      if (scoreChart) scoreChart.destroy();
      scoreChart = new Chart(scoreCtx, {
        type:'bar',
        data: { labels, datasets:[{ label:'Customers', data:values, backgroundColor:'#2563eb' }] },
        options:{ responsive:true, maintainAspectRatio:false, scales:{ y:{ beginAtZero:true } } }
      });
    }

    setTimeout(() => { try{ if (tierChart) tierChart.resize(); } catch(e){} try{ if (scoreChart) scoreChart.resize(); } catch(e){} }, 120);
  } catch (err) {
    console.error('Dashboard error:', err);
    const msg = err?.response?.data?.detail || err?.message || 'Network Error';
    statsGrid.innerHTML = `<div class="error">Failed to load dashboard: ${msg}</div>`;
  }
}

async function loadCustomers() {
  const container = document.getElementById('customersTable');
  if (!container) return;
  container.innerHTML = '<div class="loading">Loading customers...</div>';
  try {
    const tier = document.getElementById('tierFilter')?.value || '';
    const resp = await axios.get(`${API_BASE}/customers`, { params: { tier, limit: 50 } });
    const customers = Array.isArray(resp.data) ? resp.data : resp.data?.customers || [];

    const html = `
      <table>
        <thead><tr><th>Customer ID</th><th>Risk Tier</th><th>Risk Score</th><th>Utilization</th><th>Payment Ratio</th><th>Status</th></tr></thead>
        <tbody>
          ${customers.map(c => `
            <tr>
              <td>${c.customer_id ?? c.customerId ?? '-'}</td>
              <td><span class="risk-tier-badge ${c.risk_tier ?? '-'}">${c.risk_tier ?? '-'}</span></td>
              <td>${c.risk_score ?? '-'}</td>
              <td>${(c.utilization ?? c['Utilisation %'] ?? '-')}%</td>
              <td>${(c.payment_ratio ?? c['Avg Payment Ratio'] ?? '-')}%</td>
              <td>${c.is_delinquent ? '⚠️ Delinquent' : '✅ Current'}</td>
            </tr>`).join('')}
        </tbody>
      </table>`;
    container.innerHTML = html;
  } catch (err) {
    console.error('Customers error:', err);
    const msg = err?.response?.data?.detail || err?.message || 'Network Error';
    container.innerHTML = `<div class="error">Failed to load customers: ${msg}</div>`;
  }
}

function loadScoringTool() {
  const form = `
    <div style="display:grid; gap:15px;">
      <div><label>Customer ID</label><input type="text" id="cust_id" placeholder="e.g., C001"></div>
      <div><label>Utilisation %</label><input type="number" id="utilisation" min="0" max="100"></div>
      <div><label>Avg Payment Ratio %</label><input type="number" id="payment_ratio" min="0" max="100"></div>
      <div><label>Min Due Paid Frequency %</label><input type="number" id="due_freq" min="0" max="100"></div>
      <div><label>Merchant Mix Index (0-1)</label><input type="number" id="merchant_mix" min="0" max="1" step="0.1"></div>
      <div><label>Cash Withdrawal %</label><input type="number" id="cash_withdrawal" min="0" max="100"></div>
      <div><label>Recent Spend Change %</label><input type="number" id="spend_change" min="-100" max="100"></div>
    </div>`;
  const el = document.getElementById('scoringForm'); if (el) el.innerHTML = form;
}

async function scoreCustomer() {
  const resultEl = document.getElementById('scoringResult'); if (!resultEl) return;
  resultEl.innerHTML = '<div class="loading">Calculating...</div>';
  try {
    const utilisation = parseFloat(document.getElementById('utilisation')?.value || 0);
    const payment_ratio = parseFloat(document.getElementById('payment_ratio')?.value || 0);
    const due_freq = parseFloat(document.getElementById('due_freq')?.value || 0);
    const merchant_mix = parseFloat(document.getElementById('merchant_mix')?.value || 0);
    const cash_withdrawal = parseFloat(document.getElementById('cash_withdrawal')?.value || 0);
    const spend_change = parseFloat(document.getElementById('spend_change')?.value || 0);

    const payload = {
      customer_id: document.getElementById('cust_id')?.value || null,
      utilisation_pct: utilisation,
      avg_payment_ratio: payment_ratio,
      min_due_paid_frequency: due_freq,
      merchant_mix_index: merchant_mix,
      cash_withdrawal_pct: cash_withdrawal,
      recent_spend_change_pct: spend_change,
      signal_spend_decline: spend_change < -10 ? 1 : 0,
      signal_high_utilization: utilisation > 80 ? 1 : 0,
      signal_payment_decline: payment_ratio < 40 ? 1 : 0,
      signal_cash_surge: cash_withdrawal > 15 ? 1 : 0,
      signal_low_merchant_mix: merchant_mix < 0.4 ? 1 : 0
    };

    const resp = await axios.post(`${API_BASE}/score-customer`, payload);
    const result = resp.data || {};

    const html = `
      <div style="margin-top:30px;padding:20px;background:var(--light);border-radius:10px;">
        <h3>Assessment Results</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:20px 0;">
          <div style="background:white;padding:15px;border-radius:5px;text-align:center;">
            <div style="color:#6b7280;font-size:12px;">RISK TIER</div>
            <span class="risk-tier-badge ${result.risk_tier ?? '-'}">${result.risk_tier ?? '-'}</span>
          </div>
          <div style="background:white;padding:15px;border-radius:5px;text-align:center;">
            <div style="color:#6b7280;font-size:12px;">RISK SCORE</div>
            <div style="font-size:24px;font-weight:bold;">${result.risk_score ?? '-'}</div>
          </div>
          <div style="background:white;padding:15px;border-radius:5px;text-align:center;">
            <div style="color:#6b7280;font-size:12px;">DELINQUENCY PROB</div>
            <div style="font-size:24px;font-weight:bold;color:var(--danger);">${((result.delinquency_probability || 0)*100).toFixed(1)}%</div>
          </div>
        </div>
        ${(result.triggered_signals && result.triggered_signals.length) ? `
          <div style="background:#fee2e2;padding:15px;border-radius:5px;margin-bottom:20px;">
            <strong>Triggered Signals:</strong>
            <ul style="margin-left:20px;margin-top:10px;">
              ${result.triggered_signals.map(s => `<li>${s}</li>`).join('')}
            </ul>
          </div>` : ''}
        <div class="recommendation"><strong>Recommended Actions:</strong><ul>${(result.recommendations || []).map(r => `<li>${r}</li>`).join('')}</ul></div>
      </div>`;
    resultEl.innerHTML = html;
  } catch (err) {
    console.error('Scoring error:', err);
    const msg = err?.response?.data?.detail || err?.message || 'Network Error';
    resultEl.innerHTML = `<div class="error">Failed to score customer: ${msg}</div>`;
  }
}

// startup
window.addEventListener('load', () => {
  try { loadScoringTool(); } catch(e) {}
  setTimeout(() => {
    try {
      showSection('customers', { target: document.getElementById('btn-customers') });
      setTimeout(() => {
        showSection('dashboard', { target: document.getElementById('btn-dashboard') });
        setTimeout(() => { try { if (tierChart) tierChart.resize(); } catch(e){} try { if (scoreChart) scoreChart.resize(); } catch(e){} }, 180);
      }, 420);
    } catch (e) {
      console.warn('Auto tab flip failed, loading dashboard directly', e);
      loadDashboard();
    }
  }, 180);

  window.addEventListener('resize', () => {
    try { if (tierChart) tierChart.resize(); } catch(e) {}
    try { if (scoreChart) scoreChart.resize(); } catch(e) {}
  });
});
