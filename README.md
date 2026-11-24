# 🏦 Bank Customer Churn Intelligence Platform

> **End-to-end ML pipeline for retail banking churn prediction, customer segmentation, and retention ROI simulation**

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=flat&logo=streamlit)](https://bank-customer-data-prep-j3mmdpxvqukgq88ppncxxx.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://python.org)
[![Model](https://img.shields.io/badge/Model-Random%20Forest-4CAF50?style=flat)](https://scikit-learn.org)
[![AUC-ROC](https://img.shields.io/badge/AUC--ROC-0.8351-blue?style=flat)](https://github.com/AbdulbariSoliman/Bank-Customer-Data-Prep)

**🔗 [Open Live App →](https://bank-customer-data-prep-j3mmdpxvqukgq88ppncxxx.streamlit.app/)**

---

## 📌 Business Problem

Retail banks lose significant revenue when high-value customers silently exit. Generic retention campaigns waste budget by targeting the full portfolio indiscriminately — with no way to prioritise who matters most.

This project builds an **AI-powered decision system** that identifies which customers are most likely to churn, quantifies the financial exposure, segments the portfolio into actionable risk cohorts, and simulates the ROI of targeted retention campaigns — before a single dollar is committed.

---

## 🎯 Results at a Glance

| Metric | Value |
|---|---|
| Dataset | 10,000 customer records (Maven Analytics — Kaggle) |
| Model | Random Forest Classifier |
| AUC-ROC | **0.8351** (vs 0.7814 baseline — +6.9%) |
| Accuracy | **85.25%** (vs 81.25% baseline — +4.0%) |
| Segments | 4 K-Means risk cohorts with tailored retention strategies |
| Deployment | Live Streamlit dashboard — no coding required for business users |

---

## 🗂️ Project Structure

```
├── app.py                          # Streamlit dashboard (Part 2)
├── requirements.txt
├── notebooks/                      # ML pipeline (Part 1)
├── models/
│   ├── churn_model.pkl             # Trained Random Forest classifier
│   ├── scaler.pkl                  # Feature scaler (StandardScaler)
│   └── threshold.pkl               # Optimised classification threshold
├── data/
│   └── processed/
│       └── Bank_Churn_Final_With_NumericClusters.csv
└── outputs/
    ├── cluster_summary_unscaled.csv
    └── recommendations_final.md
```

---

---

# Part 1 — ML Pipeline & Research

> Data engineering · Feature design · Model training · Strategic segmentation

---

## 1.1 Technical Data Architecture

### Data Sanitisation

- **Currency Normalisation:** Transformed `Balance` and `EstimatedSalary` from string representations into numeric types for mathematical processing.
- **Integrity Checks:** Automated duplicate removal and median-based imputation for missing values to prevent data leakage.
- **Encoding:** Converted categorical fields (`Geography`, `Gender`) into machine-readable formats while retaining geographic business distinctions for segmentation.

### 1.2 Feature Engineering — The Alpha Features

Three financial ratios were engineered to capture customer behaviour more effectively than raw fields alone:

| Feature | Formula | Business Meaning |
|---|---|---|
| **Product Density** | `NumOfProducts / (Tenure + 0.1)` | Engagement depth relative to time with the bank |
| **Liquidity Leverage** | `Balance / (EstimatedSalary + 1)` | Proportion of personal wealth held at the bank |
| **Revenue Efficiency** | `EstimatedSalary / (NumOfProducts + 1)` | Cross-sell potential relative to current product usage |

---

## 1.3 Modelling Performance & Audit

A **Random Forest Classifier** was selected to capture non-linear relationships in customer behaviour, significantly outperforming the Logistic Regression baseline across all key metrics.

### Model Performance Benchmark

| Metric | Logistic Regression (Baseline) | Random Forest (Final) | Improvement |
|---|---|---|---|
| Accuracy | 81.25% | **85.25%** | +4.00% |
| ROC-AUC | 0.7814 | **0.8351** | +6.87% |

### Top Churn Drivers

1. **Age** — Risk peaks significantly in the **40–60** demographic. Older customers with single-product holdings are the highest-risk cohort.
2. **Product Count** — Churn rate drops sharply from 1 to 2 products, confirming cross-selling as the single most effective retention lever.
3. **Revenue Efficiency** — Customers whose salary far exceeds their product engagement are consistently under-served and at high risk of exit.

---

## 1.4 Strategic Segmentation — K-Means Clustering

K-Means Clustering was applied to move the analysis from general predictions to targeted interventions, categorising the full portfolio into four actionable risk segments.

### Risk Hierarchy & Retention Recommendations

| Cluster | Customer Profile | Recommended Strategy | Risk Level |
|---|---|---|---|
| **Cluster 0** | High Balance / High Salary | **VIP Retention** — Cross-sell a second product immediately to secure assets | 🔴 Critical |
| **Cluster 2** | High Balance / Low Salary | **Debt Stabilisation** — Offer financial counselling or consolidation products | 🟠 High |
| **Cluster 1** | Low Tenure / High Products | **Onboarding Support** — High-touch service to retain customers through Year 1 | 🟡 Moderate |
| **Cluster 3** | High Tenure / Low Balance | **Loyalty Maintenance** — Low-cost rewards programme for a stable, long-term base | 🟢 Stable |

---

## 1.5 Pipeline Outputs

| File | Description |
|---|---|
| `Bank_Churn_Final_With_NumericClusters.csv` | Master dataset — used directly as the app's demo data source |
| `cluster_summary_unscaled.csv` | Non-technical segment summary for stakeholder presentations |
| `recommendations_final.md` | Strategic retention playbook aligned to each customer cluster |
| `models/churn_model.pkl` | Serialised Random Forest classifier |
| `models/scaler.pkl` | Fitted StandardScaler for inference |
| `models/threshold.pkl` | Optimised classification threshold |

---

---

# Part 2 — Streamlit Intelligence Dashboard

> Production deployment · Business user interface · Real-time prediction · ROI simulation

**🔗 [Open Live App →](https://bank-customer-data-prep-j3mmdpxvqukgq88ppncxxx.streamlit.app/)**

---

## 2.1 What the App Does

The app provides four core capabilities — all accessible without any coding:

| Capability | Description |
|---|---|
| **Portfolio Risk Dashboard** | Filter and score churn risk across the full customer base with live KPIs |
| **Single Customer Assessment** | Run a real-time AI prediction on any individual customer profile |
| **What-If ROI Simulation** | Model the financial impact of a retention campaign before committing budget |
| **AI Interpretability Panel** | Inspect model feature importances and the full probability distribution |

---

## 2.2 Dashboard Modes

### Internal Demo Mode
Loads the processed dataset automatically from `data/processed/`. Use this to explore the full feature set immediately with no setup.

### Client Upload Mode
Upload any customer CSV file for batch analysis. The app uses a flexible **column alias resolver** that accepts non-standard column names and maps them automatically to the expected schema.

A downloadable **CSV template** is available in the sidebar.

**Expected columns:**
```
CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure,
Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
```

---

## 2.3 Dashboard Sections

### Portfolio Risk Dashboard
Filter the entire customer portfolio by geography, age range, balance range, and AI risk verdict simultaneously.

**KPI Strip — four live metrics update with every filter change:**
- **💰 Exposure** — Total balance at risk (customers above the churn threshold)
- **📉 Risk Avg** — Mean churn probability across the filtered portfolio
- **🚨 Critical Alerts** — Count of customers with churn probability ≥ 0.80
- **🤖 AI Health** — Model confidence indicator

### Single Customer AI Assessment
Enter any customer's profile manually and receive a real-time prediction: AI verdict, churn probability %, a full feature breakdown table, and a one-click CSV export.

**Churn probability is bucketed into four AI verdicts:**

| Score | Verdict |
|---|---|
| < 0.30 | 🟢 Stay (Safe) |
| 0.30 – 0.49 | 🟡 Likely Stay |
| 0.50 – 0.79 | 🟠 Likely Leave |
| ≥ 0.80 | 🔴 Highly Leave (Churn) |

### What-If ROI Simulation
Define a target segment by age and balance bracket, set a cost-per-customer and campaign effectiveness %, and the simulator returns:
- Estimated capital saved from successful retention
- Total campaign cost
- Net ROI

A risk distribution chart visualises the probability spread of the targeted segment. Results are exportable as a CSV financial report.

### AI Interpretability Panel
- **Feature Impact Chart** — Horizontal bar chart of Random Forest feature importances, exportable as CSV
- **Probability Distribution** — Histogram + KDE of churn scores across the full dataset, exportable as a master batch report

---

## 2.4 Model Feature Engineering (Applied at Inference)

The app re-applies the same feature engineering pipeline on every prediction:

| Feature | Formula | Business Meaning |
|---|---|---|
| `ProductPerYear` | `NumOfProducts / (Tenure + 0.1)` | Engagement depth over customer lifetime |
| `balance_to_income` | `Balance / (EstimatedSalary + 1)` | Proportion of personal wealth held at the bank |
| `income_v_product` | `EstimatedSalary / (NumOfProducts + 1)` | Revenue efficiency relative to product usage |

---

## 2.5 Installation & Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/AbdulbariSoliman/Bank-Customer-Data-Prep.git
cd Bank-Customer-Data-Prep

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

> ⚠️ The app requires all three files inside `/models` to be present at startup.

---

## 2.6 Exports Available

| Export | Filename | Where to trigger |
|---|---|---|
| Individual customer profile | `individual_assessment.csv` | Single Customer Assessment |
| Financial simulation report | `roi_simulation_report.csv` | What-If Simulation |
| Model feature importances | `ai_model_logic.csv` | AI Interpretability Panel |
| Full filtered batch report | `master_churn_report.csv` | AI Interpretability Panel |

---

---

## ✅ Conclusion

By combining **predictive modelling (AUC-ROC: 0.8351)** with **strategic segmentation (K-Means, 4 cohorts)** and a **live business dashboard**, this pipeline enables a bank to prioritise its retention budget toward customers who represent the highest financial value and the highest probability of exit — rather than applying a one-size-fits-all campaign across the full portfolio.

The result is a system that a data science team can maintain and a business team can use independently, without writing a single line of code.

---

## 👤 Author

**Abdulbari Soliman** — Program Manager · Data Analytics · AI/ML

[LinkedIn](https://www.linkedin.com/in/abdulbari-soilman/) · [GitHub](https://github.com/AbdulbariSoliman) · [Live App](https://bank-customer-data-prep-j3mmdpxvqukgq88ppncxxx.streamlit.app/)
