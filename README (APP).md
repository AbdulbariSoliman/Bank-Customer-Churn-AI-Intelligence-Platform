
# 🏦 Bank Customer Churn Prediction App

**A production-ready Streamlit intelligence dashboard for retail banking churn risk management**

Built on top of a trained Random Forest model, this app transforms raw customer data into actionable retention intelligence — giving analysts, risk teams, and executives a single interface to assess, filter, simulate, and export churn risk across an entire portfolio.

---

## 🚀 What This App Does

The app operates in two modes and provides four core capabilities:

| Capability | Description |
|---|---|
| **Portfolio Risk Dashboard** | Filter and assess churn risk across a full customer base with live KPIs |
| **Single Customer Assessment** | Run an AI prediction on any individual customer profile in real time |
| **What-If Simulation & ROI** | Model the financial impact of a retention campaign before committing budget |
| **AI Interpretability Panel** | Inspect model feature importances and the full probability distribution |

---

## 🗂️ Project Structure

```
├── app.py                                          # Main Streamlit application
├── models/
│   ├── churn_model.pkl                             # Trained Random Forest classifier
│   ├── scaler.pkl                                  # Feature scaler (StandardScaler)
│   └── threshold.pkl                               # Optimised classification threshold
└── data/
    └── processed/
        └── Bank_Churn_Final_With_NumericClusters.csv   # Demo dataset
```

> ⚠️ The app will halt at startup if any file inside `/models` is missing.

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-folder>
```

**2. Install dependencies**
```bash
pip install streamlit pandas numpy joblib matplotlib seaborn scikit-learn
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## 🖥️ Dashboard Modes

### Internal Demo Mode
Loads the processed dataset automatically from `data/processed/`. Use this to explore the full feature set before connecting your own data.

### Client Upload Mode
Upload any customer CSV file for batch analysis. The app uses a flexible **column alias resolver** that accepts non-standard column names and maps them automatically to the expected schema.

A downloadable **CSV template** is available in the sidebar to guide data formatting.

**Expected columns:**
```
CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure,
Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
```

---

## 🤖 Model & Feature Engineering

The app applies the following feature engineering pipeline on every prediction (batch or individual):

| Feature | Formula | Business Meaning |
|---|---|---|
| `ProductPerYear` | `NumOfProducts / (Tenure + 0.1)` | Engagement depth over customer lifetime |
| `balance_to_income` | `Balance / (EstimatedSalary + 1)` | Proportion of personal wealth held at the bank |
| `income_v_product` | `EstimatedSalary / (NumOfProducts + 1)` | Revenue efficiency relative to product usage |

The model then returns a **churn probability score (0–1)**, which is bucketed into four AI verdicts:

| Score Range | Verdict |
|---|---|
| < 0.30 | 🟢 Stay (Safe) |
| 0.30 – 0.49 | 🟡 Likely Stay |
| 0.50 – 0.79 | 🟠 Likely Leave |
| ≥ 0.80 | 🔴 Highly Leave (Churn) |

---

## 📊 Dashboard Sections

### Global Portfolio Search & Filters
Filter the entire customer portfolio by geography, age range, balance range, and AI risk verdict simultaneously.

### KPI Strip
Four live metrics update with every filter change:
- **💰 Exposure** — Total balance at risk (customers above the churn threshold)
- **📉 Risk Avg** — Mean churn probability across the filtered portfolio
- **🚨 Critical Alerts** — Count of customers with churn probability ≥ 0.80
- **🤖 AI Health** — Model confidence indicator

### 👤 Single Customer AI Assessment
Enter any customer's profile manually and run a real-time prediction. Results include the AI verdict, churn probability percentage, a full feature breakdown table, and a one-click CSV export.

### 💰 What-If Simulation & ROI
Define a target customer segment (by age and balance bracket), set a cost-per-customer and a campaign effectiveness percentage, and the simulator returns:
- Estimated capital that would be saved
- Total campaign cost
- Net ROI

A risk distribution chart visualises the probability spread of the targeted segment. Results are exportable as a CSV financial report.

### 🧠 AI Brain Health & Interpretability
- **Feature Impact Chart** — Horizontal bar chart of Random Forest feature importances, exportable as CSV
- **Probability Distribution** — Histogram + KDE of churn scores across the full dataset, exportable as a master batch report

---

## 📥 Exports Available

| Export | File | Trigger Location |
|---|---|---|
| Individual customer profile | `individual_assessment.csv` | Single Customer Assessment |
| Financial simulation report | `roi_simulation_report.csv` | What-If Simulation |
| Model feature importances | `ai_model_logic.csv` | AI Brain Health panel |
| Full filtered batch report | `master_churn_report.csv` | AI Brain Health panel |

---

## 💡 Executive Summary

The model identifies **Age** and **Product engagement** as the strongest churn predictors. Targeted campaigns for customers aged **30–50** with high balances consistently show the highest potential ROI when modelled through the simulation panel.
