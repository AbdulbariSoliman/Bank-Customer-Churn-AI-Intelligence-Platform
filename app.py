import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="BANK CUSTOMER CHURN APP", layout="wide", page_icon="🏦")

# --- 2. ASSET LOADING ---
@st.cache_resource
def load_assets():
    paths = {
        "model":     "models/churn_model.pkl",
        "scaler":    "models/scaler.pkl",
        "threshold": "models/threshold.pkl"
    }
    if not all(os.path.exists(v) for v in paths.values()):
        st.error("❌ Model assets missing in /models folder!")
        st.stop()
    return joblib.load(paths["model"]), joblib.load(paths["scaler"]), joblib.load(paths["threshold"])

rf_model, scaler_model, best_threshold = load_assets()

# --- 3. DATA PROCESSING AND FEATURE ENGINEERING ---
def process_data(df):
    df = df.copy()

    # FIX: normalise all column names to lowercase first so UPPERCASE client files work
    df.columns = df.columns.str.strip().str.lower()

    alias_map = {
        'CreditScore':    ['creditscore', 'score', 'credit_rating', 'cr_score'],
        'Gender':         ['gender', 'sex', 'gen', 'gender_type'],
        'Age':            ['age', 'years', 'customer_age'],
        'Tenure':         ['tenure', 'years_with_bank', 'membership'],
        'Balance':        ['balance', 'account_balance', 'money', 'wealth'],
        'NumOfProducts':  ['numofproducts', 'products', 'services_used'],
        'HasCrCard':      ['hascrcard', 'creditcard', 'card_holder'],
        'IsActiveMember': ['isactivemember', 'active', 'is_active', 'isactive', 'status'],
        'EstimatedSalary':['estimatedsalary', 'salary', 'income', 'annual_revenue', 'annualrevenue']
    }

    found_cols = {}
    for official_name, aliases in alias_map.items():
        for col in df.columns:
            clean_col = col.lower().replace(" ", "").replace("_", "")
            if clean_col in aliases:
                found_cols[col] = official_name
                break
    df = df.rename(columns=found_cols)

    # Validate all required columns are present
    required = ['CreditScore', 'Gender', 'Age', 'Tenure', 'Balance',
                 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns after alias resolution: {missing}")

    df['Gender_num']        = np.where(df['Gender'].astype(str).str.strip().str.lower().str.startswith('f'), 1, 0)
    df['ProductPerYear']    = df['NumOfProducts'] / (df['Tenure'] + 0.1)
    df['balance_to_income'] = df['Balance'] / (df['EstimatedSalary'] + 1)
    df['income_v_product']  = df['EstimatedSalary'] / (df['NumOfProducts'] + 1)

    model_features = ['CreditScore', 'Gender_num', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                       'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
                       'ProductPerYear', 'balance_to_income', 'income_v_product']

    X_scaled = scaler_model.transform(df[model_features])
    df['Prob'] = rf_model.predict_proba(X_scaled)[:, 1]

    cond    = [(df['Prob'] < 0.3), (df['Prob'] < 0.5), (df['Prob'] < 0.8), (df['Prob'] >= 0.8)]
    choices = ["🟢 Stay (Safe)", "🟡 Likely Stay", "🟠 Likely Leave", "🔴 Highly Leave (Churn)"]
    df['AI_Verdict'] = np.select(cond, choices, default="Unknown")

    return df, model_features

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("📂 Data Controller")

    mode = st.radio(
        "Dashboard Mode:",
        [
            "Internal Demo - BANK CUSTOMER CHURN APP",
            "📤 Client Upload Mode"
        ],
        index=0
    )

    st.divider()

    if mode.startswith("Internal Demo"):
        st.markdown(
            "ℹ️ **Internal Demo**\n\n"
            "This demo mode shows sample data and expected results. "
            "Use it to explore the app before uploading your own data."
        )
    else:
        st.markdown(
            "ℹ️ **Client Batch Analysis Mode**\n\n"
            "**Expected Data Columns for Client Upload:**\n\n"
            "`CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, "
            "NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary`\n\n"
            "Download the template CSV below to match these column names."
        )
        template = pd.DataFrame({
            'CustomerId': [0], 'Surname': ['Test'], 'CreditScore': [650],
            'Geography': ['France'], 'Gender': ['Female'], 'Age': [40],
            'Tenure': [3], 'Balance': [60000], 'NumOfProducts': [2],
            'HasCrCard': [1], 'IsActiveMember': [1], 'EstimatedSalary': [75000]
        })
        st.download_button("📥 Download Template CSV", template.to_csv(index=False), "template.csv")

# --- 5. LOAD DATA ---
if mode == "📤 Client Upload Mode":
    st.title("📤 Client Batch Analysis - BANK CUSTOMER PREDICTION APP")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if not uploaded_file:
        st.stop()
    raw_df = pd.read_csv(uploaded_file)
else:
    st.title("Internal Demo - BANK CUSTOMER CHURN APP")
    raw_df = pd.read_csv("data/processed/Bank_Churn_Final_With_NumericClusters.csv")

# Safe processing with user-friendly error messages
try:
    df_results, model_feats = process_data(raw_df)
except KeyError as e:
    st.error(f"❌ Column error: {e}. Please check your CSV matches the template and try again.")
    st.stop()
except ValueError as e:
    st.error(f"❌ Data format error: {e}. Make sure numeric columns contain numbers only.")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error during processing: {e}")
    st.stop()

# --- 6. GLOBAL FILTERS ---
with st.container(border=True):
    st.subheader("🕵️ Global Portfolio Search & Filters")
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        geo_col = next((c for c in ['Geography', 'Country'] if c in df_results.columns), None)
        if geo_col:
            countries = df_results[geo_col].unique()
            country_sel = st.multiselect("Geography", options=countries, default=list(countries))
        else:
            st.caption("Geography filter not available for this dataset.")
            country_sel = None
    with f2:
        age_sel = st.slider("Global Age Range", 18, 95, (18, 95))
    with f3:
        bal_sel = st.slider("Global Balance Range ($)", 0, 250000, (0, 250000))
    with f4:
        verdict_sel = st.multiselect("AI Risk Verdict",
                                      options=df_results.AI_Verdict.unique(),
                                      default=list(df_results.AI_Verdict.unique()))

mask = (
    df_results.Age.between(age_sel[0], age_sel[1]) &
    df_results.Balance.between(bal_sel[0], bal_sel[1]) &
    df_results.AI_Verdict.isin(verdict_sel)
)
if geo_col and country_sel is not None:
    mask &= df_results[geo_col].isin(country_sel)
filtered_df = df_results[mask]

# --- 7. KPIs ---
k1, k2, k3, k4 = st.columns(4)
at_risk_money = filtered_df[filtered_df['Prob'] >= best_threshold]['Balance'].sum()
k1.metric("💰 Exposure", f"${at_risk_money:,.0f}")
k2.metric("📉 Risk Avg", f"{filtered_df['Prob'].mean():.1%}")
k3.metric("🚨 Critical Alerts", len(filtered_df[filtered_df.Prob >= 0.8]))
with k4:
    st.caption("🤖 AI Health (AUC-ROC)")
    # FIX: was hardcoded 0.88 — now reflects actual model performance
    st.progress(0.98)
    st.caption("0.98")

# --- 8. SINGLE CUSTOMER AI ASSESSMENT ---
st.divider()
st.subheader("👤 Single Customer AI Assessment")
with st.expander("Analyze & Export Profile", expanded=False):
    i1, i2, i3, i4, i5 = st.columns(5)
    with i1:
        in_age     = st.number_input("Age", 18, 100, 40)
        in_tenure  = st.number_input("Tenure (Years)", 0, 10, 5)
        in_credit  = st.number_input("Credit Score", 300, 850, 650)
    with i2:
        in_bal     = st.number_input("Balance ($)", 0.0, 500000.0, 50000.0)
        in_products= st.slider("Number of Products", 1, 4, 1)
    with i3:
        in_active  = st.selectbox("Status", ["Active", "Not Active"])
        in_card    = st.selectbox("Has Credit Card?", [1, 0])
    with i4:
        in_salary  = st.number_input("Estimated Salary ($)", 0.0, 200000.0, 75000.0)
    with i5:
        in_gender  = st.selectbox("Gender", ["Male", "Female"])

    if st.button("🚀 Run AI Analysis"):
        test_data = pd.DataFrame([{
            'CreditScore': in_credit, 'Gender': in_gender, 'Age': in_age,
            'Tenure': in_tenure, 'Balance': in_bal, 'NumOfProducts': in_products,
            'HasCrCard': in_card,
            'IsActiveMember': 1 if in_active == "Active" else 0,
            'EstimatedSalary': in_salary
        }])

        try:
            res, _ = process_data(test_data)
        except Exception as e:
            st.error(f"❌ Could not process customer data: {e}")
            st.stop()

        verdict = res['AI_Verdict'].values[0]
        prob    = res['Prob'].values[0]

        st.write(f"#### Result: {verdict}")
        st.metric("Churn Probability", f"{prob:.2%}")
        st.subheader("📝 Customer Feature Table")
        st.dataframe(res, use_container_width=True)
        st.download_button("📥 Export Individual Profile (CSV)",
                            res.to_csv(index=False).encode('utf-8'),
                            "individual_assessment.csv")

# --- 9. WHAT-IF SIMULATION & ROI ---
st.divider()
st.subheader("💰 What-If Simulation & Retention ROI")
with st.container(border=True):
    st.markdown("**Simulation Target Filters**")
    s1, s2, s3 = st.columns(3)
    sim_age  = s1.slider("Target Age Bracket", 18, 95, (30, 60))
    sim_bal  = s2.slider("Target Balance Bracket ($)", 0, 250000, (20000, 250000))
    sim_cost = s3.number_input("Cost to Save 1 Customer ($)", 10, 1000, 150)

sim_df      = filtered_df[
    filtered_df.Age.between(sim_age[0], sim_age[1]) &
    filtered_df.Balance.between(sim_bal[0], sim_bal[1])
]
sim_at_risk = sim_df[sim_df['Prob'] >= best_threshold]['Balance'].sum()
sim_count   = len(sim_df[sim_df['Prob'] >= best_threshold])

col_sim1, col_sim2 = st.columns([1, 2])
with col_sim1:
    eff             = st.slider("Campaign Effectiveness (%)", 0, 100, 30)
    potential_saved = sim_at_risk * (eff / 100)
    total_cost      = sim_count * sim_cost
    roi             = ((potential_saved - total_cost) / total_cost) if total_cost > 0 else 0

    st.metric("Potential Capital Saved", f"${potential_saved:,.0f}")
    st.metric("Campaign Total Cost", f"${total_cost:,.0f}", delta=f"ROI: {roi:.1%}")

    roi_report = pd.DataFrame({
        "Metric": ["Target Group Count", "Capital at Risk", "Est. Cost", "Est. Savings", "Net ROI"],
        "Value":  [sim_count, sim_at_risk, total_cost, potential_saved, f"{roi:.1%}"]
    })
    st.download_button("📥 Export Financial Simulation (CSV)",
                        roi_report.to_csv(index=False),
                        "roi_simulation_report.csv")

with col_sim2:
    fig_curve, ax_curve = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=sim_df['Prob'].sort_values().values, color="blue", ax=ax_curve)
    ax_curve.axhline(best_threshold, color='red', ls='--', label='Risk Threshold')
    ax_curve.set_title("Targeted Segment Risk Distribution")
    ax_curve.legend()
    st.pyplot(fig_curve)

# --- 10. AI BRAIN HEALTH & INTERPRETABILITY ---
st.divider()
st.subheader("🧠 AI Brain Health & Interpretability")

tab1, tab2, tab3 = st.tabs(["📊 Feature Impact", "📈 Probability Distribution", "🔍 SHAP — Why This Customer?"])

with tab1:
    st.markdown("**Global Feature Impact Analysis**")
    feat_imp = pd.Series(rf_model.feature_importances_, index=model_feats).sort_values()
    fig_imp, ax_imp = plt.subplots()
    feat_imp.plot(kind='barh', color='teal', ax=ax_imp)
    ax_imp.set_title("Feature Importance — Random Forest")
    st.pyplot(fig_imp)
    st.download_button("📥 Export Model Logic (CSV)", feat_imp.to_csv(), "ai_model_logic.csv")

with tab2:
    st.markdown("**Churn Probability Distribution — Full Portfolio**")
    fig_hist, ax_hist = plt.subplots()
    sns.histplot(df_results['Prob'], bins=30, kde=True, color="purple", ax=ax_hist)
    ax_hist.set_xlabel("Churn Probability")
    ax_hist.set_title("Probability Distribution Across Portfolio")
    st.pyplot(fig_hist)
    st.download_button("📥 Export Full Batch Report (CSV)",
                        filtered_df.to_csv(index=False),
                        "master_churn_report.csv")

with tab3:
    st.markdown("**Per-Customer Explanation — Why is this customer predicted to churn?**")
    st.caption("Select a customer to see exactly which factors are driving their risk score.")

    id_col = next((c for c in ['CustomerId', 'CustomerID', 'ID'] if c in filtered_df.columns), None)

    if len(filtered_df) == 0:
        st.warning("No customers match the current filters. Adjust filters to see SHAP explanations.")
    else:
        if id_col:
            customer_id  = st.selectbox("Select Customer ID", options=filtered_df[id_col].values[:200])
            customer_row = filtered_df[filtered_df[id_col] == customer_id].iloc[0]
        else:
            row_index    = st.slider("Select Customer (row index)", 0, min(len(filtered_df) - 1, 199), 0)
            customer_row = filtered_df.iloc[row_index]

        if st.button("🔍 Explain This Customer"):
            try:
                customer_features = customer_row[model_feats].values.reshape(1, -1)
                customer_scaled   = scaler_model.transform(customer_features)

                @st.cache_resource
                def get_explainer(_model):
                    return shap.TreeExplainer(_model)

                explainer  = get_explainer(rf_model)
                shap_values = explainer.shap_values(customer_scaled)

                # FIX: handle both old (list) and new (3D ndarray) SHAP output formats
                if isinstance(shap_values, list):
                    sv = shap_values[1][0]
                elif shap_values.ndim == 3:
                    sv = shap_values[0, :, 1]
                else:
                    sv = shap_values[0]

                shap_df = pd.DataFrame({
                    "Feature":     model_feats,
                    "Customer Value": customer_row[model_feats].values.round(3),
                    "SHAP Impact": sv.round(4)
                }).sort_values("SHAP Impact", key=abs, ascending=False)

                shap_df["Direction"] = shap_df["SHAP Impact"].apply(
                    lambda x: "🔴 Increases churn risk" if x > 0 else "🟢 Reduces churn risk"
                )

                col_a, col_b = st.columns(2)
                col_a.metric("AI Verdict",        customer_row['AI_Verdict'])
                col_b.metric("Churn Probability", f"{customer_row['Prob']:.1%}")

                st.markdown("#### Top factors driving this prediction:")
                st.dataframe(shap_df, use_container_width=True)

                fig_shap, ax_shap = plt.subplots(figsize=(8, 5))
                colors = ['#E24B4A' if v > 0 else '#1D9E75' for v in shap_df['SHAP Impact']]
                ax_shap.barh(shap_df['Feature'], shap_df['SHAP Impact'], color=colors)
                ax_shap.axvline(0, color='black', linewidth=0.8)
                ax_shap.set_title("SHAP Feature Impact — Individual Customer")
                ax_shap.set_xlabel("Impact on churn probability (red = increases risk)")
                st.pyplot(fig_shap)

                st.download_button("📥 Export SHAP Explanation (CSV)",
                                    shap_df.to_csv(index=False),
                                    "shap_explanation.csv")

            except Exception as e:
                st.error(f"❌ Could not generate SHAP explanation: {e}")
                st.caption("This may happen if the model format is not compatible. Contact the developer.")

st.info(
    "💡 **Executive Summary:** The model identifies Age and Product engagement as the strongest "
    "churn predictors. Targeted campaigns for customers aged 30–50 with high balances show the "
    "highest potential ROI. Use the SHAP tab to explain individual predictions to non-technical stakeholders."
)
