# import streamlit as st
# import requests

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="LankaLandslide AI",
#     page_icon="⛰️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # API CONFIGURATION
# # ============================================================

# API_URL = "http://127.0.0.1:8000"

# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .main-title {
#         font-size: 48px;
#         font-weight: 800;
#         margin-bottom: 5px;
#     }

#     .subtitle {
#         font-size: 20px;
#         margin-bottom: 30px;
#     }

#     .info-card {
#         padding: 25px;
#         border-radius: 15px;
#         border: 1px solid rgba(128,128,128,0.25);
#         margin-bottom: 20px;
#     }

#     .feature-title {
#         font-size: 22px;
#         font-weight: 700;
#     }

#     .small-text {
#         font-size: 15px;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:

#     st.markdown("## ⛰️ LankaLandslide AI")

#     st.markdown("---")

#     st.markdown(
#         """
#         **Machine Learning-Based**

#         Landslide Risk Prediction  
#         & Location Intelligence System

#         🇱🇰 Sri Lanka
#         """
#     )

#     st.markdown("---")

#     st.markdown("### Navigation")

#     st.info(
#         """
#         Use the pages on the left to:

#         🔮 Predict landslide risk  
#         🗺️ Explore risk information  
#         🌧️ View weather conditions  
#         📊 Analyze historical data  
#         🤖 Understand the ML model
#         """
#     )

# # ============================================================
# # API HEALTH CHECK
# # ============================================================

# def check_api():

#     try:
#         response = requests.get(
#             f"{API_URL}/health",
#             timeout=5
#         )

#         return response.status_code == 200

#     except requests.exceptions.RequestException:
#         return False


# api_online = check_api()

# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     '<div class="main-title">⛰️ LankaLandslide AI</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">'
#     'Machine Learning-Based Landslide Risk Prediction and '
#     'Location Intelligence System for Sri Lanka'
#     '</div>',
#     unsafe_allow_html=True
# )

# # ============================================================
# # API STATUS
# # ============================================================

# if api_online:

#     st.success(
#         "🟢 Prediction API is online and ready."
#     )

# else:

#     st.error(
#         "🔴 Prediction API is offline. "
#         "Please start the FastAPI backend."
#     )

# # ============================================================
# # INTRODUCTION
# # ============================================================

# st.markdown("## 🌍 Welcome")

# st.markdown(
#     """
#     **LankaLandslide AI** is a machine learning-based system
#     designed to estimate landslide risk for Sri Lankan
#     districts using environmental and terrain information.

#     The system combines:

#     - 🌧️ Rainfall conditions
#     - 🌡️ Temperature
#     - 💨 Wind conditions
#     - ⛰️ Terrain characteristics
#     - 📅 Temporal patterns
#     - 🤖 Machine learning predictions
#     """
# )

# # ============================================================
# # THREE MAIN FEATURES
# # ============================================================

# st.markdown("## 🚀 What can you do?")

# col1, col2, col3 = st.columns(3)

# with col1:

#     st.markdown(
#         """
#         <div class="info-card">

#         <div class="feature-title">
#         🔮 Risk Prediction
#         </div>

#         <p class="small-text">
#         Select a Sri Lankan district and prediction date
#         to obtain a machine-learning-based landslide
#         risk estimate.
#         </p>

#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# with col2:

#     st.markdown(
#         """
#         <div class="info-card">

#         <div class="feature-title">
#         🌧️ Weather Conditions
#         </div>

#         <p class="small-text">
#         Examine rainfall, temperature and wind
#         conditions used by the prediction system.
#         </p>

#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# with col3:

#     st.markdown(
#         """
#         <div class="info-card">

#         <div class="feature-title">
#         📊 Data & Model Insights
#         </div>

#         <p class="small-text">
#         Explore historical information and understand
#         how the machine learning model works.
#         </p>

#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# # ============================================================
# # SYSTEM INFORMATION
# # ============================================================

# st.markdown("## 🧠 How the system works")

# st.markdown(
#     """
#     ```text
#     Weather Data
#           +
#     Terrain Data
#           +
#     Historical Landslide Records
#           ↓
#     Feature Engineering
#           ↓
#     XGBoost Machine Learning Model
#           ↓
#     District-Day Risk Estimate
#     ```
#     """
# )

# # ============================================================
# # MODEL INFORMATION
# # ============================================================

# if api_online:

#     try:

#         response = requests.get(
#             f"{API_URL}/api/model-info",
#             timeout=5
#         )

#         if response.status_code == 200:

#             model_info = response.json()

#             st.markdown("## 🤖 Current Model")

#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.metric(
#                     "Model",
#                     model_info.get(
#                         "model_name",
#                         "XGBoost"
#                     )
#                 )

#             with col2:
#                 st.metric(
#                     "Features",
#                     model_info.get(
#                         "number_of_features",
#                         27
#                     )
#                 )

#             with col3:
#                 st.metric(
#                     "Threshold",
#                     model_info.get(
#                         "threshold",
#                         0.49
#                     )
#                 )

#     except requests.exceptions.RequestException:

#         pass

# # ============================================================
# # DISCLAIMER
# # ============================================================

# st.markdown("---")

# st.caption(
#     """
#     ⚠️ LankaLandslide AI provides district-day machine-learning
#     risk estimates for research and decision-support purposes.
#     It is not an official landslide warning system and should
#     not replace information from Sri Lankan authorities.
#     """
# )
import streamlit as st
import requests
from datetime import date, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LankaLandslide AI",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

TODAY = date.today()
MAX_FORECAST_DATE = TODAY + timedelta(days=16)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌋 LankaLandslide AI")

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **Machine Learning-Based Landslide
    Risk Prediction and Location
    Intelligence System for Sri Lanka**
    """
)

st.sidebar.markdown("---")

st.sidebar.info(
    f"""
    **Prediction window**

    📚 Historical: from 1998

    📅 Today: {TODAY.strftime("%Y-%m-%d")}

    🔮 Future forecast:
    {TODAY.strftime("%Y-%m-%d")}
    → {MAX_FORECAST_DATE.strftime("%Y-%m-%d")}
    """
)


# ============================================================
# API HEALTH
# ============================================================

def check_api():

    try:

        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except Exception:

        return False


api_online = check_api()


if api_online:

    st.sidebar.success("🟢 API Online")

else:

    st.sidebar.error("🔴 API Offline")


# ============================================================
# TITLE
# ============================================================

st.title("🌋 LankaLandslide AI")

st.subheader(
    "Machine Learning-Based Landslide Risk Prediction "
    "and Location Intelligence System for Sri Lanka"
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    """
    LankaLandslide AI combines historical landslide records,
    weather conditions, rainfall accumulation, and terrain
    characteristics to estimate landslide risk at the
    **district-day level**.
    """
)


# ============================================================
# SYSTEM STATUS
# ============================================================

st.markdown("---")

st.header("📡 System Status")

col1, col2, col3 = st.columns(3)


with col1:

    if api_online:

        st.metric(
            "FastAPI",
            "Online"
        )

    else:

        st.metric(
            "FastAPI",
            "Offline"
        )


with col2:

    st.metric(
        "Model",
        "XGBoost"
    )


with col3:

    st.metric(
        "Features",
        "27"
    )


# ============================================================
# MODEL INFO
# ============================================================

if api_online:

    try:

        response = requests.get(
            f"{API_BASE_URL}/api/model-info",
            timeout=10
        )

        if response.status_code == 200:

            model_info = response.json()

            st.markdown("---")

            st.header("🤖 Current Model")

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Model",
                    model_info.get(
                        "model_name",
                        "XGBoost"
                    )
                )

            with c2:

                st.metric(
                    "Features",
                    model_info.get(
                        "number_of_features",
                        27
                    )
                )

            with c3:

                st.metric(
                    "Threshold",
                    model_info.get(
                        "threshold",
                        0.49
                    )
                )

    except Exception:

        pass


# ============================================================
# PREDICTION TYPES
# ============================================================

st.markdown("---")

st.header("🔮 Prediction Types")

c1, c2, c3 = st.columns(3)


with c1:

    st.info(
        """
        ### 📚 Historical

        Uses historical weather information
        for past dates.
        """
    )


with c2:

    st.info(
        """
        ### 📅 Today

        Uses current available weather
        information.
        """
    )


with c3:

    st.success(
        """
        ### 🔮 Future Forecast

        Uses forecast weather data for
        dates up to 16 days ahead.
        """
    )


# ============================================================
# WORKFLOW
# ============================================================

st.markdown("---")

st.header("⚙️ System Workflow")

st.markdown(
    """
    ```text
    Historical Landslide Records
                +
        Weather Data
                +
      Terrain Features
                ↓
       Feature Engineering
                ↓
         Machine Learning
                ↓
            XGBoost
                ↓
       Landslide Risk Score
                ↓
    Streamlit Dashboard
    ```
    """
)


# ============================================================
# FUTURE FORECAST EXPLANATION
# ============================================================

st.markdown("---")

st.header("🔮 Future Forecast Capability")

st.success(
    f"""
    Future predictions are available from today
    (**{TODAY.strftime("%Y-%m-%d")}**) through
    **{MAX_FORECAST_DATE.strftime("%Y-%m-%d")}**.

    Future predictions use forecast weather conditions,
    while historical dates use historical weather data.
    """
)


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown("---")

st.warning(
    """
    **Important:** LankaLandslide AI is a machine-learning
    decision-support system. It provides district-day risk
    estimates and should not be interpreted as an official
    landslide warning system or an exact prediction for a
    specific house, road, or location.
    """
)


st.caption(
    "LankaLandslide AI • XGBoost • FastAPI • Streamlit"
)