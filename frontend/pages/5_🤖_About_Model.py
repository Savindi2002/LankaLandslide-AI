import streamlit as st
import requests


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="About Model | LankaLandslide AI",
    page_icon="🤖",
    layout="wide"
)


API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# HEADER
# ============================================================

st.title("🤖 About the LankaLandslide AI Model")

st.markdown(
    """
    This page describes the machine-learning model,
    prediction features, and system limitations.
    """
)


# ============================================================
# MODEL INFO
# ============================================================

model_info = None


try:

    response = requests.get(
        f"{API_BASE_URL}/api/model-info",
        timeout=10
    )

    if response.status_code == 200:

        model_info = response.json()

except Exception:

    pass


# ============================================================
# MODEL SUMMARY
# ============================================================

st.markdown("---")

st.header("🧠 Model Summary")


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Model",
        "XGBoost"
    )


with c2:

    st.metric(
        "Features",
        "27"
    )


with c3:

    st.metric(
        "Threshold",
        "0.49"
    )


# ============================================================
# FEATURES
# ============================================================

st.markdown("---")

st.header("📊 Model Features")


features = [
    "rainfall_1day",
    "rainfall_3day",
    "rainfall_7day",
    "rainfall_14day",
    "rainfall_30day",
    "rainfall_3day_avg",
    "rainfall_7day_avg",
    "rainfall_14day_avg",
    "rainfall_30day_avg",
    "rain_hours",
    "temp_max",
    "temp_min",
    "temp_mean",
    "temperature_range",
    "wind_max",
    "wind_gust_max",
    "month_sin",
    "month_cos",
    "heavy_rain_10mm",
    "heavy_rain_25mm",
    "heavy_rain_50mm",
    "heavy_rain_100mm",
    "elevation_mean_m",
    "elevation_max_m",
    "elevation_min_m",
    "slope_mean_deg",
    "slope_max_deg"
]


feature_df = {
    "Feature": features,
    "Category": [
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Rainfall",
        "Weather",
        "Temperature",
        "Temperature",
        "Temperature",
        "Temperature",
        "Wind",
        "Wind",
        "Seasonality",
        "Seasonality",
        "Heavy Rain",
        "Heavy Rain",
        "Heavy Rain",
        "Heavy Rain",
        "Terrain",
        "Terrain",
        "Terrain",
        "Terrain",
        "Terrain"
    ]
}


import pandas as pd


st.dataframe(
    pd.DataFrame(feature_df),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PREDICTION TYPES
# ============================================================

st.markdown("---")

st.header("🔮 Prediction Modes")


c1, c2, c3 = st.columns(3)


with c1:

    st.info(
        """
        ### 📚 Historical

        Past dates use historical weather
        observations/reanalysis data.
        """
    )


with c2:

    st.info(
        """
        ### 📅 Today

        Today's available weather information
        is used for the prediction.
        """
    )


with c3:

    st.success(
        """
        ### 🔮 Future

        Future dates use forecast weather
        information up to 16 days ahead.
        """
    )


# ============================================================
# FUTURE PREDICTION PROCESS
# ============================================================

st.markdown("---")

st.header("⚙️ Future Prediction Process")


st.markdown(
    """
    ```text
    Selected Future Date
             ↓
    Historical Weather Window
             +
    Forecast Weather
             ↓
       Feature Engineering
             ↓
    27 Model Features
             ↓
          XGBoost
             ↓
     Risk Probability
             ↓
       LOW / MEDIUM / HIGH
    ```
    """
)


# ============================================================
# MODEL COMPARISON
# ============================================================

st.markdown("---")

st.header("📈 Model Evaluation")


comparison = pd.DataFrame(
    {
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "XGBoost",
            "LSTM"
        ],
        "Accuracy": [
            0.795263,
            0.954852,
            0.937500,
            0.922603
        ],
        "Precision": [
            0.011038,
            0.025381,
            0.023551,
            0.016924
        ],
        "Recall": [
            0.930233,
            0.465116,
            0.604651,
            0.534884
        ],
        "F1": [
            0.021816,
            0.048135,
            0.045336,
            0.032810
        ],
        "ROC-AUC": [
            0.927522,
            0.868705,
            0.913448,
            0.901147
        ],
        "PR-AUC": [
            0.026140,
            0.024142,
            0.027841,
            0.021189
        ]
    }
)


st.dataframe(
    comparison.style.format(
        {
            "Accuracy": "{:.4f}",
            "Precision": "{:.4f}",
            "Recall": "{:.4f}",
            "F1": "{:.4f}",
            "ROC-AUC": "{:.4f}",
            "PR-AUC": "{:.4f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CLASS IMBALANCE
# ============================================================

st.markdown("---")

st.header("⚖️ Class Imbalance")


st.write(
    """
    The historical training dataset contains many more
    non-event district-days than recorded landslide
    district-days.

    Therefore, accuracy alone is not sufficient for evaluating
    this problem. Precision, recall, F1, ROC-AUC and PR-AUC
    are also considered.
    """
)


# ============================================================
# LIMITATIONS
# ============================================================

st.markdown("---")

st.header("⚠️ Model Limitations")


st.warning(
    """
    **Important limitations**

    • Predictions represent district-day risk.

    • The model does not predict an exact landslide
      location.

    • Historical zero-event days mean no recorded event,
      not necessarily no actual event.

    • Future predictions depend on weather forecasts.

    • Forecast conditions can change when new weather
      forecasts become available.

    • Terrain features are local district-center summaries.

    • The system is not an official disaster-warning system.
    """
)


# ============================================================
# API MODEL INFORMATION
# ============================================================

if model_info is not None:

    st.markdown("---")

    st.header("🔌 Live API Model Configuration")

    st.json(
        model_info
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "LankaLandslide AI • XGBoost • FastAPI • Streamlit"
)