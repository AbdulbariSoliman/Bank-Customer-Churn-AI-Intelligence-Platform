# Retention Playbook by Customer Segment

Segments come from K-Means clustering (k = 4) on numeric customer features. They are ranked by actual churn rate, from highest to lowest risk.

**Portfolio churn rate:** 20.4% across 10,000 customers.

| Rank | Cluster | Profile | Customers | Churn Rate | Risk |
|---|---|---|---|---|---|
| 1 | **Cluster 0** | High Balance / High Salary | 2,889 | **26.2%** | 🔴 Critical |
| 2 | **Cluster 2** | High Balance / Low Salary | 2,862 | **23.4%** | 🟠 High |
| 3 | **Cluster 1** | Low Tenure / More Products | 1,602 | **17.7%** | 🟡 Moderate |
| 4 | **Cluster 3** | High Tenure / Low Balance | 2,647 | **12.4%** | 🟢 Stable |

---

## 🔴 Cluster 0: VIP Retention

**Profile:** average balance of about $107K and average salary of about $153K, but only 1.2 products per customer. These are wealthy customers who use the bank very little.

**Why they leave:** high-value customers with a single product have little reason to stay and are easy targets for competitors.

**Actions:**
- Cross-sell a second product (savings, investment or credit card) as a priority
- Assign a relationship manager to the highest balances
- Run proactive check-ins before contract or rate renewals

**Why it matters:** the highest churn rate (26.2%) combined with about $308M in total balances makes this the most valuable segment to protect.

---

## 🟠 Cluster 2: Financial Stability Support

**Profile:** average balance of about $114K but average salary of only about $49K. A large share of their personal wealth sits at the bank.

**Why they leave:** customers whose savings far exceed their income may move funds for better rates, or may be under financial pressure.

**Actions:**
- Offer competitive savings rates or term deposits to keep balances in place
- Provide financial planning or advisory sessions
- Offer consolidation products where relevant

**Why it matters:** the second-highest churn rate (23.4%) and the largest total balance of any segment, about $327M.

---

## 🟡 Cluster 1: Onboarding Support

**Profile:** average tenure of only about 1 year, but already about 1.8 products per customer. These are new, engaged customers.

**Why they leave:** early-relationship churn. Customers are still deciding whether the bank meets their expectations.

**Actions:**
- High-touch onboarding during the first 12 months
- Welcome offers and milestone rewards (6 and 12 months)
- Fast resolution of early service issues

**Why it matters:** moderate risk (17.7%) but strong engagement. Keeping them through the first year builds long-term customers.

---

## 🟢 Cluster 3: Loyalty Maintenance

**Profile:** the longest tenure (about 6.4 years), the most products (about 2.0) and a low average balance of about $12K.

**Why they stay:** long relationships and several products make switching harder.

**Actions:**
- Low-cost loyalty rewards and recognition of long tenure
- Digital self-service to keep the cost to serve low
- Avoid spending retention budget here

**Why it matters:** the lowest churn rate (12.4%). The goal is to keep this base stable at minimal cost.

---

## Key Takeaway

Retention budget should go first to **Cluster 0** and **Cluster 2**. Together they hold about $635M in balances and have the highest churn rates. Cross-selling a second product is the strongest lever across all segments.
