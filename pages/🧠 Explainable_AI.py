import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular

st.title("🧠 Explainable AI")

# ── Load models based on prediction mode ──
mode = st.session_state.get("prediction_mode", "config")

if mode == "brand":
    model_xgb  = joblib.load("models/model_xgb_brand.pkl")
    model_rf   = joblib.load("models/model_rf_brand.pkl")
    scaler     = joblib.load("models/scaler_brand_final.pkl")
    metrics    = joblib.load("models/brand_metrics.pkl")
    X_test     = pd.read_csv("models/X_brand_test.csv")
    X_train    = pd.read_csv("models/X_brand_train.csv")
    features   = [
        "Engine HP", "Engine Cylinders", "weight_est",
        "displacement_est", "vehicle_age",
        "power_to_weight", "hp_per_cylinder"
    ]
else:
    model_xgb  = joblib.load("models/model_xgb_final.pkl")
    model_rf   = joblib.load("models/model_rf_final.pkl")
    scaler     = joblib.load("models/scaler_final.pkl")
    metrics    = joblib.load("models/model_metrics.pkl")
    X_test     = pd.read_csv("models/X_test_data.csv")
    X_train    = pd.read_csv("models/X_train_data.csv")
    features   = [
        "cylinders", "displacement", "horsepower",
        "weight", "model-year",
        "power_to_weight", "car_age", "hp_per_cylinder"
    ]

XGB_W = metrics["xgb_weight"]
RF_W  = metrics["rf_weight"]

# ── Session state ──
cyl    = st.session_state.get("cyl")
hp     = st.session_state.get("hp")
weight = st.session_state.get("weight")
year   = st.session_state.get("year")
disp   = st.session_state.get("disp")

if cyl is None and mode == "config":
    st.warning("Please make a prediction first from Dashboard.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/🚗 Dashboard.py")
    st.stop()

# ── Build input vector ──
if mode == "brand":
    input_sc = np.array([st.session_state.get("brand_input_sc")])
else:
    power_to_weight = hp / weight
    car_age         = 2026 - year
    hp_per_cyl      = hp / cyl
    input_raw = np.array([[cyl, disp, hp, weight, year,
                            power_to_weight, car_age, hp_per_cyl]])
    input_sc  = scaler.transform(input_raw)

# ── Ensemble prediction ──
xgb_pred = model_xgb.predict(input_sc)[0]
rf_pred  = model_rf.predict(input_sc)[0]
ens_pred = (XGB_W * xgb_pred) + (RF_W * rf_pred)
ens_kmpl = ens_pred * 0.4251

st.success(f"🎯 Ensemble Prediction: **{ens_pred:.2f} MPG** ({ens_kmpl:.2f} KM/L)")
st.caption(f"Weighted: {int(XGB_W*100)}% XGBoost + {int(RF_W*100)}% Random Forest")

col1, col2, col3 = st.columns(3)
col1.metric("XGBoost", f"{xgb_pred:.2f} MPG")
col2.metric("Random Forest", f"{rf_pred:.2f} MPG")
col3.metric("Ensemble", f"{ens_pred:.2f} MPG")

st.divider()

# ── Precompute SHAP ──
@st.cache_data
def get_shap(_model, _X_test_vals, _input_sc):
    try:
        explainer   = shap.TreeExplainer(_model)
        shap_vals   = explainer.shap_values(_X_test_vals)
        shap_single = explainer.shap_values(_input_sc)
        ev          = explainer.expected_value
        return explainer, shap_vals, shap_single, ev
    except Exception as e:
        return None, None, None, None

explainer, shap_vals, shap_single, ev = get_shap(
    model_xgb, X_test.values, input_sc
)

tab1, tab2, tab3 = st.tabs(["🔵 SHAP", "🟢 LIME", "📊 XGBoost vs RF"])

# ════════════════════════════════
# TAB 1 — SHAP
# ════════════════════════════════
with tab1:
    st.subheader("SHAP — Feature Contribution (XGBoost)")
    st.info("SHAP uses game theory to show how each feature contributed to this prediction.")

    try:
        st.markdown("#### 1️⃣ Summary Plot — Global Feature Importance")
        st.caption("Which features matter most across ALL predictions.")
        plt.figure(figsize=(8, 4))
        shap.summary_plot(shap_vals, X_test, feature_names=features,
                        plot_type="bar", show=False)
        st.pyplot(plt.gcf())
        plt.close()

        st.markdown("#### 2️⃣ Waterfall Plot — Your Prediction Breakdown")
        st.caption("Step-by-step how features pushed your prediction up or down.")
        shap_exp = shap.Explanation(
            values=shap_single[0],
            base_values=ev,
            data=input_sc[0],
            feature_names=features
        )
        plt.figure(figsize=(8, 4))
        shap.plots.waterfall(shap_exp, show=False)
        st.pyplot(plt.gcf())
        plt.close()

        st.markdown("#### 3️⃣ Force Plot — Most Famous SHAP Graph")
        st.caption("Red = pushes prediction higher | Blue = pushes prediction lower")

        # Round values for clean display
        rounded_input    = np.round(input_sc[0], 2)
        rounded_shap     = np.round(shap_single[0], 2)
        rounded_features = [f"{f}={round(v, 2)}" for f, v in zip(features, input_sc[0])]

        plt.figure(figsize=(14, 3))
        shap.force_plot(
        round(float(ev), 2),
        rounded_shap,
        rounded_input,
        feature_names=features,
        matplotlib=True,
        show=False,
        text_rotation=15
        )
        st.pyplot(plt.gcf())
        plt.close()

        st.markdown("#### 4️⃣ Dependence Plot")
        st.caption("Relationship between most important feature and SHAP impact.")
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        top_feature = features[np.argmax(np.abs(shap_single[0]))]
        shap.dependence_plot(top_feature, shap_vals, X_test,
                            feature_names=features,
                            ax=ax4, show=False)
        st.pyplot(fig4)
        plt.close()

    except Exception as e:
        st.error(f"SHAP Error: {e}")

# ════════════════════════════════
# TAB 2 — LIME
# ════════════════════════════════
with tab2:
    st.subheader("LIME — Local Explanation (Ensemble)")
    st.info("LIME explains the ensemble prediction using a local interpretable model.")

    try:
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names=features,
            mode="regression",
            verbose=False
        )

        def ensemble_predict(x):
            return (XGB_W * model_xgb.predict(x)) + (RF_W * model_rf.predict(x))

        explanation = lime_explainer.explain_instance(
            input_sc[0], ensemble_predict, num_features=len(features)
        )

        lime_vals     = explanation.as_list()
        lime_features = [x[0] for x in lime_vals]
        lime_weights  = [x[1] for x in lime_vals]

        fig5, ax5 = plt.subplots(figsize=(8, 4))
        colors = ['green' if w > 0 else 'red' for w in lime_weights]
        ax5.barh(lime_features, lime_weights, color=colors)
        ax5.set_xlabel("Contribution to Ensemble Prediction")
        ax5.set_title("LIME — Feature Contributions (Ensemble)")
        ax5.axvline(x=0, color='black', linewidth=0.8)
        st.pyplot(fig5)
        plt.close()

        col1, col2 = st.columns(2)
        col1.metric("LIME Local R²", f"{explanation.score:.3f}")
        col2.metric("Ensemble MPG",  f"{ens_pred:.2f}")

        st.markdown("#### SHAP vs LIME — Feature Agreement")
        comp_df = pd.DataFrame({
            "Feature":    features,
            "SHAP Value": [round(v, 4) for v in shap_single[0]],
        })
        comp_df.index = range(1, len(comp_df) + 1)
        st.dataframe(comp_df)

    except Exception as e:
        st.error(f"LIME Error: {e}")

# ════════════════════════════════
# TAB 3 — XGBoost vs RF
# ════════════════════════════════
with tab3:
    st.subheader("📊 XGBoost vs Random Forest vs Ensemble")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔵 XGBoost")
        st.metric("R²",   str(metrics["xgb_r2"]))
        st.metric("RMSE", str(metrics["xgb_rmse"]))
    with col2:
        st.markdown("### 🔴 Random Forest")
        st.metric("R²",   str(metrics["rf_r2"]))
        st.metric("RMSE", str(metrics["rf_rmse"]))
    with col3:
        st.markdown("### 🟢 Ensemble")
        st.metric("R²",   str(metrics["ens_r2"]))
        st.metric("RMSE", str(metrics["ens_rmse"]))

    st.divider()

    models_list = ["XGBoost", "Random Forest", "Ensemble"]
    r2_vals     = [metrics["xgb_r2"], metrics["rf_r2"], metrics["ens_r2"]]
    rmse_vals   = [metrics["xgb_rmse"], metrics["rf_rmse"], metrics["ens_rmse"]]
    colors_bar  = ["#00C9FF", "#FF6B6B", "#00FF9F"]

    st.markdown("### R² Score Comparison")
    fig6, ax6 = plt.subplots(figsize=(7, 3))
    bars = ax6.bar(models_list, r2_vals, color=colors_bar, width=0.4)
    ax6.set_ylabel("R² Score")
    ax6.set_title("R² Comparison")
    for bar, val in zip(bars, r2_vals):
        ax6.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.001,
                f"{val}", ha='center', fontweight='bold')
    st.pyplot(fig6)
    plt.close()

    st.markdown("### RMSE Comparison")
    fig7, ax7 = plt.subplots(figsize=(7, 3))
    bars2 = ax7.bar(models_list, rmse_vals, color=colors_bar, width=0.4)
    ax7.set_ylabel("RMSE")
    ax7.set_title("RMSE Comparison")
    for bar, val in zip(bars2, rmse_vals):
        ax7.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.01,
                f"{val}", ha='center', fontweight='bold')
    st.pyplot(fig7)
    plt.close()

    st.markdown("### Feature Importance: XGBoost vs RF")
    xgb_imp = model_xgb.feature_importances_
    rf_imp  = model_rf.feature_importances_

    fig8, ax8 = plt.subplots(figsize=(8, 4))
    x     = np.arange(len(features))
    width = 0.35
    ax8.bar(x - width/2, xgb_imp, width, label='XGBoost',      color='#00C9FF')
    ax8.bar(x + width/2, rf_imp,  width, label='Random Forest', color='#FF6B6B')
    ax8.set_xticks(x)
    ax8.set_xticklabels(features, rotation=45, ha='right', fontsize=8)
    ax8.set_ylabel("Importance")
    ax8.set_title("Feature Importance Comparison")
    ax8.legend()
    st.pyplot(fig8)
    plt.close()

    st.divider()
    st.markdown("### 🏆 Conclusion")
    best = max(zip(models_list, r2_vals), key=lambda x: x[1])
    st.success(f"**{best[0]} wins** with highest R² = {best[1]}")
    st.info("Ensemble combines both models for more robust and reliable predictions.")

if st.button("Go to Analytics"):
    st.switch_page("pages/📈 Analytics.py")

st.markdown("""
<style>
.stApp{
    background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
    background-size: cover;
    background-attachment: fixed;
}
</style>""", unsafe_allow_html=True)