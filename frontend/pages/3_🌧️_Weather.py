# import streamlit as st
# import requests
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import date, timedelta

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Weather & Conditions | LankaLandslide AI",
#     page_icon="🌧️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # API CONFIGURATION
# # ============================================================

# API_URL = "http://127.0.0.1:8000"

# # ============================================================
# # DISTRICT COORDINATES
# # ============================================================

# district_coordinates = {
#     "Ampara": (7.2917, 81.6720),
#     "Anuradhapura": (8.3114, 80.4037),
#     "Badulla": (6.9934, 81.0550),
#     "Batticaloa": (7.7170, 81.7000),
#     "Colombo": (6.9271, 79.8612),
#     "Galle": (6.0329, 80.2168),
#     "Gampaha": (7.0840, 80.0098),
#     "Hambantota": (6.1429, 81.1212),
#     "Jaffna": (9.6615, 80.0255),
#     "Kalutara": (6.5854, 79.9607),
#     "Kandy": (7.2906, 80.6337),
#     "Kegalle": (7.2513, 80.3464),
#     "Kilinochchi": (9.3803, 80.3770),
#     "Kurunegala": (7.4863, 80.3647),
#     "Mannar": (8.9810, 79.9044),
#     "Matale": (7.4675, 80.6234),
#     "Matara": (5.9549, 80.5550),
#     "Monaragala": (6.8728, 81.3507),
#     "Nuwara Eliya": (6.9497, 80.7891),
#     "Polonnaruwa": (7.9403, 81.0188),
#     "Puttalam": (8.0362, 79.8283),
#     "Ratnapura": (6.6828, 80.3992),
#     "Trincomalee": (8.5874, 81.2152),
#     "Vavuniya": (8.7514, 80.4971)
# }

# DISTRICTS = list(district_coordinates.keys())

# # ============================================================
# # PAGE CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .page-title {
#         font-size: 42px;
#         font-weight: 800;
#         margin-bottom: 5px;
#     }

#     .page-subtitle {
#         font-size: 18px;
#         margin-bottom: 30px;
#     }

#     .section-title {
#         font-size: 25px;
#         font-weight: 700;
#         margin-top: 30px;
#         margin-bottom: 15px;
#     }

#     .weather-card {
#         padding: 20px;
#         border-radius: 15px;
#         border: 1px solid rgba(128,128,128,0.25);
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     '<div class="page-title">🌧️ Weather & Conditions</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="page-subtitle">'
#     'Explore rainfall, temperature and wind conditions '
#     'used by LankaLandslide AI.'
#     '</div>',
#     unsafe_allow_html=True
# )

# st.info(
#     """
#     🌦️ Weather information shown on this page is based on
#     the weather information retrieved by the LankaLandslide AI
#     backend for the selected district and date.
#     """
# )

# # ============================================================
# # DISTRICT AND DATE INPUT
# # ============================================================

# st.markdown(
#     '<div class="section-title">📍 Select Location & Date</div>',
#     unsafe_allow_html=True
# )

# col1, col2 = st.columns(2)

# with col1:

#     selected_district = st.selectbox(
#         "Select District",
#         DISTRICTS,
#         index=DISTRICTS.index("Colombo")
#     )

# with col2:

#     selected_date = st.date_input(
#         "Select Date",
#         value=date.today()
#     )

# # ============================================================
# # GET PREDICTION DATA
# # ============================================================

# if st.button(
#     "🌦️ Load Weather Conditions",
#     type="primary",
#     use_container_width=True
# ):

#     payload = {
#         "district": selected_district,
#         "prediction_date": selected_date.isoformat()
#     }

#     with st.spinner(
#         "Retrieving weather and environmental conditions..."
#     ):

#         try:

#             response = requests.post(
#                 f"{API_URL}/api/predict",
#                 json=payload,
#                 timeout=120
#             )

#             if response.status_code == 200:

#                 result = response.json()

#                 st.session_state["weather_result"] = result
#                 st.session_state["weather_district"] = selected_district
#                 st.session_state["weather_date"] = selected_date

#             else:

#                 st.error(
#                     f"Weather request failed. "
#                     f"API returned HTTP {response.status_code}."
#                 )

#                 try:
#                     st.json(response.json())
#                 except Exception:
#                     st.text(response.text)

#         except requests.exceptions.RequestException as error:

#             st.error(
#                 "Could not connect to the FastAPI backend."
#             )

#             st.code(str(error))


# # ============================================================
# # DISPLAY WEATHER RESULTS
# # ============================================================

# if "weather_result" in st.session_state:

#     result = st.session_state["weather_result"]

#     district = st.session_state["weather_district"]

#     selected_weather_date = st.session_state["weather_date"]

#     features = result.get(
#         "features_used",
#         {}
#     )

#     st.markdown("---")

#     st.markdown(
#         f"""
#         <div class="section-title">
#         🌦️ Weather Conditions — {district}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.caption(
#         f"Date: {selected_weather_date}"
#     )

#     # ========================================================
#     # CURRENT WEATHER METRICS
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '🌡️ Current Environmental Conditions'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:

#         rainfall = features.get(
#             "rainfall_mm",
#             0
#         )

#         st.metric(
#             "🌧️ Daily Rainfall",
#             f"{float(rainfall):.1f} mm"
#         )

#     with col2:

#         temperature = features.get(
#             "temp_mean",
#             0
#         )

#         st.metric(
#             "🌡️ Mean Temperature",
#             f"{float(temperature):.1f} °C"
#         )

#     with col3:

#         rain_hours = features.get(
#             "rain_hours",
#             0
#         )

#         st.metric(
#             "⏱️ Rain Hours",
#             f"{float(rain_hours):.0f} h"
#         )

#     with col4:

#         wind = features.get(
#             "wind_max",
#             0
#         )

#         st.metric(
#             "💨 Maximum Wind",
#             f"{float(wind):.1f} km/h"
#         )

#     # ========================================================
#     # TEMPERATURE INFORMATION
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '🌡️ Temperature'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)

#     with temp_col1:

#         st.metric(
#             "Maximum",
#             f"{float(features.get('temp_max', 0)):.1f} °C"
#         )

#     with temp_col2:

#         st.metric(
#             "Minimum",
#             f"{float(features.get('temp_min', 0)):.1f} °C"
#         )

#     with temp_col3:

#         st.metric(
#             "Mean",
#             f"{float(features.get('temp_mean', 0)):.1f} °C"
#         )

#     with temp_col4:

#         st.metric(
#             "Temperature Range",
#             f"{float(features.get('temperature_range', 0)):.1f} °C"
#         )

#     # ========================================================
#     # WIND INFORMATION
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '💨 Wind Conditions'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     wind_col1, wind_col2 = st.columns(2)

#     with wind_col1:

#         st.metric(
#             "Maximum Wind Speed",
#             f"{float(features.get('wind_max', 0)):.1f} km/h"
#         )

#     with wind_col2:

#         st.metric(
#             "Maximum Wind Gust",
#             f"{float(features.get('wind_gust_max', 0)):.1f} km/h"
#         )

#     # ========================================================
#     # RAINFALL ACCUMULATION
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '🌧️ Rainfall Accumulation'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     rainfall_values = {
#         "1 Day": float(
#             features.get(
#                 "rainfall_1day",
#                 0
#             )
#         ),

#         "3 Days": float(
#             features.get(
#                 "rainfall_3day",
#                 0
#             )
#         ),

#         "7 Days": float(
#             features.get(
#                 "rainfall_7day",
#                 0
#             )
#         ),

#         "14 Days": float(
#             features.get(
#                 "rainfall_14day",
#                 0
#             )
#         ),

#         "30 Days": float(
#             features.get(
#                 "rainfall_30day",
#                 0
#             )
#         )
#     }

#     rain_col1, rain_col2, rain_col3, rain_col4, rain_col5 = st.columns(5)

#     columns = [
#         rain_col1,
#         rain_col2,
#         rain_col3,
#         rain_col4,
#         rain_col5
#     ]

#     for column, (label, value) in zip(
#         columns,
#         rainfall_values.items()
#     ):

#         with column:

#             st.metric(
#                 label,
#                 f"{value:.1f} mm"
#             )

#     # ========================================================
#     # RAINFALL BAR CHART
#     # ========================================================

#     rainfall_df = pd.DataFrame(
#         {
#             "Period": list(
#                 rainfall_values.keys()
#             ),

#             "Rainfall (mm)": list(
#                 rainfall_values.values()
#             )
#         }
#     )

#     fig_rain = go.Figure()

#     fig_rain.add_trace(
#         go.Bar(
#             x=rainfall_df["Period"],
#             y=rainfall_df["Rainfall (mm)"],
#             text=[
#                 f"{value:.1f} mm"
#                 for value in rainfall_df["Rainfall (mm)"]
#             ],
#             textposition="outside"
#         )
#     )

#     fig_rain.update_layout(
#         title="Rainfall Accumulation",
#         xaxis_title="Accumulation Period",
#         yaxis_title="Rainfall (mm)",
#         height=450,
#         margin=dict(
#             l=20,
#             r=20,
#             t=60,
#             b=20
#         )
#     )

#     st.plotly_chart(
#         fig_rain,
#         use_container_width=True
#     )

#     # ========================================================
#     # RAINFALL AVERAGES
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '📈 Average Daily Rainfall'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     average_rainfall = {
#         "3-Day Average": float(
#             features.get(
#                 "rainfall_3day_avg",
#                 0
#             )
#         ),

#         "7-Day Average": float(
#             features.get(
#                 "rainfall_7day_avg",
#                 0
#             )
#         ),

#         "14-Day Average": float(
#             features.get(
#                 "rainfall_14day_avg",
#                 0
#             )
#         ),

#         "30-Day Average": float(
#             features.get(
#                 "rainfall_30day_avg",
#                 0
#             )
#         )
#     }

#     avg_df = pd.DataFrame(
#         {
#             "Period": list(
#                 average_rainfall.keys()
#             ),

#             "Average Rainfall (mm/day)": list(
#                 average_rainfall.values()
#             )
#         }
#     )

#     fig_avg = go.Figure()

#     fig_avg.add_trace(
#         go.Bar(
#             x=avg_df["Period"],
#             y=avg_df["Average Rainfall (mm/day)"],
#             text=[
#                 f"{value:.2f}"
#                 for value in avg_df[
#                     "Average Rainfall (mm/day)"
#                 ]
#             ],
#             textposition="outside"
#         )
#     )

#     fig_avg.update_layout(
#         title="Average Daily Rainfall",
#         xaxis_title="Period",
#         yaxis_title="Rainfall (mm/day)",
#         height=450,
#         margin=dict(
#             l=20,
#             r=20,
#             t=60,
#             b=20
#         )
#     )

#     st.plotly_chart(
#         fig_avg,
#         use_container_width=True
#     )

#     # ========================================================
#     # HEAVY RAIN INDICATORS
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '⛈️ Heavy Rainfall Indicators'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     heavy_rain = {
#         "10 mm": features.get(
#             "heavy_rain_10mm",
#             0
#         ),

#         "25 mm": features.get(
#             "heavy_rain_25mm",
#             0
#         ),

#         "50 mm": features.get(
#             "heavy_rain_50mm",
#             0
#         ),

#         "100 mm": features.get(
#             "heavy_rain_100mm",
#             0
#         )
#     }

#     h1, h2, h3, h4 = st.columns(4)

#     heavy_columns = [h1, h2, h3, h4]

#     for column, (threshold, value) in zip(
#         heavy_columns,
#         heavy_rain.items()
#     ):

#         with column:

#             if value == 1:

#                 st.warning(
#                     f"⚠️ {threshold} threshold exceeded"
#                 )

#             else:

#                 st.success(
#                     f"✓ {threshold} threshold not exceeded"
#                 )

#     # ========================================================
#     # WEATHER SUMMARY
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '📝 Weather Summary'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     daily_rainfall = float(
#         features.get(
#             "rainfall_mm",
#             0
#         )
#     )

#     seven_day = float(
#         features.get(
#             "rainfall_7day",
#             0
#         )
#     )

#     thirty_day = float(
#         features.get(
#             "rainfall_30day",
#             0
#         )
#     )

#     mean_temperature = float(
#         features.get(
#             "temp_mean",
#             0
#         )
#     )

#     max_wind = float(
#         features.get(
#             "wind_max",
#             0
#         )
#     )

#     summary_parts = []

#     if daily_rainfall > 50:

#         summary_parts.append(
#             "The selected date has substantial daily rainfall."
#         )

#     elif daily_rainfall > 25:

#         summary_parts.append(
#             "The selected date has notable daily rainfall."
#         )

#     elif daily_rainfall > 10:

#         summary_parts.append(
#             "The selected date has measurable rainfall."
#         )

#     else:

#         summary_parts.append(
#             "Daily rainfall is relatively low."
#         )

#     if seven_day > 100:

#         summary_parts.append(
#             "The recent 7-day accumulated rainfall is relatively high."
#         )

#     if thirty_day > 300:

#         summary_parts.append(
#             "The 30-day accumulated rainfall indicates "
#             "substantial longer-term wetness."
#         )

#     summary_parts.append(
#         f"The mean temperature is approximately "
#         f"{mean_temperature:.1f} °C."
#     )

#     summary_parts.append(
#         f"The maximum wind speed is approximately "
#         f"{max_wind:.1f} km/h."
#     )

#     st.write(
#         " ".join(summary_parts)
#     )

#     # ========================================================
#     # TERRAIN INFORMATION
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '⛰️ Terrain Information'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     terrain_col1, terrain_col2, terrain_col3, terrain_col4 = st.columns(4)

#     with terrain_col1:

#         st.metric(
#             "Mean Elevation",
#             f"{float(features.get('elevation_mean_m', 0)):.1f} m"
#         )

#     with terrain_col2:

#         st.metric(
#             "Maximum Elevation",
#             f"{float(features.get('elevation_max_m', 0)):.1f} m"
#         )

#     with terrain_col3:

#         st.metric(
#             "Mean Slope",
#             f"{float(features.get('slope_mean_deg', 0)):.1f}°"
#         )

#     with terrain_col4:

#         st.metric(
#             "Maximum Slope",
#             f"{float(features.get('slope_max_deg', 0)):.1f}°"
#         )

#     st.caption(
#         """
#         Terrain values represent statistics around the district
#         reference point used by the system. They are not a complete
#         district-wide terrain survey.
#         """
#     )

#     # ========================================================
#     # LINK WEATHER TO MODEL
#     # ========================================================

#     st.markdown(
#         '<div class="section-title">'
#         '🤖 Connection to Landslide Prediction'
#         '</div>',
#         unsafe_allow_html=True
#     )

#     prediction_probability = result.get(
#         "probability",
#         None
#     )

#     prediction_risk = result.get(
#         "risk",
#         "UNKNOWN"
#     )

#     if prediction_probability is not None:

#         st.metric(
#             "Model Estimated Probability",
#             f"{float(prediction_probability) * 100:.3f}%"
#         )

#         if str(prediction_risk).upper() == "HIGH":

#             st.error(
#                 f"Current model classification: **{prediction_risk}**"
#             )

#         elif str(prediction_risk).upper() == "MEDIUM":

#             st.warning(
#                 f"Current model classification: **{prediction_risk}**"
#             )

#         else:

#             st.success(
#                 f"Current model classification: **{prediction_risk}**"
#             )

#     # ========================================================
#     # RAW DATA
#     # ========================================================

#     with st.expander(
#         "🔍 View all weather and model features"
#     ):

#         st.json(features)

# # ============================================================
# # INITIAL INFORMATION
# # ============================================================

# else:

#     st.markdown("---")

#     st.info(
#         """
#         🌧️ Select a district and date above, then click
#         **Load Weather Conditions** to retrieve the environmental
#         conditions from the LankaLandslide AI backend.
#         """
#     )

# # ============================================================
# # DISCLAIMER
# # ============================================================

# st.markdown("---")

# st.caption(
#     """
#     ⚠️ Weather values shown here are environmental inputs and
#     derived rainfall features used by the machine-learning
#     system. They are not an official weather warning.
#     """
# )
import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Weather | LankaLandslide AI",
    page_icon="🌧️",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000"

TODAY = date.today()

MAX_FORECAST_DATE = TODAY + timedelta(days=16)


# ============================================================
# DISTRICTS
# ============================================================

DISTRICTS = [
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


# ============================================================
# HEADER
# ============================================================

st.title("🌧️ Weather & Environmental Conditions")

st.markdown(
    """
    Explore weather conditions used by LankaLandslide AI
    for landslide risk estimation.
    """
)


# ============================================================
# INPUT
# ============================================================

col1, col2 = st.columns(2)


with col1:

    district = st.selectbox(
        "Select District",
        DISTRICTS
    )


with col2:

    selected_date = st.date_input(
        "Weather Date",
        value=TODAY,
        min_value=date(1998, 1, 1),
        max_value=MAX_FORECAST_DATE
    )


# ============================================================
# DATE TYPE
# ============================================================

if selected_date < TODAY:

    date_type = "Historical"

elif selected_date == TODAY:

    date_type = "Today"

else:

    days_ahead = (
        selected_date - TODAY
    ).days

    date_type = "Forecast"


# ============================================================
# DATE LABEL
# ============================================================

if date_type == "Forecast":

    st.success(
        f"""
        🔮 **FORECAST WEATHER**

        Date: **{selected_date.strftime("%d %B %Y")}**

        Forecast horizon: **+{days_ahead} days**
        """
    )

elif date_type == "Today":

    st.info(
        f"""
        📅 **TODAY'S WEATHER**

        Date: **{selected_date.strftime("%d %B %Y")}**
        """
    )

else:

    st.info(
        f"""
        📚 **HISTORICAL WEATHER**

        Date: **{selected_date.strftime("%d %B %Y")}**
        """
    )


# ============================================================
# GET WEATHER
# ============================================================

if st.button(
    "🌧️ Get Weather Conditions",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Retrieving weather information..."
    ):

        try:

            response = requests.post(
                f"{API_BASE_URL}/api/predict",
                json={
                    "district": district,
                    "prediction_date":
                        selected_date.strftime("%Y-%m-%d")
                },
                timeout=120
            )


            if response.status_code != 200:

                st.error(
                    f"Weather request failed: "
                    f"HTTP {response.status_code}"
                )

                st.code(
                    response.text
                )

                st.stop()


            data = response.json()

            features = data.get(
                "features_used",
                {}
            )


        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

            st.stop()


    # ========================================================
    # MAIN WEATHER
    # ========================================================

    st.markdown("---")

    st.subheader("🌧️ Main Conditions")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Daily Rainfall",
            f"{float(features.get('rainfall_mm', 0)):.1f} mm"
        )


    with c2:

        st.metric(
            "Mean Temperature",
            f"{float(features.get('temp_mean', 0)):.1f} °C"
        )


    with c3:

        st.metric(
            "Rain Hours",
            f"{float(features.get('rain_hours', 0)):.0f} h"
        )


    with c4:

        st.metric(
            "Maximum Wind",
            f"{float(features.get('wind_max', 0)):.1f} km/h"
        )


    # ========================================================
    # TEMPERATURE
    # ========================================================

    st.markdown("---")

    st.subheader("🌡️ Temperature")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Maximum",
            f"{float(features.get('temp_max', 0)):.1f} °C"
        )


    with c2:

        st.metric(
            "Minimum",
            f"{float(features.get('temp_min', 0)):.1f} °C"
        )


    with c3:

        st.metric(
            "Mean",
            f"{float(features.get('temp_mean', 0)):.1f} °C"
        )


    with c4:

        st.metric(
            "Range",
            f"{float(features.get('temperature_range', 0)):.1f} °C"
        )


    # ========================================================
    # WIND
    # ========================================================

    st.markdown("---")

    st.subheader("💨 Wind")


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "Maximum Wind",
            f"{float(features.get('wind_max', 0)):.1f} km/h"
        )


    with c2:

        st.metric(
            "Maximum Gust",
            f"{float(features.get('wind_gust_max', 0)):.1f} km/h"
        )


    # ========================================================
    # RAINFALL
    # ========================================================

    st.markdown("---")

    st.subheader("💧 Rainfall Accumulation")


    rainfall_values = {
        "1 Day":
            features.get("rainfall_1day", 0),

        "3 Days":
            features.get("rainfall_3day", 0),

        "7 Days":
            features.get("rainfall_7day", 0),

        "14 Days":
            features.get("rainfall_14day", 0),

        "30 Days":
            features.get("rainfall_30day", 0)
    }


    rain_df = pd.DataFrame(
        {
            "Period":
                list(rainfall_values.keys()),

            "Rainfall (mm)":
                list(rainfall_values.values())
        }
    )


    st.bar_chart(
        rain_df.set_index("Period")
    )


    # ========================================================
    # HEAVY RAIN
    # ========================================================

    st.markdown("---")

    st.subheader("🌧️ Heavy Rainfall Indicators")


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "≥ 10 mm",
            int(features.get(
                "heavy_rain_10mm",
                0
            ))
        )


    with c2:

        st.metric(
            "≥ 25 mm",
            int(features.get(
                "heavy_rain_25mm",
                0
            ))
        )


    with c3:

        st.metric(
            "≥ 50 mm",
            int(features.get(
                "heavy_rain_50mm",
                0
            ))
        )


    with c4:

        st.metric(
            "≥ 100 mm",
            int(features.get(
                "heavy_rain_100mm",
                0
            ))
        )


    # ========================================================
    # MODEL CONNECTION
    # ========================================================

    st.markdown("---")

    st.subheader("🔮 Landslide Risk Connection")


    probability = data.get(
        "probability",
        0
    )

    risk = data.get(
        "risk",
        "UNKNOWN"
    )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "Model Probability",
            f"{float(probability):.2f}%"
        )


    with c2:

        st.metric(
            "Risk Level",
            risk
        )


    if date_type == "Forecast":

        st.info(
            f"""
            This is a **forecast-based weather and landslide
            risk estimate** for **+{days_ahead} days**.

            Forecast conditions may change when new weather
            forecasts become available.
            """
        )


    # ========================================================
    # TERRAIN
    # ========================================================

    st.markdown("---")

    st.subheader("⛰️ Terrain")


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Mean Elevation",
            f"{float(features.get('elevation_mean_m', 0)):.1f} m"
        )


    with c2:

        st.metric(
            "Mean Slope",
            f"{float(features.get('slope_mean_deg', 0)):.1f}°"
        )


    with c3:

        st.metric(
            "Maximum Slope",
            f"{float(features.get('slope_max_deg', 0)):.1f}°"
        )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown("---")

st.warning(
    """
    Weather conditions shown for future dates are forecast
    values. They should not be interpreted as guaranteed
    weather conditions.

    Terrain values are district-center-area summaries.
    """
)