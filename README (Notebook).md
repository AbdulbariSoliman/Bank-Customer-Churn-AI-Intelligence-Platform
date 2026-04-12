# 🏦 Bank Customer Churn: Predictive Intelligence & Strategic Research

**End-to-End Machine Learning Pipeline for Financial Risk Management**

This project delivers a high-fidelity data science pipeline to solve the problem of customer attrition in retail banking. It moves from raw, messy data to a production-ready model that identifies high-value risk segments and generates targeted retention recommendations.

> **Source:** Maven Analytics — Bank Customer Churn Dataset (Kaggle)
> **Engineering Focus:** Feature creation, stratified validation, and numeric clustering
> **Scope:** 10,000 customer records

---

## 🏗️ 1. Technical Data Architecture

The foundation of this project is a robust cleaning and feature engineering suite designed specifically for banking data.

### 🧹 Data Sanitisation

- **Currency Normalisation:** Transformed `Balance` and `EstimatedSalary` from string representations into numeric types for mathematical processing.
- **Integrity Checks:** Automated duplicate removal and median-based imputation for missing values to prevent data leakage.
- **Encoding:** Converted categorical fields (`Geography`, `Gender`) into machine-readable formats while retaining geographic business distinctions for segmentation.

### 🛠️ Feature Engineering — The "Alpha" Features

Three financial ratios were engineered to capture customer behaviour more effectively than raw fields alone:

| Feature | Formula | Business Meaning |
|---|---|---|
| **Product Density** | `NumOfProducts / (Tenure + 0.1)` | Measures engagement depth relative to time with the bank |
| **Liquidity Leverage** | `Balance / (EstimatedSalary + 1)` | Indicates the proportion of personal wealth held at the bank |
| **Revenue Efficiency** | `EstimatedSalary / (NumOfProducts + 1)` | Estimates cross-sell potential relative to current product usage |

---

## 🎯 2. Modelling Performance & Audit

A **Random Forest Classifier** was selected to capture the non-linear relationships in customer behaviour, significantly outperforming the Logistic Regression baseline across all key metrics.

### 📊 Model Performance Benchmark

| Metric | Logistic Regression (Baseline) | Random Forest (Final) | Improvement |
|---|---|---|---|
| Accuracy | 81.25% | 85.25% | +4.00% |
| ROC-AUC | 0.7814 | 0.8351 | +6.87% |

### 🔍 Top Churn Drivers

The model identifies the following as the primary predictors of customer exit:

1. **Age** — Risk peaks significantly in the **40–60** demographic. Older customers with single-product holdings are the highest-risk cohort.
2. **Product Count** — Churn rate drops sharply as product holdings increase from 1 to 2, confirming that cross-selling is the single most effective retention lever.
3. **Income vs. Product (Revenue Efficiency)** — Customers whose salary far exceeds their product engagement are consistently under-served and at high risk of exit.

> ⚠️ **Note:** Feature importance percentage values were not included in the original notes. Add them here once extracted from the model — e.g. *Age (importance: 28.4%)*.

---

## 🧭 3. Strategic Segmentation — K-Means Clustering

K-Means Clustering was applied to categorise the portfolio into actionable segments, moving the analysis from general predictions to targeted interventions.

> ⚠️ **Note:** The number of clusters (K value) was not specified in the original notes. Add it here — e.g. *K-Means (K=4)*.

### 📊 Risk Hierarchy & Retention Recommendations

| Cluster | Customer Profile | Recommended Strategy | Risk Level |
|---|---|---|---|
| **Cluster 0** | High Balance / High Salary | **VIP Retention** — Cross-sell a second product immediately to secure assets. | 🔴 Critical |
| **Cluster 2** | High Balance / Low Salary | **Debt Stabilisation** — Offer financial counselling or consolidation products. | 🟠 High |
| **Cluster 1** | Low Tenure / High Products | **Onboarding Support** — High-touch service to retain customers through Year 1. | 🟡 Moderate |
| **Cluster 3** | High Tenure / Low Balance | **Loyalty Maintenance** — Low-cost rewards programme for a stable, long-term base. | 🟢 Stable |

---

## 💾 4. Project Outputs

The notebook generates the following assets for business integration and downstream use in the prediction app:

| File | Description |
|---|---|
| `Bank_Churn_Final_With_NumericClusters.csv` | Master dataset — used directly as the app's demo data source |
| `cluster_summary_unscaled.csv` | Non-technical segment summary for stakeholder presentations |
| `recommendations_final.md` | Strategic retention playbook aligned to each customer cluster |
| `models/churn_model.pkl` | Serialised Random Forest classifier |
| `models/scaler.pkl` | Fitted StandardScaler for inference |
| `models/threshold.pkl` | Optimised classification threshold |

---

## ✅ Conclusion

By combining **predictive modelling (ROC-AUC: 0.8351)** with **strategic segmentation**, this pipeline enables the bank to prioritise its retention budget toward customers who represent the highest financial value and the highest probability of exit — rather than applying a one-size-fits-all campaign across the full portfolio.

The outputs feed directly into the [Bank Customer Churn Prediction App](../app.py), where risk scores, simulations, and segment filters can be explored interactively by business users without any coding required.
