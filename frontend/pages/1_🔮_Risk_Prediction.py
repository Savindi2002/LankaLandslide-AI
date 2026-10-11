# import streamlit as st
# import requests
# from datetime import date
# from datetime import date, timedelta

# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Risk Prediction | LankaLandslide AI",
#     page_icon="🔮",
#     layout="wide"
# )

# # ============================================================
# # API CONFIG
# # ============================================================

# API_URL = "http://127.0.0.1:8000"

# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .page-title {
#         font-size: 40px;
#         font-weight: 800;
#         margin-bottom: 5px;
#     }

#     .page-subtitle {
#         font-size: 18px;
#         margin-bottom: 30px;
#     }

#     .risk-box {
#         padding: 30px;
#         border-radius: 18px;
#         text-align: center;
#         border: 1px solid rgba(128,128,128,0.25);
#         margin: 20px 0;
#     }

#     .risk-title {
#         font-size: 18px;
#         font-weight: 600;
#     }

#     .risk-value {
#         font-size: 42px;
#         font-weight: 800;
#     }

#     .section-title {
#         font-size: 24px;
#         font-weight: 700;
#         margin-top: 25px;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     '<div class="page-title">🔮 Landslide Risk Prediction</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="page-subtitle">'
#     'Estimate district-day landslide risk using the LankaLandslide AI model.'
#     '</div>',
#     unsafe_allow_html=True
# )

# # ============================================================
# # GET DISTRICTS FROM API
# # ============================================================

# try:

#     district_response = requests.get(
#         f"{API_URL}/api/districts",
#         timeout=5
#     )

#     if district_response.status_code == 200:

#         district_data = district_response.json()

#         # Handle common API response formats
#         if isinstance(district_data, list):
#             districts = district_data

#         elif isinstance(district_data, dict):

#             if "districts" in district_data:
#                 districts = district_data["districts"]

#             elif "data" in district_data:
#                 districts = district_data["data"]

#             else:
#                 districts = []

#         else:
#             districts = []

#     else:
#         districts = []

# except requests.exceptions.RequestException:

#     districts = []

# # ============================================================
# # FALLBACK DISTRICTS
# # ============================================================

# if not districts:

#     districts = [
#         "Ampara",
#         "Anuradhapura",
#         "Badulla",
#         "Batticaloa",
#         "Colombo",
#         "Galle",
#         "Gampaha",
#         "Hambantota",
#         "Jaffna",
#         "Kalutara",
#         "Kandy",
#         "Kegalle",
#         "Kilinochchi",
#         "Kurunegala",
#         "Mannar",
#         "Matale",
#         "Matara",
#         "Monaragala",
#         "Nuwara Eliya",
#         "Polonnaruwa",
#         "Puttalam",
#         "Ratnapura",
#         "Trincomalee",
#         "Vavuniya"
#     ]

# # ============================================================
# # INPUT SECTION
# # ============================================================

# st.markdown(
#     '<div class="section-title">📍 Select Prediction Information</div>',
#     unsafe_allow_html=True
# )

# col1, col2 = st.columns(2)

# with col1:

#     district = st.selectbox(
#         "Select District",
#         districts
#     )

# with col2:

#     prediction_date = st.date_input(
#         "Prediction Date",
#         value=date.today()
#     )

# # ============================================================
# # PREDICT BUTTON
# # ============================================================

# st.markdown("")

# predict_button = st.button(
#     "🔮 Predict Landslide Risk",
#     type="primary",
#     use_container_width=True
# )

# # ============================================================
# # PREDICTION
# # ============================================================

# if predict_button:

#     payload = {
#         "district": district,
#         "prediction_date": prediction_date.isoformat()
#     }

#     with st.spinner("Analyzing weather, terrain and historical patterns..."):

#         try:

#             response = requests.post(
#                 f"{API_URL}/api/predict",
#                 json=payload,
#                 timeout=60
#             )

#             if response.status_code == 200:

#                 result = response.json()

#                 st.success("Prediction completed successfully.")

#                 # ====================================================
#                 # BASIC RESULTS
#                 # ====================================================

#                 risk = result.get(
#                     "risk",
#                     "UNKNOWN"
#                 )

#                 probability = float(
#                     result.get(
#                         "probability",
#                         0
#                     )
#                 )

#                 threshold = result.get(
#                     "threshold",
#                     0.49
#                 )

#                 model = result.get(
#                     "model",
#                     "XGBoost"
#                 )

#                 # ====================================================
#                 # RISK DISPLAY
#                 # ====================================================

#                 st.markdown(
#                     '<div class="section-title">'
#                     '📊 Prediction Result'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 result_col1, result_col2, result_col3 = st.columns(3)

#                 with result_col1:

#                     st.metric(
#                         "District",
#                         result.get(
#                             "district",
#                             district
#                         )
#                     )

#                 with result_col2:

#                     st.metric(
#                         "Prediction Date",
#                         result.get(
#                             "prediction_date",
#                             prediction_date.isoformat()
#                         )
#                     )

#                 with result_col3:

#                     st.metric(
#                         "Model",
#                         model
#                     )

#                 # ====================================================
#                 # RISK LEVEL
#                 # ====================================================

#                 if risk.upper() == "HIGH":

#                     st.error(
#                         f"🔴 **{risk} RISK**"
#                     )

#                 elif risk.upper() == "MEDIUM":

#                     st.warning(
#                         f"🟠 **{risk} RISK**"
#                     )

#                 elif risk.upper() == "LOW":

#                     st.success(
#                         f"🟢 **{risk} RISK**"
#                     )

#                 else:

#                     st.info(
#                         f"Risk classification: **{risk}**"
#                     )

#                 # ====================================================
#                 # PROBABILITY
#                 # ====================================================

#                 probability_percent = probability * 100

#                 st.markdown(
#                     '<div class="section-title">'
#                     '🎯 Estimated Risk Probability'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 st.progress(
#                     min(max(probability, 0.0), 1.0)
#                 )

#                 st.metric(
#                     "Estimated Probability",
#                     f"{probability_percent:.2f}%"
#                 )

#                 st.caption(
#                     f"Model decision threshold: {threshold:.2f}"
#                 )

#                 # ====================================================
#                 # MESSAGE
#                 # ====================================================

#                 message = result.get(
#                     "message",
#                     ""
#                 )

#                 if message:

#                     st.info(
#                         f"💡 {message}"
#                     )

#                 # ====================================================
#                 # WEATHER INFORMATION
#                 # ====================================================

#                 features = result.get(
#                     "features_used",
#                     {}
#                 )

#                 st.markdown(
#                     '<div class="section-title">'
#                     '🌧️ Weather Conditions'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 weather_col1, weather_col2, weather_col3, weather_col4 = st.columns(4)

#                 with weather_col1:

#                     st.metric(
#                         "Rainfall",
#                         f"{features.get('rainfall_mm', 0):.1f} mm"
#                     )

#                 with weather_col2:

#                     st.metric(
#                         "Temperature",
#                         f"{features.get('temp_mean', 0):.1f} °C"
#                     )

#                 with weather_col3:

#                     st.metric(
#                         "Rain Hours",
#                         f"{features.get('rain_hours', 0):.0f}"
#                     )

#                 with weather_col4:

#                     st.metric(
#                         "Wind",
#                         f"{features.get('wind_max', 0):.1f} km/h"
#                     )

#                 # ====================================================
#                 # RAINFALL HISTORY
#                 # ====================================================

#                 st.markdown(
#                     '<div class="section-title">'
#                     '🌧️ Recent Rainfall'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 rain_col1, rain_col2, rain_col3, rain_col4, rain_col5 = st.columns(5)

#                 with rain_col1:

#                     st.metric(
#                         "1 Day",
#                         f"{features.get('rainfall_1day', 0):.1f} mm"
#                     )

#                 with rain_col2:

#                     st.metric(
#                         "3 Days",
#                         f"{features.get('rainfall_3day', 0):.1f} mm"
#                     )

#                 with rain_col3:

#                     st.metric(
#                         "7 Days",
#                         f"{features.get('rainfall_7day', 0):.1f} mm"
#                     )

#                 with rain_col4:

#                     st.metric(
#                         "14 Days",
#                         f"{features.get('rainfall_14day', 0):.1f} mm"
#                     )

#                 with rain_col5:

#                     st.metric(
#                         "30 Days",
#                         f"{features.get('rainfall_30day', 0):.1f} mm"
#                     )

#                 # ====================================================
#                 # TERRAIN INFORMATION
#                 # ====================================================

#                 st.markdown(
#                     '<div class="section-title">'
#                     '⛰️ Terrain Characteristics'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 terrain_col1, terrain_col2, terrain_col3, terrain_col4 = st.columns(4)

#                 with terrain_col1:

#                     st.metric(
#                         "Mean Elevation",
#                         f"{features.get('elevation_mean_m', 0):.1f} m"
#                     )

#                 with terrain_col2:

#                     st.metric(
#                         "Maximum Elevation",
#                         f"{features.get('elevation_max_m', 0):.1f} m"
#                     )

#                 with terrain_col3:

#                     st.metric(
#                         "Mean Slope",
#                         f"{features.get('slope_mean_deg', 0):.1f}°"
#                     )

#                 with terrain_col4:

#                     st.metric(
#                         "Maximum Slope",
#                         f"{features.get('slope_max_deg', 0):.1f}°"
#                     )

#                 st.caption(
#                     "Terrain values represent statistics around the "
#                     "district reference point used by the system."
#                 )

#                 # ====================================================
#                 # MODEL INPUT INFORMATION
#                 # ====================================================

#                 with st.expander("🔍 View Model Input Features"):

#                     st.json(features)

#                 # ====================================================
#                 # INTERPRETATION
#                 # ====================================================

#                 st.markdown(
#                     '<div class="section-title">'
#                     '📝 Interpretation'
#                     '</div>',
#                     unsafe_allow_html=True
#                 )

#                 if risk.upper() == "HIGH":

#                     st.warning(
#                         "The model's estimated probability is at or "
#                         "above the configured decision threshold. "
#                         "This indicates a higher model-estimated "
#                         "district-day risk."
#                     )

#                 elif risk.upper() == "MEDIUM":

#                     st.warning(
#                         "The model indicates an intermediate "
#                         "district-day risk estimate. Monitor the "
#                         "environmental conditions and relevant "
#                         "official information."
#                     )

#                 else:

#                     st.success(
#                         "The model estimates a lower landslide risk "
#                         "for the selected district and date."
#                     )

#             else:

#                 st.error(
#                     f"Prediction failed. "
#                     f"API returned HTTP {response.status_code}."
#                 )

#                 try:

#                     error_data = response.json()

#                     st.json(error_data)

#                 except Exception:

#                     st.text(response.text)

#         except requests.exceptions.RequestException as error:

#             st.error(
#                 "Could not connect to the FastAPI backend."
#             )

#             st.code(
#                 str(error)
#             )

# # ============================================================
# # DISCLAIMER
# # ============================================================

# st.markdown("---")

# st.caption(
#     """
#     ⚠️ This prediction is a district-day machine-learning estimate
#     for research and decision-support purposes. It is not an
#     official landslide warning and should not replace information
#     from Sri Lankan authorities.
#     """
# )
import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Risk Prediction | LankaLandslide AI",
    page_icon="🔮",
    layout="wide"
)


# ============================================================
# API CONFIGURATION
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# DATE CONFIGURATION
# ============================================================

TODAY = date.today()

# LankaLandslide AI allows predictions up to 16 days ahead.
MAX_FORECAST_DATE = TODAY + timedelta(days=16)

MIN_DATE = date(1998, 1, 1)


# ============================================================
# HEADER
# ============================================================

st.title("🔮 Landslide Risk Prediction")

st.markdown(
    """
    Use LankaLandslide AI to estimate landslide risk for a
    selected Sri Lankan district and date.
    """
)


# ============================================================
# FORECAST INFORMATION BANNER
# ============================================================

st.info(
    f"""
    **Forecast availability:** {TODAY.strftime("%Y-%m-%d")}
    → {MAX_FORECAST_DATE.strftime("%Y-%m-%d")}

    Future dates use forecast weather data. Historical dates use
    historical weather data.
    """
)


# ============================================================
# GET DISTRICTS
# ============================================================

DEFAULT_DISTRICTS = [
    "Colombo",
    "Gampaha",
    "Kalutara",
    "Kandy",
    "Matale",
    "Nuwara Eliya",
    "Kegalle",
    "Ratnapura",
    "Galle",
    "Matara",
    "Hambantota",
    "Badulla",
    "Monaragala",
    "Kurunegala",
    "Puttalam",
    "Anuradhapura",
    "Polonnaruwa",
    "Jaffna",
    "Kilinochchi",
    "Mannar",
    "Vavuniya",
    "Trincomalee",
    "Batticaloa",
    "Ampara"
]


@st.cache_data(ttl=300)
def get_districts():

    try:

        response = requests.get(
            f"{API_BASE_URL}/api/districts",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # Handle different possible API response structures
        if isinstance(data, list):
            return data

        if isinstance(data, dict):

            if "districts" in data:
                return data["districts"]

        return DEFAULT_DISTRICTS

    except Exception:

        return DEFAULT_DISTRICTS


districts = get_districts()


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("📍 Prediction Settings")

col1, col2 = st.columns(2)


with col1:

    selected_district = st.selectbox(
        "Select District",
        districts,
        index=0
    )


with col2:

    selected_date = st.date_input(
        "Prediction Date",
        value=TODAY,
        min_value=MIN_DATE,
        max_value=MAX_FORECAST_DATE
    )


# ============================================================
# DATE TYPE
# ============================================================

if selected_date < TODAY:

    date_type = "historical"

    date_label = "Historical Prediction"

    date_icon = "📚"

    horizon_text = "Historical date"

elif selected_date == TODAY:

    date_type = "today"

    date_label = "Today's Prediction"

    date_icon = "📅"

    horizon_text = "Today"

else:

    date_type = "future"

    date_label = "Forecast-Based Prediction"

    date_icon = "🔮"

    forecast_days_ahead = (
        selected_date - TODAY
    ).days

    horizon_text = (
        f"+{forecast_days_ahead} day"
        if forecast_days_ahead == 1
        else f"+{forecast_days_ahead} days"
    )


# ============================================================
# DATE STATUS DISPLAY
# ============================================================

st.markdown("---")

if date_type == "future":

    st.success(
        f"""
        🔮 **Forecast-Based Prediction**

        **{selected_date.strftime("%d %B %Y")}** is
        **{forecast_days_ahead} day(s)** ahead of today.

        Weather conditions are obtained from the forecast API
        and then passed through the LankaLandslide AI model.
        """
    )

elif date_type == "today":

    st.info(
        f"""
        📅 **Today's Prediction**

        Prediction date: **{selected_date.strftime("%d %B %Y")}**
        """
    )

else:

    st.info(
        f"""
        📚 **Historical Prediction**

        Prediction date: **{selected_date.strftime("%d %B %Y")}**

        Historical weather data is used for this date.
        """
    )


# ============================================================
# PREDICTION BUTTON
# ============================================================

predict_button = st.button(
    "🔍 Predict Landslide Risk",
    type="primary",
    use_container_width=True
)


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    payload = {
        "district": selected_district,
        "prediction_date": selected_date.strftime("%Y-%m-%d")
    }

    with st.spinner(
        "Getting weather data and calculating landslide risk..."
    ):

        try:

            response = requests.post(
                f"{API_BASE_URL}/api/predict",
                json=payload,
                timeout=120
            )

            # ------------------------------------------------
            # API ERROR
            # ------------------------------------------------

            if response.status_code != 200:

                st.error(
                    f"Prediction failed. "
                    f"API returned HTTP {response.status_code}."
                )

                try:

                    error_data = response.json()

                    st.code(
                        str(error_data),
                        language="json"
                    )

                except Exception:

                    st.code(
                        response.text
                    )

                st.stop()

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error(
                """
                ❌ Cannot connect to the LankaLandslide AI API.

                Please make sure FastAPI is running:

                `uvicorn main:app --reload`
                """
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                """
                ⏱️ The prediction request timed out.

                The weather API may be taking too long to respond.
                Please try again.
                """
            )

            st.stop()

        except Exception as e:

            st.error(
                f"Unexpected error: {str(e)}"
            )

            st.stop()


    # ========================================================
    # EXTRACT RESULT
    # ========================================================

    probability = float(
        result.get("probability", 0)
    )

    risk = result.get(
        "risk",
        "UNKNOWN"
    )

    threshold = float(
        result.get("threshold", 0.49)
    )

    model_name = result.get(
        "model",
        "XGBoost"
    )

    features = result.get(
        "features_used",
        {}
    )

    message = result.get(
        "message",
        ""
    )


    # ========================================================
    # PREDICTION HEADER
    # ========================================================

    st.markdown("---")

    st.subheader(
        f"{date_icon} Prediction Result"
    )

    # ========================================================
    # FORECAST LABEL
    # ========================================================

    if date_type == "future":

        st.warning(
            f"""
            🔮 **FORECAST-BASED PREDICTION**

            District: **{selected_district}**

            Date: **{selected_date.strftime("%d %B %Y")}**

            Forecast horizon: **{horizon_text}**

            The model is using forecast weather conditions for
            the selected future date.
            """
        )

    elif date_type == "today":

        st.info(
            f"""
            📅 **TODAY'S PREDICTION**

            District: **{selected_district}**

            Date: **{selected_date.strftime("%d %B %Y")}**
            """
        )

    else:

        st.info(
            f"""
            📚 **HISTORICAL PREDICTION**

            District: **{selected_district}**

            Date: **{selected_date.strftime("%d %B %Y")}**
            """
        )


    # ========================================================
    # RISK DISPLAY
    # ========================================================

    risk_col1, risk_col2, risk_col3 = st.columns(3)


    with risk_col1:

        st.metric(
            "Risk Level",
            risk
        )


    with risk_col2:

        st.metric(
            "Estimated Probability",
            f"{probability:.2f}%"
        )


    with risk_col3:

        st.metric(
            "Model Threshold",
            f"{threshold:.2f}"
        )


    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    st.markdown("---")

    info_col1, info_col2, info_col3, info_col4 = st.columns(4)


    with info_col1:

        st.metric(
            "District",
            selected_district
        )


    with info_col2:

        st.metric(
            "Prediction Date",
            selected_date.strftime("%Y-%m-%d")
        )


    with info_col3:

        st.metric(
            "Forecast Horizon",
            horizon_text
        )


    with info_col4:

        st.metric(
            "Model",
            model_name
        )


    # ========================================================
    # RISK INTERPRETATION
    # ========================================================

    st.markdown("---")

    st.subheader("📊 Risk Interpretation")


    if risk == "HIGH":

        st.error(
            """
            ⚠️ **HIGH RISK**

            The model estimates elevated landslide risk for
            this district and date based on the available
            environmental conditions.
            """
        )

    elif risk == "MEDIUM":

        st.warning(
            """
            ⚠️ **MEDIUM RISK**

            The model estimates moderate landslide risk for
            this district and date.
            """
        )

    elif risk == "LOW":

        st.success(
            """
            ✅ **LOW RISK**

            The model estimates lower landslide risk for
            this district and date.
            """
        )

    else:

        st.info(
            f"""
            Model result: **{risk}**
            """
        )


    if message:

        st.caption(
            message
        )


    # ========================================================
    # WEATHER CONDITIONS
    # ========================================================

    st.markdown("---")

    st.subheader("🌧️ Weather Conditions")


    weather_col1, weather_col2, weather_col3, weather_col4 = (
        st.columns(4)
    )


    rainfall_mm = features.get(
        "rainfall_mm",
        0
    )

    rain_hours = features.get(
        "rain_hours",
        0
    )

    temp_mean = features.get(
        "temp_mean",
        0
    )

    wind_max = features.get(
        "wind_max",
        0
    )


    with weather_col1:

        st.metric(
            "Daily Rainfall",
            f"{float(rainfall_mm):.1f} mm"
        )


    with weather_col2:

        st.metric(
            "Rain Hours",
            f"{float(rain_hours):.0f} h"
        )


    with weather_col3:

        st.metric(
            "Mean Temperature",
            f"{float(temp_mean):.1f} °C"
        )


    with weather_col4:

        st.metric(
            "Maximum Wind",
            f"{float(wind_max):.1f} km/h"
        )


    # ========================================================
    # TEMPERATURE
    # ========================================================

    st.markdown("### 🌡️ Temperature")

    temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)


    temp_max = features.get(
        "temp_max",
        0
    )

    temp_min = features.get(
        "temp_min",
        0
    )

    temperature_range = features.get(
        "temperature_range",
        0
    )

    with temp_col1:

        st.metric(
            "Maximum",
            f"{float(temp_max):.1f} °C"
        )


    with temp_col2:

        st.metric(
            "Minimum",
            f"{float(temp_min):.1f} °C"
        )


    with temp_col3:

        st.metric(
            "Mean",
            f"{float(temp_mean):.1f} °C"
        )


    with temp_col4:

        st.metric(
            "Temperature Range",
            f"{float(temperature_range):.1f} °C"
        )


    # ========================================================
    # WIND
    # ========================================================

    st.markdown("### 💨 Wind")

    wind_col1, wind_col2 = st.columns(2)


    wind_gust = features.get(
        "wind_gust_max",
        0
    )


    with wind_col1:

        st.metric(
            "Maximum Wind",
            f"{float(wind_max):.1f} km/h"
        )


    with wind_col2:

        st.metric(
            "Maximum Wind Gust",
            f"{float(wind_gust):.1f} km/h"
        )


    # ========================================================
    # RAINFALL ACCUMULATION
    # ========================================================

    st.markdown("---")

    st.subheader("💧 Rainfall Accumulation")


    rain_col1, rain_col2, rain_col3, rain_col4, rain_col5 = (
        st.columns(5)
    )


    rainfall_1day = features.get(
        "rainfall_1day",
        0
    )

    rainfall_3day = features.get(
        "rainfall_3day",
        0
    )

    rainfall_7day = features.get(
        "rainfall_7day",
        0
    )

    rainfall_14day = features.get(
        "rainfall_14day",
        0
    )

    rainfall_30day = features.get(
        "rainfall_30day",
        0
    )


    with rain_col1:

        st.metric(
            "1 Day",
            f"{float(rainfall_1day):.1f} mm"
        )


    with rain_col2:

        st.metric(
            "3 Days",
            f"{float(rainfall_3day):.1f} mm"
        )


    with rain_col3:

        st.metric(
            "7 Days",
            f"{float(rainfall_7day):.1f} mm"
        )


    with rain_col4:

        st.metric(
            "14 Days",
            f"{float(rainfall_14day):.1f} mm"
        )


    with rain_col5:

        st.metric(
            "30 Days",
            f"{float(rainfall_30day):.1f} mm"
        )


    # ========================================================
    # RAINFALL CHART
    # ========================================================

    rainfall_chart_data = pd.DataFrame(
        {
            "Period": [
                "1 Day",
                "3 Days",
                "7 Days",
                "14 Days",
                "30 Days"
            ],
            "Rainfall (mm)": [
                rainfall_1day,
                rainfall_3day,
                rainfall_7day,
                rainfall_14day,
                rainfall_30day
            ]
        }
    )


    st.bar_chart(
        rainfall_chart_data.set_index("Period")
    )


    # ========================================================
    # RAINFALL AVERAGES
    # ========================================================

    st.subheader("📈 Average Daily Rainfall")


    avg_data = pd.DataFrame(
        {
            "Period": [
                "3 Days",
                "7 Days",
                "14 Days",
                "30 Days"
            ],
            "Average Rainfall (mm/day)": [
                features.get(
                    "rainfall_3day_avg",
                    0
                ),
                features.get(
                    "rainfall_7day_avg",
                    0
                ),
                features.get(
                    "rainfall_14day_avg",
                    0
                ),
                features.get(
                    "rainfall_30day_avg",
                    0
                )
            ]
        }
    )


    st.bar_chart(
        avg_data.set_index("Period")
    )


    # ========================================================
    # HEAVY RAIN INDICATORS
    # ========================================================

    st.markdown("---")

    st.subheader("🌧️ Heavy Rainfall Indicators")


    heavy_col1, heavy_col2, heavy_col3, heavy_col4 = (
        st.columns(4)
    )


    heavy_10 = features.get(
        "heavy_rain_10mm",
        0
    )

    heavy_25 = features.get(
        "heavy_rain_25mm",
        0
    )

    heavy_50 = features.get(
        "heavy_rain_50mm",
        0
    )

    heavy_100 = features.get(
        "heavy_rain_100mm",
        0
    )


    with heavy_col1:

        st.metric(
            "≥ 10 mm",
            int(heavy_10)
        )


    with heavy_col2:

        st.metric(
            "≥ 25 mm",
            int(heavy_25)
        )


    with heavy_col3:

        st.metric(
            "≥ 50 mm",
            int(heavy_50)
        )


    with heavy_col4:

        st.metric(
            "≥ 100 mm",
            int(heavy_100)
        )


    # ========================================================
    # TERRAIN INFORMATION
    # ========================================================

    st.markdown("---")

    st.subheader("⛰️ Terrain Information")


    terrain_col1, terrain_col2, terrain_col3 = st.columns(3)


    elevation_mean = features.get(
        "elevation_mean_m",
        0
    )

    elevation_max = features.get(
        "elevation_max_m",
        0
    )

    elevation_min = features.get(
        "elevation_min_m",
        0
    )

    slope_mean = features.get(
        "slope_mean_deg",
        0
    )

    slope_max = features.get(
        "slope_max_deg",
        0
    )


    with terrain_col1:

        st.metric(
            "Mean Elevation",
            f"{float(elevation_mean):.1f} m"
        )

        st.metric(
            "Minimum Elevation",
            f"{float(elevation_min):.1f} m"
        )


    with terrain_col2:

        st.metric(
            "Maximum Elevation",
            f"{float(elevation_max):.1f} m"
        )

        st.metric(
            "Mean Slope",
            f"{float(slope_mean):.1f}°"
        )


    with terrain_col3:

        st.metric(
            "Maximum Slope",
            f"{float(slope_max):.1f}°"
        )


    # ========================================================
    # FUTURE FORECAST NOTICE
    # ========================================================

    if date_type == "future":

        st.markdown("---")

        st.subheader("🔮 Forecast Information")

        st.info(
            f"""
            **Forecast horizon:** {horizon_text}

            The selected date is within the available
            16-day forecast window.

            Weather variables for the future date are based on
            forecast weather data rather than observed weather.

            Therefore, the landslide probability should be
            interpreted as a **forecast-based model estimate**.
            """
        )


    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    st.markdown("---")

    st.subheader("🤖 Model Information")


    model_col1, model_col2, model_col3 = st.columns(3)


    with model_col1:

        st.metric(
            "Model",
            model_name
        )


    with model_col2:

        st.metric(
            "Features",
            "27"
        )


    with model_col3:

        st.metric(
            "Decision Threshold",
            f"{threshold:.2f}"
        )


    # ========================================================
    # RAW FEATURES
    # ========================================================

    with st.expander(
        "🔍 View Model Features"
    ):

        feature_df = pd.DataFrame(
            [
                {
                    "Feature": key,
                    "Value": value
                }
                for key, value in features.items()
            ]
        )

        st.dataframe(
            feature_df,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # IMPORTANT LIMITATIONS
    # ========================================================

    st.markdown("---")

    st.subheader("⚠️ Important Limitations")

    st.warning(
        """
        **This system is a machine-learning decision-support
        application, not an official landslide warning system.**

        • Predictions represent **district-day risk**.

        • They do not identify an exact house, road, or
          individual slope.

        • Future predictions depend on forecast weather data,
          which can change as new weather forecasts are issued.

        • Historical "no landslide" days represent days without
          recorded events in the dataset and do not prove that
          no landslide occurred.

        • Terrain values are district-center-area summaries.

        • Future risk estimates should therefore be interpreted
          as model-based estimates rather than guaranteed
          outcomes.
        """
    )


# ============================================================
# NO PREDICTION YET
# ============================================================

else:

    st.markdown("---")

    st.subheader("📌 Ready to Predict")

    if date_type == "future":

        days_ahead = (
            selected_date - TODAY
        ).days

        st.info(
            f"""
            Select **{selected_district}** and click
            **Predict Landslide Risk**.

            🔮 This will generate a **+{days_ahead} day
            forecast-based landslide risk prediction** for
            {selected_date.strftime("%d %B %Y")}.
            """
        )

    elif date_type == "today":

        st.info(
            """
            Select a district and click
            **Predict Landslide Risk** to generate today's
            landslide risk estimate.
            """
        )

    else:

        st.info(
            """
            Select a district and click
            **Predict Landslide Risk** to generate a historical
            landslide risk estimate.
            """
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔮 Risk Prediction")

    st.markdown("---")

    st.markdown(
        "### Prediction Window"
    )

    st.write(
        f"📅 Today: **{TODAY.strftime('%Y-%m-%d')}**"
    )

    st.write(
        f"🔮 Maximum forecast: **{MAX_FORECAST_DATE.strftime('%Y-%m-%d')}**"
    )

    st.write(
        "📚 Historical data: from 1998"
    )

    st.markdown("---")

    st.markdown(
        """
        ### Prediction Types

        📚 **Historical**

        Uses historical weather data.

        📅 **Today**

        Uses current/forecast weather information.

        🔮 **Future**

        Uses forecast weather data up to
        the available forecast horizon.
        """
    )

    st.markdown("---")

    st.caption(
        "LankaLandslide AI • XGBoost"
    )