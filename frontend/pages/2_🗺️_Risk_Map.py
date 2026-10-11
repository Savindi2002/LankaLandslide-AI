# # import streamlit as st
# # import requests
# # import pandas as pd
# # import plotly.express as px
# # from datetime import date

# # # ============================================================
# # # PAGE CONFIGURATION
# # # ============================================================

# # st.set_page_config(
# #     page_title="Risk Map | LankaLandslide AI",
# #     page_icon="🗺️",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # ============================================================
# # # API CONFIGURATION
# # # ============================================================

# # API_URL = "http://127.0.0.1:8000"

# # # ============================================================
# # # PAGE CSS
# # # ============================================================

# # st.markdown(
# #     """
# #     <style>

# #     .page-title {
# #         font-size: 42px;
# #         font-weight: 800;
# #         margin-bottom: 5px;
# #     }

# #     .page-subtitle {
# #         font-size: 18px;
# #         margin-bottom: 25px;
# #     }

# #     .section-title {
# #         font-size: 25px;
# #         font-weight: 700;
# #         margin-top: 25px;
# #         margin-bottom: 15px;
# #     }

# #     </style>
# #     """,
# #     unsafe_allow_html=True
# # )

# # # ============================================================
# # # SRI LANKA DISTRICT COORDINATES
# # # ============================================================

# # district_coordinates = {

# #     "Ampara": {
# #         "latitude": 7.2917,
# #         "longitude": 81.6720
# #     },

# #     "Anuradhapura": {
# #         "latitude": 8.3114,
# #         "longitude": 80.4037
# #     },

# #     "Badulla": {
# #         "latitude": 6.9934,
# #         "longitude": 81.0550
# #     },

# #     "Batticaloa": {
# #         "latitude": 7.7170,
# #         "longitude": 81.7000
# #     },

# #     "Colombo": {
# #         "latitude": 6.9271,
# #         "longitude": 79.8612
# #     },

# #     "Galle": {
# #         "latitude": 6.0329,
# #         "longitude": 80.2168
# #     },

# #     "Gampaha": {
# #         "latitude": 7.0840,
# #         "longitude": 80.0098
# #     },

# #     "Hambantota": {
# #         "latitude": 6.1429,
# #         "longitude": 81.1212
# #     },

# #     "Jaffna": {
# #         "latitude": 9.6615,
# #         "longitude": 80.0255
# #     },

# #     "Kalutara": {
# #         "latitude": 6.5854,
# #         "longitude": 79.9607
# #     },

# #     "Kandy": {
# #         "latitude": 7.2906,
# #         "longitude": 80.6337
# #     },

# #     "Kegalle": {
# #         "latitude": 7.2513,
# #         "longitude": 80.3464
# #     },

# #     "Kilinochchi": {
# #         "latitude": 9.3803,
# #         "longitude": 80.3770
# #     },

# #     "Kurunegala": {
# #         "latitude": 7.4863,
# #         "longitude": 80.3647
# #     },

# #     "Mannar": {
# #         "latitude": 8.9810,
# #         "longitude": 79.9044
# #     },

# #     "Matale": {
# #         "latitude": 7.4675,
# #         "longitude": 80.6234
# #     },

# #     "Matara": {
# #         "latitude": 5.9549,
# #         "longitude": 80.5550
# #     },

# #     "Monaragala": {
# #         "latitude": 6.8728,
# #         "longitude": 81.3507
# #     },

# #     "Nuwara Eliya": {
# #         "latitude": 6.9497,
# #         "longitude": 80.7891
# #     },

# #     "Polonnaruwa": {
# #         "latitude": 7.9403,
# #         "longitude": 81.0188
# #     },

# #     "Puttalam": {
# #         "latitude": 8.0362,
# #         "longitude": 79.8283
# #     },

# #     "Ratnapura": {
# #         "latitude": 6.6828,
# #         "longitude": 80.3992
# #     },

# #     "Trincomalee": {
# #         "latitude": 8.5874,
# #         "longitude": 81.2152
# #     },

# #     "Vavuniya": {
# #         "latitude": 8.7514,
# #         "longitude": 80.4971
# #     }
# # }

# # # ============================================================
# # # HEADER
# # # ============================================================

# # st.markdown(
# #     '<div class="page-title">🗺️ Sri Lanka Landslide Risk Map</div>',
# #     unsafe_allow_html=True
# # )

# # st.markdown(
# #     '<div class="page-subtitle">'
# #     'Explore machine-learning-based landslide risk estimates '
# #     'across Sri Lankan districts.'
# #     '</div>',
# #     unsafe_allow_html=True
# # )

# # st.info(
# #     """
# #     📍 The map displays district-day risk estimates.

# #     The markers represent district reference locations and
# #     should not be interpreted as exact landslide locations.
# #     """
# # )

# # # ============================================================
# # # DATE SELECTION
# # # ============================================================

# # st.markdown(
# #     '<div class="section-title">📅 Select Prediction Date</div>',
# #     unsafe_allow_html=True
# # )

# # selected_date = st.date_input(
# #     "Prediction date",
# #     value=date.today()
# # )

# # # ============================================================
# # # GENERATE MAP BUTTON
# # # ============================================================

# # generate_map = st.button(
# #     "🗺️ Generate Sri Lanka Risk Map",
# #     type="primary",
# #     width="stretch"
# # )

# # # ============================================================
# # # API PREDICTION FUNCTION
# # # ============================================================

# # def get_prediction(district, prediction_date):

# #     payload = {
# #         "district": district,
# #         "prediction_date": prediction_date.isoformat()
# #     }

# #     try:

# #         response = requests.post(
# #             f"{API_URL}/api/predict",
# #             json=payload,
# #             timeout=120
# #         )

# #         # ----------------------------------------------------
# #         # SUCCESS
# #         # ----------------------------------------------------

# #         if response.status_code == 200:

# #             try:

# #                 return response.json()

# #             except ValueError:

# #                 return {
# #                     "error": True,
# #                     "message": "Backend returned invalid JSON."
# #                 }

# #         # ----------------------------------------------------
# #         # API ERROR
# #         # ----------------------------------------------------

# #         return {
# #             "error": True,
# #             "status_code": response.status_code,
# #             "message": response.text
# #         }

# #     except requests.exceptions.Timeout:

# #         return {
# #             "error": True,
# #             "message": "Prediction request timed out."
# #         }

# #     except requests.exceptions.ConnectionError:

# #         return {
# #             "error": True,
# #             "message": (
# #                 "Could not connect to the FastAPI backend."
# #             )
# #         }

# #     except requests.exceptions.RequestException as error:

# #         return {
# #             "error": True,
# #             "message": str(error)
# #         }


# # # ============================================================
# # # GENERATE PREDICTIONS
# # # ============================================================

# # if generate_map:

# #     st.markdown("---")

# #     st.markdown(
# #         '<div class="section-title">'
# #         '🔄 Generating District Predictions'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     progress_bar = st.progress(0)

# #     status_text = st.empty()

# #     results = []

# #     total_districts = len(
# #         district_coordinates
# #     )

# #     for index, district in enumerate(
# #         district_coordinates.keys()
# #     ):

# #         status_text.write(
# #             f"Analyzing **{district}**..."
# #         )

# #         prediction = get_prediction(
# #             district,
# #             selected_date
# #         )

# #         latitude = district_coordinates[
# #             district
# #         ]["latitude"]

# #         longitude = district_coordinates[
# #             district
# #         ]["longitude"]

# #         # ====================================================
# #         # SUCCESSFUL PREDICTION
# #         # ====================================================

# #         if (
# #             prediction
# #             and not prediction.get(
# #                 "error",
# #                 False
# #             )
# #         ):

# #             raw_probability = prediction.get(
# #                 "probability"
# #             )

# #             # ------------------------------------------------
# #             # Safely convert probability
# #             # ------------------------------------------------

# #             try:

# #                 if raw_probability is None:

# #                     probability = None

# #                 else:

# #                     probability = float(
# #                         raw_probability
# #                     )

# #             except (
# #                 TypeError,
# #                 ValueError
# #             ):

# #                 probability = None

# #             # ------------------------------------------------
# #             # Risk
# #             # ------------------------------------------------

# #             risk = prediction.get(
# #                 "risk",
# #                 "Unavailable"
# #             )

# #             if risk is None:

# #                 risk = "Unavailable"

# #             risk = str(risk).upper()

# #             # ------------------------------------------------
# #             # Features
# #             # ------------------------------------------------

# #             features = prediction.get(
# #                 "features_used",
# #                 {}
# #             )

# #             if not isinstance(
# #                 features,
# #                 dict
# #             ):

# #                 features = {}

# #             # ------------------------------------------------
# #             # Probability percentage
# #             # ------------------------------------------------

# #             if probability is not None:

# #                 probability_percent = (
# #                     probability * 100
# #                 )

# #             else:

# #                 probability_percent = None

# #             # ------------------------------------------------
# #             # Store result
# #             # ------------------------------------------------

# #             results.append(
# #                 {
# #                     "district": district,

# #                     "latitude": latitude,

# #                     "longitude": longitude,

# #                     "probability": probability,

# #                     "probability_percent":
# #                         probability_percent,

# #                     "risk": risk,

# #                     "rainfall_mm":
# #                         features.get(
# #                             "rainfall_mm"
# #                         ),

# #                     "rainfall_1day":
# #                         features.get(
# #                             "rainfall_1day"
# #                         ),

# #                     "rainfall_3day":
# #                         features.get(
# #                             "rainfall_3day"
# #                         ),

# #                     "rainfall_7day":
# #                         features.get(
# #                             "rainfall_7day"
# #                         ),

# #                     "rainfall_14day":
# #                         features.get(
# #                             "rainfall_14day"
# #                         ),

# #                     "rainfall_30day":
# #                         features.get(
# #                             "rainfall_30day"
# #                         ),

# #                     "temp_mean":
# #                         features.get(
# #                             "temp_mean"
# #                         ),

# #                     "wind_max":
# #                         features.get(
# #                             "wind_max"
# #                         )
# #                 }
# #             )

# #         # ====================================================
# #         # FAILED / UNAVAILABLE PREDICTION
# #         # ====================================================

# #         else:

# #             results.append(
# #                 {
# #                     "district": district,

# #                     "latitude": latitude,

# #                     "longitude": longitude,

# #                     "probability": None,

# #                     "probability_percent": None,

# #                     "risk": "UNAVAILABLE",

# #                     "rainfall_mm": None,

# #                     "rainfall_1day": None,

# #                     "rainfall_3day": None,

# #                     "rainfall_7day": None,

# #                     "rainfall_14day": None,

# #                     "rainfall_30day": None,

# #                     "temp_mean": None,

# #                     "wind_max": None
# #                 }
# #             )

# #         # ----------------------------------------------------
# #         # Update progress
# #         # ----------------------------------------------------

# #         progress_bar.progress(
# #             int(
# #                 ((index + 1) / total_districts)
# #                 * 100
# #             )
# #         )

# #     status_text.success(
# #         "✅ District predictions completed."
# #     )

# #     # ========================================================
# #     # CREATE DATAFRAME
# #     # ========================================================

# #     map_df = pd.DataFrame(results)

# #     # ========================================================
# #     # CONVERT NUMERIC COLUMNS SAFELY
# #     # ========================================================

# #     numeric_columns = [
# #         "probability",
# #         "probability_percent",
# #         "rainfall_mm",
# #         "rainfall_1day",
# #         "rainfall_3day",
# #         "rainfall_7day",
# #         "rainfall_14day",
# #         "rainfall_30day",
# #         "temp_mean",
# #         "wind_max"
# #     ]

# #     for column in numeric_columns:

# #         map_df[column] = pd.to_numeric(
# #             map_df[column],
# #             errors="coerce"
# #         )

# #     # ========================================================
# #     # SAVE SESSION STATE
# #     # ========================================================

# #     st.session_state[
# #         "risk_map_data"
# #     ] = map_df

# #     st.session_state[
# #         "risk_map_date"
# #     ] = selected_date


# # # ============================================================
# # # DISPLAY RESULTS
# # # ============================================================

# # if "risk_map_data" in st.session_state:

# #     map_df = st.session_state[
# #         "risk_map_data"
# #     ]

# #     map_date = st.session_state[
# #         "risk_map_date"
# #     ]

# #     st.markdown("---")

# #     st.markdown(
# #         f"""
# #         <div class="section-title">
# #         🌍 District Risk Overview — {map_date}
# #         </div>
# #         """,
# #         unsafe_allow_html=True
# #     )

# #     # ========================================================
# #     # RISK COUNTS
# #     # ========================================================

# #     risk_values = (
# #         map_df["risk"]
# #         .fillna("UNAVAILABLE")
# #         .astype(str)
# #         .str.upper()
# #     )

# #     high_count = (
# #         risk_values == "HIGH"
# #     ).sum()

# #     medium_count = (
# #         risk_values == "MEDIUM"
# #     ).sum()

# #     low_count = (
# #         risk_values == "LOW"
# #     ).sum()

# #     unavailable_count = (
# #         risk_values == "UNAVAILABLE"
# #     ).sum()

# #     # ========================================================
# #     # METRICS
# #     # ========================================================

# #     col1, col2, col3, col4 = st.columns(4)

# #     with col1:

# #         st.metric(
# #             "🔴 High Risk",
# #             int(high_count)
# #         )

# #     with col2:

# #         st.metric(
# #             "🟠 Medium Risk",
# #             int(medium_count)
# #         )

# #     with col3:

# #         st.metric(
# #             "🟢 Low Risk",
# #             int(low_count)
# #         )

# #     with col4:

# #         st.metric(
# #             "⚪ Unavailable",
# #             int(unavailable_count)
# #         )

# #     # ========================================================
# #     # VALID MAP DATA
# #     # ========================================================

# #     valid_map_df = map_df[
# #         map_df["probability"].notna()
# #     ].copy()

# #     # ========================================================
# #     # INTERACTIVE MAP
# #     # ========================================================

# #     st.markdown(
# #         '<div class="section-title">'
# #         '🗺️ Interactive Risk Map'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     if len(valid_map_df) > 0:

# #         # ----------------------------------------------------
# #         # Marker size
# #         #
# #         # Give every marker a visible minimum size.
# #         # This prevents low probabilities from becoming tiny.
# #         # ----------------------------------------------------

# #         valid_map_df["marker_size"] = (
# #             valid_map_df[
# #                 "probability_percent"
# #             ]
# #             .clip(
# #                 lower=5,
# #                 upper=100
# #             )
# #         )

# #         # ----------------------------------------------------
# #         # Plotly interactive map
# #         # ----------------------------------------------------

# #         fig = px.scatter_map(
# #             valid_map_df,

# #             lat="latitude",

# #             lon="longitude",

# #             color="risk",

# #             size="marker_size",

# #             size_max=35,

# #             hover_name="district",

# #             hover_data={
# #                 "probability_percent": ":.3f",

# #                 "rainfall_mm": ":.1f",

# #                 "rainfall_7day": ":.1f",

# #                 "rainfall_30day": ":.1f",

# #                 "temp_mean": ":.1f",

# #                 "wind_max": ":.1f",

# #                 "latitude": False,

# #                 "longitude": False,

# #                 "marker_size": False
# #             },

# #             zoom=6.2,

# #             center={
# #                 "lat": 7.8731,
# #                 "lon": 80.7718
# #             },

# #             height=700,

# #             map_style="open-street-map"
# #         )

# #         # ----------------------------------------------------
# #         # Risk colors
# #         # ----------------------------------------------------

# #         fig.update_traces(
# #             marker={
# #                 "opacity": 0.85
# #             }
# #         )

# #         fig.update_layout(
# #             margin={
# #                 "r": 0,
# #                 "t": 0,
# #                 "l": 0,
# #                 "b": 0
# #             },

# #             legend_title_text="Risk Level"
# #         )

# #         # ----------------------------------------------------
# #         # Display map
# #         # ----------------------------------------------------

# #         st.plotly_chart(
# #             fig,
# #             width="stretch"
# #         )

# #     else:

# #         st.warning(
# #             "⚠️ No valid predictions are available "
# #             "for the selected date."
# #         )

# #     # ========================================================
# #     # DISTRICT RISK SUMMARY
# #     # ========================================================

# #     st.markdown(
# #         '<div class="section-title">'
# #         '📊 District Risk Summary'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     table_df = map_df[
# #         [
# #             "district",
# #             "risk",
# #             "probability_percent",
# #             "rainfall_mm",
# #             "rainfall_7day",
# #             "rainfall_30day",
# #             "temp_mean",
# #             "wind_max"
# #         ]
# #     ].copy()

# #     table_df.columns = [
# #         "District",
# #         "Risk",
# #         "Probability (%)",
# #         "Rainfall (mm)",
# #         "7-Day Rainfall (mm)",
# #         "30-Day Rainfall (mm)",
# #         "Mean Temperature (°C)",
# #         "Maximum Wind (km/h)"
# #     ]

# #     # ========================================================
# #     # SAFE NUMERIC CONVERSION
# #     # ========================================================

# #     for column in [
# #         "Probability (%)",
# #         "Rainfall (mm)",
# #         "7-Day Rainfall (mm)",
# #         "30-Day Rainfall (mm)",
# #         "Mean Temperature (°C)",
# #         "Maximum Wind (km/h)"
# #     ]:

# #         table_df[column] = pd.to_numeric(
# #             table_df[column],
# #             errors="coerce"
# #         )

# #     # ========================================================
# #     # ROUND NUMBERS
# #     # ========================================================

# #     table_df[
# #         "Probability (%)"
# #     ] = table_df[
# #         "Probability (%)"
# #     ].round(3)

# #     table_df[
# #         "Rainfall (mm)"
# #     ] = table_df[
# #         "Rainfall (mm)"
# #     ].round(1)

# #     table_df[
# #         "7-Day Rainfall (mm)"
# #     ] = table_df[
# #         "7-Day Rainfall (mm)"
# #     ].round(1)

# #     table_df[
# #         "30-Day Rainfall (mm)"
# #     ] = table_df[
# #         "30-Day Rainfall (mm)"
# #     ].round(1)

# #     table_df[
# #         "Mean Temperature (°C)"
# #     ] = table_df[
# #         "Mean Temperature (°C)"
# #     ].round(1)

# #     table_df[
# #         "Maximum Wind (km/h)"
# #     ] = table_df[
# #         "Maximum Wind (km/h)"
# #     ].round(1)

# #     # ========================================================
# #     # DISPLAY TABLE
# #     # ========================================================

# #     st.dataframe(
# #         table_df,
# #         width="stretch",
# #         hide_index=True
# #     )

# #     # ========================================================
# #     # SORTED RISK TABLE
# #     # ========================================================

# #     st.markdown(
# #         '<div class="section-title">'
# #         '🎯 Estimated Probabilities'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     ranking_df = map_df[
# #         [
# #             "district",
# #             "risk",
# #             "probability_percent"
# #         ]
# #     ].copy()

# #     ranking_df.columns = [
# #         "District",
# #         "Risk",
# #         "Probability (%)"
# #     ]

# #     # ========================================================
# #     # VERY IMPORTANT:
# #     # Convert None values to NaN BEFORE round()
# #     # ========================================================

# #     ranking_df[
# #         "Probability (%)"
# #     ] = pd.to_numeric(
# #         ranking_df[
# #             "Probability (%)"
# #         ],
# #         errors="coerce"
# #     )

# #     # ========================================================
# #     # SORT
# #     # ========================================================

# #     ranking_df = ranking_df.sort_values(
# #         by="Probability (%)",
# #         ascending=False,
# #         na_position="last"
# #     )

# #     # ========================================================
# #     # ROUND
# #     # ========================================================

# #     ranking_df[
# #         "Probability (%)"
# #     ] = ranking_df[
# #         "Probability (%)"
# #     ].round(3)

# #     # ========================================================
# #     # DISPLAY
# #     # ========================================================

# #     st.dataframe(
# #         ranking_df,
# #         width="stretch",
# #         hide_index=True
# #     )

# #     # ========================================================
# #     # DOWNLOAD CSV
# #     # ========================================================

# #     st.markdown(
# #         '<div class="section-title">'
# #         '⬇️ Export Results'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     csv_data = map_df.to_csv(
# #         index=False
# #     ).encode("utf-8")

# #     st.download_button(
# #         label="⬇️ Download District Risk Results",

# #         data=csv_data,

# #         file_name=(
# #             f"lankalandslide_risk_map_"
# #             f"{map_date}.csv"
# #         ),

# #         mime="text/csv",

# #         width="stretch"
# #     )

# #     # ========================================================
# #     # EXPLANATION
# #     # ========================================================

# #     st.markdown("---")

# #     st.markdown(
# #         '<div class="section-title">'
# #         'ℹ️ Understanding the Map'
# #         '</div>',
# #         unsafe_allow_html=True
# #     )

# #     st.markdown(
# #         """
# #         ### 🗺️ What does the map show?

# #         Each marker represents a **district reference
# #         location**.

# #         The machine-learning model generates a
# #         **district-day landslide risk estimate** using
# #         environmental and terrain-related features.

# #         ### 📈 Probability

# #         The probability represents the model's estimated
# #         probability for the selected district and date.

# #         ### ⚠️ Risk classification

# #         The risk classification is produced using the
# #         decision threshold configured in the deployed
# #         machine-learning model.

# #         ### 📍 Location limitation

# #         The markers represent district reference points.
# #         They do **not** represent the exact location of
# #         a future landslide.

# #         ### 🌧️ Weather information

# #         The prediction uses rainfall and other weather
# #         features supplied by the backend system.

# #         ### ⛰️ Terrain information

# #         Terrain characteristics such as elevation and
# #         slope are used by the machine-learning model
# #         where available.
# #         """
# #     )

# # else:

# #     # ========================================================
# #     # EMPTY STATE
# #     # ========================================================

# #     st.markdown("---")

# #     st.info(
# #         """
# #         🗺️ **No risk map has been generated yet.**

# #         Select a prediction date above and click:

# #         **🗺️ Generate Sri Lanka Risk Map**

# #         The system will request predictions from the
# #         FastAPI backend for all 24 districts.
# #         """
# #     )

# # # ============================================================
# # # DISCLAIMER
# # # ============================================================

# # st.markdown("---")

# # st.caption(
# #     """
# #     ⚠️ LankaLandslide AI provides district-day
# #     machine-learning risk estimates for research and
# #     decision-support purposes. It is not an official
# #     landslide warning system and should not replace
# #     information from Sri Lankan authorities.
# #     """
# # )import streamlit as st
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# from datetime import date, timedelta


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Risk Map | LankaLandslide AI",
#     page_icon="🗺️",
#     layout="wide"
# )


# API_BASE_URL = "http://127.0.0.1:8000"

# TODAY = date.today()

# MAX_FORECAST_DATE = TODAY + timedelta(days=16)


# # ============================================================
# # DISTRICT COORDINATES
# # ============================================================

# DISTRICTS = {
#     "Colombo": (6.9271, 79.8612),
#     "Gampaha": (7.0840, 80.0098),
#     "Kalutara": (6.5854, 79.9607),
#     "Kandy": (7.2906, 80.6337),
#     "Matale": (7.4675, 80.6234),
#     "Nuwara Eliya": (6.9497, 80.7891),
#     "Kegalle": (7.2513, 80.3464),
#     "Ratnapura": (6.6828, 80.3992),
#     "Galle": (6.0329, 80.2168),
#     "Matara": (5.9549, 80.5550),
#     "Hambantota": (6.1429, 81.1212),
#     "Badulla": (6.9934, 81.0550),
#     "Monaragala": (6.8728, 81.3507),
#     "Kurunegala": (7.4863, 80.3647),
#     "Puttalam": (8.0362, 79.8283),
#     "Anuradhapura": (8.3114, 80.4037),
#     "Polonnaruwa": (7.9403, 81.0188),
#     "Jaffna": (9.6615, 80.0255),
#     "Kilinochchi": (9.3803, 80.3770),
#     "Mannar": (8.9810, 79.9044),
#     "Vavuniya": (8.7514, 80.4971),
#     "Trincomalee": (8.5874, 81.2152),
#     "Batticaloa": (7.7170, 81.7000),
#     "Ampara": (7.2917, 81.6720)
# }


# # ============================================================
# # HEADER
# # ============================================================

# st.title("🗺️ Sri Lanka Landslide Risk Map")

# st.markdown(
#     """
#     View district-level landslide risk estimates across
#     Sri Lanka for a selected date.
#     """
# )


# # ============================================================
# # DATE SELECTION
# # ============================================================

# st.subheader("📅 Select Prediction Date")

# selected_date = st.date_input(
#     "Prediction Date",
#     value=TODAY,
#     min_value=date(1998, 1, 1),
#     max_value=MAX_FORECAST_DATE
# )


# # ============================================================
# # DATE TYPE
# # ============================================================

# if selected_date < TODAY:

#     date_type = "Historical"

#     horizon = "Historical"

# elif selected_date == TODAY:

#     date_type = "Today"

#     horizon = "Today"

# else:

#     days_ahead = (
#         selected_date - TODAY
#     ).days

#     date_type = "Forecast"

#     horizon = (
#         f"+{days_ahead} day"
#         if days_ahead == 1
#         else f"+{days_ahead} days"
#     )


# # ============================================================
# # DATE INFORMATION
# # ============================================================

# if date_type == "Forecast":

#     st.success(
#         f"""
#         🔮 **FORECAST RISK MAP**

#         Date: **{selected_date.strftime("%d %B %Y")}**

#         Forecast horizon: **{horizon}**

#         Weather conditions are based on forecast data.
#         """
#     )

# elif date_type == "Today":

#     st.info(
#         f"""
#         📅 **TODAY'S RISK MAP**

#         Date: **{selected_date.strftime("%d %B %Y")}**
#         """
#     )

# else:

#     st.info(
#         f"""
#         📚 **HISTORICAL RISK MAP**

#         Date: **{selected_date.strftime("%d %B %Y")}**
#         """
#     )


# # ============================================================
# # PREDICT BUTTON
# # ============================================================

# if st.button(
#     "🗺️ Generate Risk Map",
#     type="primary",
#     use_container_width=True
# ):

#     results = []

#     progress = st.progress(0)

#     status = st.empty()

#     total = len(DISTRICTS)


#     for index, (
#         district,
#         coordinates
#     ) in enumerate(DISTRICTS.items()):

#         status.write(
#             f"Predicting {district}..."
#         )

#         try:

#             response = requests.post(
#                 f"{API_BASE_URL}/api/predict",
#                 json={
#                     "district": district,
#                     "prediction_date":
#                         selected_date.strftime("%Y-%m-%d")
#                 },
#                 timeout=120
#             )

#             if response.status_code == 200:

#                 data = response.json()

#                 results.append(
#                     {
#                         "district": district,
#                         "latitude": coordinates[0],
#                         "longitude": coordinates[1],
#                         "probability":
#                             data.get(
#                                 "probability",
#                                 0
#                             ),
#                         "risk":
#                             data.get(
#                                 "risk",
#                                 "UNKNOWN"
#                             ),
#                         "model":
#                             data.get(
#                                 "model",
#                                 "XGBoost"
#                             )
#                     }
#                 )

#             else:

#                 results.append(
#                     {
#                         "district": district,
#                         "latitude": coordinates[0],
#                         "longitude": coordinates[1],
#                         "probability": None,
#                         "risk": "Unavailable",
#                         "model": "N/A"
#                     }
#                 )

#         except Exception:

#             results.append(
#                 {
#                     "district": district,
#                     "latitude": coordinates[0],
#                     "longitude": coordinates[1],
#                     "probability": None,
#                     "risk": "Unavailable",
#                     "model": "N/A"
#                 }
#             )

#         progress.progress(
#             (index + 1) / total
#         )


#     status.success(
#         "Risk prediction completed."
#     )


#     df = pd.DataFrame(results)


#     # ========================================================
#     # SUMMARY
#     # ========================================================

#     st.markdown("---")

#     st.subheader("📊 Risk Summary")


#     high_count = (
#         df["risk"] == "HIGH"
#     ).sum()

#     medium_count = (
#         df["risk"] == "MEDIUM"
#     ).sum()

#     low_count = (
#         df["risk"] == "LOW"
#     ).sum()

#     unavailable_count = (
#         df["risk"] == "Unavailable"
#     ).sum()


#     c1, c2, c3, c4 = st.columns(4)


#     with c1:

#         st.metric(
#             "🔴 High",
#             high_count
#         )


#     with c2:

#         st.metric(
#             "🟠 Medium",
#             medium_count
#         )


#     with c3:

#         st.metric(
#             "🟢 Low",
#             low_count
#         )


#     with c4:

#         st.metric(
#             "⚪ Unavailable",
#             unavailable_count
#         )


#     # ========================================================
#     # MAP
#     # ========================================================

#     valid_df = df[
#         df["probability"].notna()
#     ].copy()


#     if not valid_df.empty:

#         st.markdown("---")

#         st.subheader(
#             f"🌋 Risk Map — {selected_date.strftime('%d %B %Y')}"
#         )


#         fig = px.scatter_mapbox(
#             valid_df,
#             lat="latitude",
#             lon="longitude",
#             color="risk",
#             size="probability",
#             hover_name="district",
#             hover_data={
#                 "probability": ":.2f",
#                 "latitude": False,
#                 "longitude": False
#             },
#             zoom=6,
#             height=650,
#             mapbox_style="open-street-map"
#         )


#         fig.update_layout(
#             margin={
#                 "r": 0,
#                 "t": 0,
#                 "l": 0,
#                 "b": 0
#             }
#         )


#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )


#         # ====================================================
#         # TABLE
#         # ====================================================

#         st.markdown("---")

#         st.subheader("📋 District Risk Results")


#         display_df = valid_df[
#             [
#                 "district",
#                 "probability",
#                 "risk"
#             ]
#         ].copy()


#         display_df["probability"] = (
#             display_df["probability"]
#             .round(4)
#         )


#         display_df = display_df.sort_values(
#             "probability",
#             ascending=False
#         )


#         st.dataframe(
#             display_df,
#             use_container_width=True,
#             hide_index=True
#         )


#         # ====================================================
#         # DOWNLOAD
#         # ====================================================

#         csv = df.to_csv(
#             index=False
#         )


#         st.download_button(
#             "⬇️ Download Risk Results CSV",
#             csv,
#             file_name=(
#                 f"landslide_risk_"
#                 f"{selected_date}.csv"
#             ),
#             mime="text/csv"
#         )


#     else:

#         st.error(
#             "No valid predictions are available."
#         )


# # ============================================================
# # LIMITATIONS
# # ============================================================

# st.markdown("---")

# st.warning(
#     """
#     **Map interpretation**

#     • Predictions represent district-day risk.

#     • Markers indicate district reference locations,
#       not exact landslide locations.

#     • Future map results are forecast-based estimates.

#     • Forecast weather can change as new forecasts become
#       available.

#     • This system is not an official warning system.
#     """
# )
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date, timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Risk Map | LankaLandslide AI",
    page_icon="🗺️",
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

MAX_FORECAST_DATE = TODAY + timedelta(days=16)


# ============================================================
# SRI LANKAN DISTRICT COORDINATES
# ============================================================

DISTRICTS = {

    "Colombo": (6.9271, 79.8612),

    "Gampaha": (7.0840, 80.0098),

    "Kalutara": (6.5854, 79.9607),

    "Kandy": (7.2906, 80.6337),

    "Matale": (7.4675, 80.6234),

    "Nuwara Eliya": (6.9497, 80.7891),

    "Kegalle": (7.2513, 80.3464),

    "Ratnapura": (6.6828, 80.3992),

    "Galle": (6.0329, 80.2168),

    "Matara": (5.9549, 80.5550),

    "Hambantota": (6.1429, 81.1212),

    "Badulla": (6.9934, 81.0550),

    "Monaragala": (6.8728, 81.3507),

    "Kurunegala": (7.4863, 80.3647),

    "Puttalam": (8.0362, 79.8283),

    "Anuradhapura": (8.3114, 80.4037),

    "Polonnaruwa": (7.9403, 81.0188),

    "Jaffna": (9.6615, 80.0255),

    "Kilinochchi": (9.3803, 80.3770),

    "Mannar": (8.9810, 79.9044),

    "Vavuniya": (8.7514, 80.4971),

    "Trincomalee": (8.5874, 81.2152),

    "Batticaloa": (7.7170, 81.7000),

    "Ampara": (7.2917, 81.6720)
}


# ============================================================
# HEADER
# ============================================================

st.title("🗺️ Sri Lanka Landslide Risk Map")

st.markdown(
    """
    View machine-learning-based landslide risk estimates
    across Sri Lankan districts for a selected date.
    """
)

st.info(
    """
    📍 Each marker represents a district reference location.
    It does not represent the exact location of a landslide.
    """
)


# ============================================================
# DATE SELECTION
# ============================================================

st.subheader("📅 Select Prediction Date")

selected_date = st.date_input(
    "Prediction Date",
    value=TODAY,
    min_value=date(1998, 1, 1),
    max_value=MAX_FORECAST_DATE
)


# ============================================================
# DETERMINE DATE TYPE
# ============================================================

if selected_date < TODAY:

    date_type = "Historical"
    days_ahead = None

elif selected_date == TODAY:

    date_type = "Today"
    days_ahead = 0

else:

    date_type = "Forecast"
    days_ahead = (selected_date - TODAY).days


# ============================================================
# DATE INFORMATION
# ============================================================

if date_type == "Historical":

    st.info(
        f"""
        📚 **Historical Risk Map**

        Selected date:
        **{selected_date.strftime("%d %B %Y")}**

        Historical weather data will be used.
        """
    )

elif date_type == "Today":

    st.info(
        f"""
        📅 **Today's Risk Map**

        Selected date:
        **{selected_date.strftime("%d %B %Y")}**

        Current available weather information will be used.
        """
    )

else:

    st.success(
        f"""
        🔮 **Forecast Risk Map**

        Selected date:
        **{selected_date.strftime("%d %B %Y")}**

        Forecast horizon:
        **+{days_ahead} days**

        Forecast weather conditions will be used.
        """
    )


# ============================================================
# API PREDICTION FUNCTION
# ============================================================

def get_prediction(district, prediction_date):

    payload = {
        "district": district,
        "prediction_date": prediction_date.strftime("%Y-%m-%d")
    }

    try:

        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            json=payload,
            timeout=120
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if response.status_code == 200:

            return response.json()

        # ----------------------------------------------------
        # API ERROR
        # ----------------------------------------------------

        try:

            error_data = response.json()

            message = error_data.get(
                "detail",
                response.text
            )

        except ValueError:

            message = response.text

        return {
            "error": True,
            "status_code": response.status_code,
            "message": message
        }

    # --------------------------------------------------------
    # TIMEOUT
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        return {
            "error": True,
            "message": "Prediction request timed out."
        }

    # --------------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------------

    except requests.exceptions.ConnectionError:

        return {
            "error": True,
            "message": (
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running."
            )
        }

    # --------------------------------------------------------
    # OTHER REQUEST ERROR
    # --------------------------------------------------------

    except requests.exceptions.RequestException as error:

        return {
            "error": True,
            "message": str(error)
        }


# ============================================================
# GENERATE RISK MAP BUTTON
# ============================================================

generate_map = st.button(
    "🗺️ Generate Risk Map",
    type="primary",
    width="stretch"
)


# ============================================================
# GENERATE MAP
# ============================================================

if generate_map:

    st.markdown("---")

    st.subheader("🔄 Generating District Predictions")

    progress = st.progress(0)

    status = st.empty()

    results = []

    total_districts = len(DISTRICTS)


    # ========================================================
    # PREDICT ALL DISTRICTS
    # ========================================================

    for index, (district, coordinates) in enumerate(
        DISTRICTS.items()
    ):

        status.write(
            f"Analyzing **{district}**..."
        )

        prediction = get_prediction(
            district,
            selected_date
        )

        latitude = coordinates[0]
        longitude = coordinates[1]


        # ====================================================
        # SUCCESSFUL PREDICTION
        # ====================================================

        if (
            prediction
            and not prediction.get("error", False)
        ):

            raw_probability = prediction.get(
                "probability"
            )


            # ------------------------------------------------
            # CONVERT PROBABILITY
            # ------------------------------------------------

            try:

                probability = float(
                    raw_probability
                )

            except (
                TypeError,
                ValueError
            ):

                probability = None


            # ------------------------------------------------
            # RISK
            # ------------------------------------------------

            risk = prediction.get(
                "risk",
                "Unavailable"
            )

            if risk is None:

                risk = "Unavailable"

            risk = str(risk).upper()


            # ------------------------------------------------
            # FEATURES
            # ------------------------------------------------

            features = prediction.get(
                "features_used",
                {}
            )

            if not isinstance(
                features,
                dict
            ):

                features = {}


            # ------------------------------------------------
            # STORE RESULT
            # ------------------------------------------------

            results.append(
                {
                    "district": district,

                    "latitude": latitude,

                    "longitude": longitude,

                    "probability": probability,

                    "probability_percent": (
                        probability * 100
                        if probability is not None
                        else None
                    ),

                    "risk": risk,

                    "rainfall_mm": features.get(
                        "rainfall_mm"
                    ),

                    "rainfall_7day": features.get(
                        "rainfall_7day"
                    ),

                    "rainfall_30day": features.get(
                        "rainfall_30day"
                    ),

                    "temp_mean": features.get(
                        "temp_mean"
                    ),

                    "wind_max": features.get(
                        "wind_max"
                    )
                }
            )


        # ====================================================
        # FAILED PREDICTION
        # ====================================================

        else:

            results.append(
                {
                    "district": district,

                    "latitude": latitude,

                    "longitude": longitude,

                    "probability": None,

                    "probability_percent": None,

                    "risk": "UNAVAILABLE",

                    "rainfall_mm": None,

                    "rainfall_7day": None,

                    "rainfall_30day": None,

                    "temp_mean": None,

                    "wind_max": None
                }
            )


        # ----------------------------------------------------
        # UPDATE PROGRESS
        # ----------------------------------------------------

        progress.progress(
            (index + 1) / total_districts
        )


    status.success(
        "✅ District predictions completed."
    )


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(results)


    # ========================================================
    # SAVE RESULTS TO SESSION STATE
    # ========================================================

    st.session_state["risk_map_data"] = df

    st.session_state["risk_map_date"] = selected_date


# ============================================================
# DISPLAY STORED RESULTS
# ============================================================

if "risk_map_data" in st.session_state:

    df = st.session_state["risk_map_data"]

    map_date = st.session_state["risk_map_date"]


    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        f"📊 Risk Summary — "
        f"{map_date.strftime('%d %B %Y')}"
    )


    risk_values = (
        df["risk"]
        .fillna("UNAVAILABLE")
        .astype(str)
        .str.upper()
    )


    high_count = (
        risk_values == "HIGH"
    ).sum()


    medium_count = (
        risk_values == "MEDIUM"
    ).sum()


    low_count = (
        risk_values == "LOW"
    ).sum()


    unavailable_count = (
        risk_values == "UNAVAILABLE"
    ).sum()


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🔴 High Risk",
            int(high_count)
        )


    with c2:

        st.metric(
            "🟠 Medium Risk",
            int(medium_count)
        )


    with c3:

        st.metric(
            "🟢 Low Risk",
            int(low_count)
        )


    with c4:

        st.metric(
            "⚪ Unavailable",
            int(unavailable_count)
        )


    # ========================================================
    # VALID MAP DATA
    # ========================================================

    valid_df = df[
        df["probability"].notna()
    ].copy()


    # ========================================================
    # INTERACTIVE MAP
    # ========================================================

    st.markdown("---")

    st.subheader("🗺️ Interactive Risk Map")


    if not valid_df.empty:

        # ----------------------------------------------------
        # MARKER SIZE
        # ----------------------------------------------------

        valid_df["marker_size"] = (
            valid_df["probability_percent"]
            .clip(
                lower=5,
                upper=100
            )
        )


        # ----------------------------------------------------
        # CREATE MAP
        # ----------------------------------------------------

        fig = px.scatter_map(
            valid_df,

            lat="latitude",

            lon="longitude",

            color="risk",

            size="marker_size",

            size_max=35,

            hover_name="district",

            hover_data={
                "probability_percent": ":.2f",

                "rainfall_mm": ":.1f",

                "rainfall_7day": ":.1f",

                "rainfall_30day": ":.1f",

                "temp_mean": ":.1f",

                "wind_max": ":.1f",

                "latitude": False,

                "longitude": False,

                "marker_size": False
            },

            zoom=6,

            center={
                "lat": 7.8731,
                "lon": 80.7718
            },

            height=650,

            map_style="open-street-map"
        )


        # ----------------------------------------------------
        # MAP APPEARANCE
        # ----------------------------------------------------

        fig.update_traces(
            marker={
                "opacity": 0.85
            }
        )


        fig.update_layout(
            margin={
                "r": 0,
                "t": 0,
                "l": 0,
                "b": 0
            }
        )


        # ----------------------------------------------------
        # DISPLAY MAP
        # ----------------------------------------------------

        st.plotly_chart(
            fig,
            width="stretch"
        )


    else:

        st.warning(
            "⚠️ No valid predictions are available "
            "for the selected date."
        )


    # ========================================================
    # DISTRICT TABLE
    # ========================================================

    st.markdown("---")

    st.subheader("📋 District Risk Results")


    display_df = df[
        [
            "district",

            "risk",

            "probability_percent",

            "rainfall_mm",

            "rainfall_7day",

            "rainfall_30day",

            "temp_mean",

            "wind_max"
        ]
    ].copy()


    # ========================================================
    # RENAME COLUMNS
    # ========================================================

    display_df.columns = [

        "District",

        "Risk",

        "Probability (%)",

        "Rainfall (mm)",

        "7-Day Rainfall (mm)",

        "30-Day Rainfall (mm)",

        "Mean Temperature (°C)",

        "Maximum Wind (km/h)"
    ]


    # ========================================================
    # NUMERIC CONVERSION
    # ========================================================

    numeric_columns = [

        "Probability (%)",

        "Rainfall (mm)",

        "7-Day Rainfall (mm)",

        "30-Day Rainfall (mm)",

        "Mean Temperature (°C)",

        "Maximum Wind (km/h)"
    ]


    for column in numeric_columns:

        display_df[column] = pd.to_numeric(
            display_df[column],
            errors="coerce"
        )


    # ========================================================
    # ROUND VALUES
    # ========================================================

    display_df["Probability (%)"] = (
        display_df["Probability (%)"]
        .round(2)
    )


    display_df["Rainfall (mm)"] = (
        display_df["Rainfall (mm)"]
        .round(1)
    )


    display_df["7-Day Rainfall (mm)"] = (
        display_df["7-Day Rainfall (mm)"]
        .round(1)
    )


    display_df["30-Day Rainfall (mm)"] = (
        display_df["30-Day Rainfall (mm)"]
        .round(1)
    )


    display_df["Mean Temperature (°C)"] = (
        display_df["Mean Temperature (°C)"]
        .round(1)
    )


    display_df["Maximum Wind (km/h)"] = (
        display_df["Maximum Wind (km/h)"]
        .round(1)
    )


    # ========================================================
    # DISPLAY TABLE
    # ========================================================

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


    # ========================================================
    # DOWNLOAD RESULTS
    # ========================================================

    st.markdown("---")

    st.subheader("⬇️ Export Results")


    csv_data = (
        df.to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="⬇️ Download Risk Results CSV",

        data=csv_data,

        file_name=(
            f"lankalandslide_risk_"
            f"{map_date}.csv"
        ),

        mime="text/csv",

        width="stretch"
    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    st.markdown("---")

    st.subheader("ℹ️ Understanding the Map")


    st.markdown(
        """
        ### 🗺️ What does the map show?

        Each marker represents a **district reference
        location**.

        The machine-learning model generates a
        **district-day landslide risk estimate** using
        environmental and terrain-related features.

        ### 📈 Probability

        The probability represents the model's estimated
        probability for the selected district and date.

        ### ⚠️ Risk Classification

        The risk classification is produced using the
        decision threshold configured in the deployed
        machine-learning model.

        ### 📍 Location Limitation

        The markers represent district reference points.
        They do **not** represent the exact location of
        a future landslide.

        ### 🌧️ Weather

        Rainfall and other weather features supplied by
        the backend are used by the prediction system.

        ### ⛰️ Terrain

        Terrain characteristics such as elevation and
        slope are used by the machine-learning model
        where available.
        """
    )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.markdown("---")

    st.info(
        """
        🗺️ **No risk map has been generated yet.**

        Select a prediction date above and click:

        **🗺️ Generate Risk Map**

        The system will request predictions from the
        FastAPI backend for all 24 Sri Lankan districts.
        """
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown("---")

st.warning(
    """
    **Important:** LankaLandslide AI provides district-day
    machine-learning risk estimates for research and
    decision-support purposes. It is not an official
    landslide warning system and should not replace
    information from Sri Lankan authorities.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "LankaLandslide AI • XGBoost • FastAPI • Streamlit"
)