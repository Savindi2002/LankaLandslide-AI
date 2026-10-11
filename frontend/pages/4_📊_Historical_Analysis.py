# # ============================================================
# # LankaLandslide AI
# # Historical Analysis Dashboard
# # ============================================================
# #
# # File:
# # frontend/pages/4_📊_Historical_Analysis.py
# #
# # Data source:
# # data/processed/landslide_weather_master.csv
# #
# # ============================================================

# import os

# import numpy as np
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Historical Analysis | LankaLandslide AI",
#     page_icon="📊",
#     layout="wide"
# )


# # ============================================================
# # PROJECT PATH
# # ============================================================

# PROJECT_ROOT = os.path.abspath(
#     os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         ".."
#     )
# )

# DATA_FILE = os.path.join(
#     PROJECT_ROOT,
#     "data",
#     "processed",
#     "landslide_weather_master.csv"
# )


# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .main-title {
#         font-size: 2.2rem;
#         font-weight: 700;
#         margin-bottom: 0.2rem;
#     }

#     .subtitle {
#         color: #6b7280;
#         font-size: 1rem;
#         margin-bottom: 1.2rem;
#     }

#     .section-title {
#         font-size: 1.35rem;
#         font-weight: 650;
#         margin-top: 1.2rem;
#         margin-bottom: 0.6rem;
#     }

#     .info-box {
#         padding: 1rem;
#         border-radius: 10px;
#         border: 1px solid rgba(128,128,128,0.25);
#         background-color: rgba(128,128,128,0.05);
#         margin-bottom: 1rem;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # TITLE
# # ============================================================

# st.markdown(
#     '<div class="main-title">📊 Historical Landslide Analysis</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <div class="subtitle">
#     Explore historical landslide events, rainfall patterns, seasonal behavior,
#     and differences between Sri Lankan districts using the project's
#     processed historical dataset.
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_historical_data():

#     if not os.path.exists(DATA_FILE):

#         return None, (
#             "Historical dataset was not found at:\n\n"
#             f"`{DATA_FILE}`"
#         )

#     try:

#         df = pd.read_csv(DATA_FILE)

#     except Exception as error:

#         return None, (
#             "Could not read the historical dataset.\n\n"
#             f"Error: `{error}`"
#         )

#     # --------------------------------------------------------
#     # Date
#     # --------------------------------------------------------

#     if "date" not in df.columns:

#         return None, (
#             "The dataset does not contain a `date` column."
#         )

#     df["date"] = pd.to_datetime(
#         df["date"],
#         errors="coerce"
#     )

#     df = df.dropna(
#         subset=["date"]
#     ).copy()

#     # --------------------------------------------------------
#     # Numeric columns
#     # --------------------------------------------------------

#     numeric_columns = [
#         "rainfall_mm",
#         "rain_mm",
#         "rain_hours",
#         "temp_max",
#         "temp_min",
#         "temp_mean",
#         "wind_max",
#         "wind_gust_max",
#         "latitude",
#         "longitude",
#         "landslide_events",
#         "landslide_recorded"
#     ]

#     for column in numeric_columns:

#         if column in df.columns:

#             df[column] = pd.to_numeric(
#                 df[column],
#                 errors="coerce"
#             )

#     # --------------------------------------------------------
#     # Ensure target
#     # --------------------------------------------------------

#     if "landslide_recorded" not in df.columns:

#         if "landslide_events" in df.columns:

#             df["landslide_recorded"] = (
#                 df["landslide_events"]
#                 .fillna(0)
#                 .gt(0)
#                 .astype(int)
#             )

#         else:

#             return None, (
#                 "The dataset contains neither "
#                 "`landslide_recorded` nor "
#                 "`landslide_events`."
#             )

#     # --------------------------------------------------------
#     # Ensure event count
#     # --------------------------------------------------------

#     if "landslide_events" not in df.columns:

#         df["landslide_events"] = (
#             df["landslide_recorded"]
#             .fillna(0)
#         )

#     # --------------------------------------------------------
#     # Date features
#     # --------------------------------------------------------

#     df["year"] = (
#         df["date"].dt.year
#     )

#     df["month"] = (
#         df["date"].dt.month
#     )

#     df["month_name"] = (
#         df["date"].dt.strftime("%b")
#     )

#     df["month_full"] = (
#         df["date"].dt.strftime("%B")
#     )

#     df["day_of_year"] = (
#         df["date"].dt.dayofyear
#     )

#     # --------------------------------------------------------
#     # District
#     # --------------------------------------------------------

#     if "district" in df.columns:

#         df["district"] = (
#             df["district"]
#             .astype(str)
#             .str.strip()
#         )

#         df["district"] = df["district"].replace(
#             {
#                 "Moneragala": "Monaragala"
#             }
#         )

#     # --------------------------------------------------------
#     # Event flag
#     # --------------------------------------------------------

#     df["event_day"] = (
#         df["landslide_recorded"]
#         .fillna(0)
#         .astype(int)
#     )

#     # --------------------------------------------------------
#     # Rainfall helper
#     # --------------------------------------------------------

#     if "rainfall_mm" in df.columns:

#         df["rainfall_clean"] = (
#             pd.to_numeric(
#                 df["rainfall_mm"],
#                 errors="coerce"
#             )
#             .fillna(0)
#         )

#     elif "rain_mm" in df.columns:

#         df["rainfall_clean"] = (
#             pd.to_numeric(
#                 df["rain_mm"],
#                 errors="coerce"
#             )
#             .fillna(0)
#         )

#     else:

#         df["rainfall_clean"] = 0.0

#     return df, None


# # ============================================================
# # LOAD DATA
# # ============================================================

# df, error_message = load_historical_data()


# if df is None:

#     st.error(error_message)

#     st.info(
#         "Make sure the project contains "
#         "`data/processed/landslide_weather_master.csv`."
#     )

#     st.stop()


# # ============================================================
# # DATASET OVERVIEW
# # ============================================================

# min_date = df["date"].min()

# max_date = df["date"].max()

# number_of_rows = len(df)

# number_of_districts = (
#     df["district"].nunique()
#     if "district" in df.columns
#     else 0
# )

# total_events = int(
#     df["landslide_events"]
#     .fillna(0)
#     .sum()
# )

# event_days = int(
#     df["event_day"]
#     .sum()
# )

# event_rate = (
#     event_days
#     / number_of_rows
#     * 100
#     if number_of_rows > 0
#     else 0
# )


# # ============================================================
# # DATASET OVERVIEW
# # ============================================================

# st.markdown(
#     '<div class="section-title">📁 Historical Dataset Overview</div>',
#     unsafe_allow_html=True
# )

# col1, col2, col3, col4, col5 = st.columns(5)

# with col1:

#     st.metric(
#         "Records",
#         f"{number_of_rows:,}"
#     )

# with col2:

#     st.metric(
#         "Districts",
#         number_of_districts
#     )

# with col3:

#     st.metric(
#         "Landslide events",
#         f"{total_events:,}"
#     )

# with col4:

#     st.metric(
#         "Event days",
#         f"{event_days:,}"
#     )

# with col5:

#     st.metric(
#         "Event-day rate",
#         f"{event_rate:.2f}%"
#     )


# st.info(
#     f"""
# **Historical coverage:** {min_date.strftime('%d %b %Y')}
# → {max_date.strftime('%d %b %Y')}

# The dataset contains daily district-level weather observations
# together with recorded landslide-event information.

# A recorded event day means that at least one landslide was recorded
# for that district and date in the source data.
# """
# )


# # ============================================================
# # SIDEBAR FILTERS
# # ============================================================

# st.sidebar.header("🔎 Historical Filters")


# available_years = sorted(
#     df["year"]
#     .dropna()
#     .unique()
#     .astype(int)
#     .tolist()
# )


# if available_years:

#     selected_years = st.sidebar.slider(
#         "Year range",
#         min_value=int(min(available_years)),
#         max_value=int(max(available_years)),
#         value=(
#             int(min(available_years)),
#             int(max(available_years))
#         )
#     )

# else:

#     selected_years = (0, 0)


# # ------------------------------------------------------------
# # District
# # ------------------------------------------------------------

# district_options = [
#     "All districts"
# ]

# if "district" in df.columns:

#     district_options += sorted(
#         df["district"]
#         .dropna()
#         .unique()
#         .tolist()
#     )


# selected_district = st.sidebar.selectbox(
#     "District",
#     district_options
# )


# # ------------------------------------------------------------
# # Record type
# # ------------------------------------------------------------

# event_filter = st.sidebar.selectbox(
#     "Record type",
#     [
#         "All days",
#         "Landslide days only",
#         "Non-landslide days only"
#     ]
# )


# # ============================================================
# # APPLY FILTERS
# # ============================================================

# filtered_df = df[
#     (df["year"] >= selected_years[0])
#     &
#     (df["year"] <= selected_years[1])
# ].copy()


# if selected_district != "All districts":

#     filtered_df = filtered_df[
#         filtered_df["district"]
#         == selected_district
#     ].copy()


# if event_filter == "Landslide days only":

#     filtered_df = filtered_df[
#         filtered_df["event_day"] == 1
#     ].copy()

# elif event_filter == "Non-landslide days only":

#     filtered_df = filtered_df[
#         filtered_df["event_day"] == 0
#     ].copy()


# # ============================================================
# # EMPTY FILTER CHECK
# # ============================================================

# if filtered_df.empty:

#     st.warning(
#         "No records match the selected filters. "
#         "Please change the year, district, or record type."
#     )

#     st.stop()


# # ============================================================
# # FILTER SUMMARY
# # ============================================================

# st.markdown(
#     '<div class="section-title">📌 Current Selection</div>',
#     unsafe_allow_html=True
# )

# fc1, fc2, fc3, fc4 = st.columns(4)


# with fc1:

#     st.metric(
#         "Filtered records",
#         f"{len(filtered_df):,}"
#     )


# with fc2:

#     filtered_events = int(
#         filtered_df["landslide_events"]
#         .fillna(0)
#         .sum()
#     )

#     st.metric(
#         "Recorded events",
#         f"{filtered_events:,}"
#     )


# with fc3:

#     filtered_event_days = int(
#         filtered_df["event_day"]
#         .sum()
#     )

#     st.metric(
#         "Event days",
#         f"{filtered_event_days:,}"
#     )


# with fc4:

#     filtered_rainfall = (
#         filtered_df["rainfall_clean"]
#         .mean()
#     )

#     st.metric(
#         "Average daily rainfall",
#         f"{filtered_rainfall:.2f} mm"
#     )


# # ============================================================
# # 1. YEARLY LANDSLIDE TRENDS
# # ============================================================

# st.markdown(
#     '<div class="section-title">📈 1. Yearly Landslide Trends</div>',
#     unsafe_allow_html=True
# )

# yearly = (
#     filtered_df
#     .groupby(
#         "year",
#         as_index=False
#     )
#     .agg(
#         landslide_events=(
#             "landslide_events",
#             "sum"
#         ),
#         event_days=(
#             "event_day",
#             "sum"
#         ),
#         rainfall_mm=(
#             "rainfall_clean",
#             "sum"
#         ),
#         average_daily_rainfall=(
#             "rainfall_clean",
#             "mean"
#         )
#     )
#     .sort_values("year")
# )


# if not yearly.empty:

#     fig_year = go.Figure()

#     fig_year.add_trace(
#         go.Bar(
#             x=yearly["year"],
#             y=yearly["landslide_events"],
#             name="Landslide events"
#         )
#     )

#     fig_year.add_trace(
#         go.Scatter(
#             x=yearly["year"],
#             y=yearly["event_days"],
#             name="Event days",
#             mode="lines+markers",
#             yaxis="y2"
#         )
#     )

#     fig_year.update_layout(
#         title="Annual landslide activity",
#         height=380,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         ),
#         xaxis_title="Year",
#         yaxis=dict(
#             title="Landslide events"
#         ),
#         yaxis2=dict(
#             title="Event days",
#             overlaying="y",
#             side="right"
#         ),
#         hovermode="x unified"
#     )

#     st.plotly_chart(
#         fig_year,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )

#     with st.expander(
#         "📋 View yearly statistics"
#     ):

#         yearly_display = yearly.copy()

#         yearly_display[
#             "rainfall_mm"
#         ] = (
#             yearly_display[
#                 "rainfall_mm"
#             ].round(1)
#         )

#         yearly_display[
#             "average_daily_rainfall"
#         ] = (
#             yearly_display[
#                 "average_daily_rainfall"
#             ].round(2)
#         )

#         yearly_display = (
#             yearly_display.rename(
#                 columns={
#                     "year":
#                         "Year",
#                     "landslide_events":
#                         "Landslide events",
#                     "event_days":
#                         "Event days",
#                     "rainfall_mm":
#                         "Total rainfall (mm)",
#                     "average_daily_rainfall":
#                         "Average daily rainfall (mm)"
#                 }
#             )
#         )

#         st.dataframe(
#             yearly_display,
#             width="stretch",
#             hide_index=True
#         )


# # ============================================================
# # 2. MONTHLY PATTERNS
# # ============================================================

# st.markdown(
#     '<div class="section-title">📅 2. Monthly Landslide Patterns</div>',
#     unsafe_allow_html=True
# )

# monthly = (
#     filtered_df
#     .groupby(
#         [
#             "month",
#             "month_full"
#         ],
#         as_index=False
#     )
#     .agg(
#         landslide_events=(
#             "landslide_events",
#             "sum"
#         ),
#         event_days=(
#             "event_day",
#             "sum"
#         ),
#         average_rainfall=(
#             "rainfall_clean",
#             "mean"
#         ),
#         total_rainfall=(
#             "rainfall_clean",
#             "sum"
#         )
#     )
#     .sort_values("month")
# )


# if not monthly.empty:

#     month_order = [
#         "January",
#         "February",
#         "March",
#         "April",
#         "May",
#         "June",
#         "July",
#         "August",
#         "September",
#         "October",
#         "November",
#         "December"
#     ]

#     monthly["month_full"] = pd.Categorical(
#         monthly["month_full"],
#         categories=month_order,
#         ordered=True
#     )

#     monthly = monthly.sort_values(
#         "month_full"
#     )

#     fig_month = go.Figure()

#     fig_month.add_trace(
#         go.Bar(
#             x=monthly["month_full"],
#             y=monthly["landslide_events"],
#             name="Landslide events"
#         )
#     )

#     fig_month.add_trace(
#         go.Scatter(
#             x=monthly["month_full"],
#             y=monthly["average_rainfall"],
#             name="Average rainfall (mm)",
#             mode="lines+markers",
#             yaxis="y2"
#         )
#     )

#     fig_month.update_layout(
#         title="Monthly landslide activity and rainfall",
#         height=380,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         ),
#         xaxis_title="Month",
#         yaxis=dict(
#             title="Landslide events"
#         ),
#         yaxis2=dict(
#             title="Average rainfall (mm)",
#             overlaying="y",
#             side="right"
#         ),
#         hovermode="x unified"
#     )

#     st.plotly_chart(
#         fig_month,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )


#     # --------------------------------------------------------
#     # Monthly rate
#     # --------------------------------------------------------

#     monthly_rate = (
#         filtered_df
#         .groupby(
#             "month",
#             as_index=False
#         )
#         .agg(
#             event_days=(
#                 "event_day",
#                 "sum"
#             ),
#             total_days=(
#                 "event_day",
#                 "count"
#             )
#         )
#     )

#     monthly_rate["event_rate"] = (
#         monthly_rate["event_days"]
#         /
#         monthly_rate["total_days"]
#         * 100
#     )

#     monthly_rate["month_name"] = (
#         monthly_rate["month"]
#         .map(
#             {
#                 i + 1:
#                     month_order[i]
#                 for i in range(12)
#             }
#         )
#     )

#     monthly_rate = monthly_rate.sort_values(
#         "month"
#     )

#     fig_rate = px.bar(
#         monthly_rate,
#         x="month_name",
#         y="event_rate",
#         title="Historical landslide event-day rate by month",
#         labels={
#             "month_name":
#                 "Month",
#             "event_rate":
#                 "Event-day rate (%)"
#         },
#         text="event_rate"
#     )

#     fig_rate.update_traces(
#         texttemplate="%{text:.2f}%",
#         textposition="outside"
#     )

#     fig_rate.update_layout(
#         height=350,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         )
#     )

#     st.plotly_chart(
#         fig_rate,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )


# # ============================================================
# # 3. DISTRICT COMPARISON
# # ============================================================

# st.markdown(
#     '<div class="section-title">🗺️ 3. District Comparison</div>',
#     unsafe_allow_html=True
# )

# if "district" in filtered_df.columns:

#     district_summary = (
#         filtered_df
#         .groupby(
#             "district",
#             as_index=False
#         )
#         .agg(
#             landslide_events=(
#                 "landslide_events",
#                 "sum"
#             ),
#             event_days=(
#                 "event_day",
#                 "sum"
#             ),
#             total_days=(
#                 "event_day",
#                 "count"
#             ),
#             average_rainfall=(
#                 "rainfall_clean",
#                 "mean"
#             ),
#             total_rainfall=(
#                 "rainfall_clean",
#                 "sum"
#             )
#         )
#     )

#     district_summary["event_rate"] = (
#         district_summary["event_days"]
#         /
#         district_summary["total_days"]
#         * 100
#     )

#     district_summary = (
#         district_summary
#         .sort_values(
#             "landslide_events",
#             ascending=False
#         )
#     )

#     fig_district = px.bar(
#         district_summary,
#         x="landslide_events",
#         y="district",
#         orientation="h",
#         title="Landslide events by district",
#         labels={
#             "landslide_events":
#                 "Landslide events",
#             "district":
#                 "District"
#         }
#     )

#     fig_district.update_layout(
#         height=450,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         )
#     )

#     st.plotly_chart(
#         fig_district,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )


#     fig_district_rate = px.bar(
#         district_summary.sort_values(
#             "event_rate",
#             ascending=False
#         ),
#         x="event_rate",
#         y="district",
#         orientation="h",
#         title="Historical event-day rate by district",
#         labels={
#             "event_rate":
#                 "Event-day rate (%)",
#             "district":
#                 "District"
#         }
#     )

#     fig_district_rate.update_layout(
#         height=450,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         )
#     )

#     st.plotly_chart(
#         fig_district_rate,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )


#     with st.expander(
#         "📋 View district statistics"
#     ):

#         district_display = (
#             district_summary.copy()
#         )

#         district_display[
#             "average_rainfall"
#         ] = (
#             district_display[
#                 "average_rainfall"
#             ].round(2)
#         )

#         district_display[
#             "total_rainfall"
#         ] = (
#             district_display[
#                 "total_rainfall"
#             ].round(1)
#         )

#         district_display[
#             "event_rate"
#         ] = (
#             district_display[
#                 "event_rate"
#             ].round(3)
#         )

#         district_display = (
#             district_display.rename(
#                 columns={
#                     "district":
#                         "District",
#                     "landslide_events":
#                         "Landslide events",
#                     "event_days":
#                         "Event days",
#                     "total_days":
#                         "Total days",
#                     "average_rainfall":
#                         "Average rainfall (mm)",
#                     "total_rainfall":
#                         "Total rainfall (mm)",
#                     "event_rate":
#                         "Event-day rate (%)"
#                 }
#             )
#         )

#         st.dataframe(
#             district_display,
#             width="stretch",
#             hide_index=True
#         )


# # ============================================================
# # 4. RAINFALL VS LANDSLIDE EVENTS
# # ============================================================

# st.markdown(
#     '<div class="section-title">🌧️ 4. Rainfall vs. Landslide Events</div>',
#     unsafe_allow_html=True
# )

# rainfall_analysis = (
#     filtered_df[
#         [
#             "rainfall_clean",
#             "landslide_events",
#             "event_day"
#         ]
#     ]
#     .copy()
# )

# rainfall_analysis[
#     "event_status"
# ] = np.where(
#     rainfall_analysis["event_day"] == 1,
#     "Landslide recorded",
#     "No landslide recorded"
# )


# fig_box = px.box(
#     rainfall_analysis,
#     x="event_status",
#     y="rainfall_clean",
#     points="outliers",
#     title="Daily rainfall distribution by landslide status",
#     labels={
#         "event_status":
#             "Day type",
#         "rainfall_clean":
#             "Daily rainfall (mm)"
#     }
# )

# fig_box.update_layout(
#     height=380,
#     margin=dict(
#         l=40,
#         r=40,
#         t=60,
#         b=40
#     )
# )

# st.plotly_chart(
#     fig_box,
#     width="stretch",
#     config={
#         "displayModeBar": False,
#         "responsive": True
#     }
# )


# scatter_df = (
#     filtered_df[
#         [
#             "rainfall_clean",
#             "landslide_events",
#             "event_day",
#             "district"
#         ]
#     ]
#     .copy()
# )

# scatter_df[
#     "event_status"
# ] = np.where(
#     scatter_df["event_day"] == 1,
#     "Landslide recorded",
#     "No landslide recorded"
# )


# fig_scatter = px.scatter(
#     scatter_df,
#     x="rainfall_clean",
#     y="landslide_events",
#     color="event_status",
#     hover_data=["district"],
#     opacity=0.65,
#     title="Daily rainfall vs. recorded landslide events",
#     labels={
#         "rainfall_clean":
#             "Daily rainfall (mm)",
#         "landslide_events":
#             "Landslide events",
#         "event_status":
#             "Day type"
#     }
# )

# fig_scatter.update_layout(
#     height=400,
#     margin=dict(
#         l=40,
#         r=40,
#         t=60,
#         b=40
#     )
# )

# st.plotly_chart(
#     fig_scatter,
#     width="stretch",
#     config={
#         "displayModeBar": False,
#         "responsive": True
#     }
# )


# # ============================================================
# # 5. RAINFALL THRESHOLD ANALYSIS
# # ============================================================

# st.markdown(
#     '<div class="section-title">☔ 5. Rainfall Threshold Analysis</div>',
#     unsafe_allow_html=True
# )

# thresholds = [
#     10,
#     25,
#     50,
#     100
# ]

# threshold_results = []


# for threshold in thresholds:

#     rain_days = filtered_df[
#         filtered_df["rainfall_clean"]
#         >= threshold
#     ]

#     if len(rain_days) == 0:

#         event_rate_at_threshold = 0

#     else:

#         event_rate_at_threshold = (
#             rain_days["event_day"].sum()
#             /
#             len(rain_days)
#             * 100
#         )

#     threshold_results.append(
#         {
#             "threshold":
#                 f">= {threshold} mm",

#             "threshold_value":
#                 threshold,

#             "rainy_days":
#                 len(rain_days),

#             "event_days":
#                 int(
#                     rain_days["event_day"]
#                     .sum()
#                 ),

#             "event_rate":
#                 event_rate_at_threshold
#         }
#     )


# threshold_df = pd.DataFrame(
#     threshold_results
# )


# fig_threshold = px.bar(
#     threshold_df,
#     x="threshold",
#     y="event_rate",
#     title="Landslide event-day rate after rainfall thresholds",
#     labels={
#         "threshold":
#             "Daily rainfall threshold",
#         "event_rate":
#             "Event-day rate (%)"
#     },
#     text="event_rate"
# )

# fig_threshold.update_traces(
#     texttemplate="%{text:.2f}%",
#     textposition="outside"
# )

# fig_threshold.update_layout(
#     height=380,
#     margin=dict(
#         l=40,
#         r=40,
#         t=60,
#         b=40
#     )
# )

# st.plotly_chart(
#     fig_threshold,
#     width="stretch",
#     config={
#         "displayModeBar": False,
#         "responsive": True
#     }
# )

# st.caption(
#     "These are descriptive historical rates, not official "
#     "warning thresholds and not guarantees of future landslides."
# )


# # ============================================================
# # 6. YEARLY RAINFALL VS LANDSLIDE ACTIVITY
# # ============================================================

# st.markdown(
#     '<div class="section-title">🌧️📈 6. Yearly Rainfall and Landslide Activity</div>',
#     unsafe_allow_html=True
# )

# year_rain = (
#     filtered_df
#     .groupby(
#         "year",
#         as_index=False
#     )
#     .agg(
#         average_rainfall=(
#             "rainfall_clean",
#             "mean"
#         ),
#         landslide_events=(
#             "landslide_events",
#             "sum"
#         ),
#         event_days=(
#             "event_day",
#             "sum"
#         )
#     )
# )


# if not year_rain.empty:

#     fig_rain_year = go.Figure()

#     fig_rain_year.add_trace(
#         go.Scatter(
#             x=year_rain["year"],
#             y=year_rain["average_rainfall"],
#             name="Average daily rainfall",
#             mode="lines+markers"
#         )
#     )

#     fig_rain_year.add_trace(
#         go.Bar(
#             x=year_rain["year"],
#             y=year_rain["landslide_events"],
#             name="Landslide events",
#             opacity=0.45,
#             yaxis="y2"
#         )
#     )

#     fig_rain_year.update_layout(
#         title="Annual rainfall conditions and landslide activity",
#         height=400,
#         margin=dict(
#             l=40,
#             r=40,
#             t=60,
#             b=40
#         ),
#         xaxis_title="Year",
#         yaxis=dict(
#             title="Average daily rainfall (mm)"
#         ),
#         yaxis2=dict(
#             title="Landslide events",
#             overlaying="y",
#             side="right"
#         ),
#         hovermode="x unified"
#     )

#     st.plotly_chart(
#         fig_rain_year,
#         width="stretch",
#         config={
#             "displayModeBar": False,
#             "responsive": True
#         }
#     )


# # ============================================================
# # 7. RAINFALL CATEGORY VS EVENT RATE
# # ============================================================

# st.markdown(
#     '<div class="section-title">🌦️ 7. Rainfall Category vs. Historical Event Rate</div>',
#     unsafe_allow_html=True
# )


# def rainfall_category(value):

#     if value < 1:

#         return "0–<1 mm"

#     elif value < 10:

#         return "1–<10 mm"

#     elif value < 25:

#         return "10–<25 mm"

#     elif value < 50:

#         return "25–<50 mm"

#     elif value < 100:

#         return "50–<100 mm"

#     else:

#         return "100+ mm"


# category_order = [
#     "0–<1 mm",
#     "1–<10 mm",
#     "10–<25 mm",
#     "25–<50 mm",
#     "50–<100 mm",
#     "100+ mm"
# ]


# rainfall_categories = (
#     filtered_df.copy()
# )

# rainfall_categories[
#     "rainfall_category"
# ] = (
#     rainfall_categories[
#         "rainfall_clean"
#     ]
#     .apply(rainfall_category)
# )


# category_summary = (
#     rainfall_categories
#     .groupby(
#         "rainfall_category",
#         as_index=False
#     )
#     .agg(
#         days=(
#             "event_day",
#             "count"
#         ),
#         event_days=(
#             "event_day",
#             "sum"
#         ),
#         landslide_events=(
#             "landslide_events",
#             "sum"
#         )
#     )
# )


# category_summary[
#     "rainfall_category"
# ] = pd.Categorical(
#     category_summary[
#         "rainfall_category"
#     ],
#     categories=category_order,
#     ordered=True
# )

# category_summary = (
#     category_summary
#     .sort_values(
#         "rainfall_category"
#     )
# )

# category_summary[
#     "event_rate"
# ] = (
#     category_summary[
#         "event_days"
#     ]
#     /
#     category_summary[
#         "days"
#     ]
#     * 100
# )


# fig_category = px.bar(
#     category_summary,
#     x="rainfall_category",
#     y="event_rate",
#     title="Historical event-day rate by daily rainfall category",
#     labels={
#         "rainfall_category":
#             "Daily rainfall",
#         "event_rate":
#             "Event-day rate (%)"
#     },
#     text="event_rate"
# )

# fig_category.update_traces(
#     texttemplate="%{text:.2f}%",
#     textposition="outside"
# )

# fig_category.update_layout(
#     height=380,
#     margin=dict(
#         l=40,
#         r=40,
#         t=60,
#         b=40
#     )
# )

# st.plotly_chart(
#     fig_category,
#     width="stretch",
#     config={
#         "displayModeBar": False,
#         "responsive": True
#     }
# )


# # ============================================================
# # 8. HISTORICAL HIGH-ACTIVITY DAYS
# # ============================================================

# st.markdown(
#     '<div class="section-title">🚨 8. Historical High-Activity Days</div>',
#     unsafe_allow_html=True
# )

# event_records = (
#     filtered_df[
#         filtered_df["event_day"] == 1
#     ]
#     .copy()
# )


# if not event_records.empty:

#     top_events = (
#         event_records
#         .sort_values(
#             [
#                 "landslide_events",
#                 "rainfall_clean"
#             ],
#             ascending=False
#         )
#         .head(20)
#         .copy()
#     )

#     display_columns = [
#         "date",
#         "district",
#         "rainfall_clean",
#         "landslide_events"
#     ]

#     display_columns = [
#         column
#         for column in display_columns
#         if column in top_events.columns
#     ]

#     top_events_display = (
#         top_events[
#             display_columns
#         ]
#         .copy()
#     )

#     top_events_display = (
#         top_events_display.rename(
#             columns={
#                 "date":
#                     "Date",
#                 "district":
#                     "District",
#                 "rainfall_clean":
#                     "Rainfall (mm)",
#                 "landslide_events":
#                     "Landslide events"
#             }
#         )
#     )

#     if "Rainfall (mm)" in top_events_display.columns:

#         top_events_display[
#             "Rainfall (mm)"
#         ] = (
#             top_events_display[
#                 "Rainfall (mm)"
#             ].round(2)
#         )

#     st.dataframe(
#         top_events_display,
#         width="stretch",
#         hide_index=True
#     )

# else:

#     st.info(
#         "No recorded landslide days are available "
#         "for the selected filters."
#     )


# # ============================================================
# # 9. SELECTED DISTRICT PROFILE
# # ============================================================

# if selected_district != "All districts":

#     st.markdown(
#         f'<div class="section-title">'
#         f'📍 9. Historical Profile: {selected_district}'
#         f'</div>',
#         unsafe_allow_html=True
#     )

#     district_df = (
#         df[
#             df["district"]
#             == selected_district
#         ]
#         .copy()
#     )

#     district_yearly = (
#         district_df
#         .groupby(
#             "year",
#             as_index=False
#         )
#         .agg(
#             landslide_events=(
#                 "landslide_events",
#                 "sum"
#             ),
#             event_days=(
#                 "event_day",
#                 "sum"
#             ),
#             average_rainfall=(
#                 "rainfall_clean",
#                 "mean"
#             )
#         )
#         .sort_values("year")
#     )

#     if not district_yearly.empty:

#         fig_selected = go.Figure()

#         fig_selected.add_trace(
#             go.Bar(
#                 x=district_yearly["year"],
#                 y=district_yearly[
#                     "landslide_events"
#                 ],
#                 name="Landslide events"
#             )
#         )

#         fig_selected.add_trace(
#             go.Scatter(
#                 x=district_yearly["year"],
#                 y=district_yearly[
#                     "average_rainfall"
#                 ],
#                 name="Average rainfall (mm)",
#                 mode="lines+markers",
#                 yaxis="y2"
#             )
#         )

#         fig_selected.update_layout(
#             title=(
#                 f"{selected_district}: "
#                 "yearly historical pattern"
#             ),
#             height=380,
#             margin=dict(
#                 l=40,
#                 r=40,
#                 t=60,
#                 b=40
#             ),
#             xaxis_title="Year",
#             yaxis=dict(
#                 title="Landslide events"
#             ),
#             yaxis2=dict(
#                 title="Average rainfall (mm)",
#                 overlaying="y",
#                 side="right"
#             ),
#             hovermode="x unified"
#         )

#         st.plotly_chart(
#             fig_selected,
#             width="stretch",
#             config={
#                 "displayModeBar": False,
#                 "responsive": True
#             }
#         )


# # ============================================================
# # 10. HISTORICAL DATA PREVIEW
# # ============================================================

# st.markdown(
#     '<div class="section-title">🧾 10. Historical Data Preview</div>',
#     unsafe_allow_html=True
# )

# with st.expander(
#     "Open filtered historical records"
# ):

#     preview_df = filtered_df.copy()

#     st.dataframe(
#         preview_df.head(500),
#         width="stretch",
#         hide_index=True
#     )

#     st.caption(
#         "Showing the first 500 rows of the current "
#         "filtered dataset."
#     )


# # ============================================================
# # DOWNLOAD
# # ============================================================

# st.markdown(
#     '<div class="section-title">⬇️ Download Historical Data</div>',
#     unsafe_allow_html=True
# )

# csv_data = (
#     filtered_df
#     .to_csv(index=False)
#     .encode("utf-8")
# )


# st.download_button(
#     label="📥 Download filtered historical data",
#     data=csv_data,
#     file_name="lankalandslide_historical_analysis.csv",
#     mime="text/csv"
# )


# # ============================================================
# # INTERPRETATION
# # ============================================================

# st.markdown(
#     '<div class="section-title">🧠 How to Interpret This Page</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <div class="info-box">

#     <b>Yearly trends</b><br>
#     Show how recorded landslide activity changed across the historical period.

#     <br><br>

#     <b>Monthly patterns</b><br>
#     Show seasonal differences in recorded landslide activity and rainfall.

#     <br><br>

#     <b>District comparison</b><br>
#     Shows how the number and rate of recorded event days differ between districts.

#     <br><br>

#     <b>Rainfall vs. events</b><br>
#     Helps examine whether recorded landslide activity tends to occur on
#     wetter days.

#     <br><br>

#     <b>Rainfall thresholds</b><br>
#     These are descriptive statistics from the historical dataset.
#     They should not be interpreted as official warning thresholds.

#     </div>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # LIMITATIONS
# # ============================================================

# st.warning(
#     """
#     **Important limitation:** `landslide_recorded = 0` means that no landslide
#     was recorded in the available source data for that district-day. It does
#     not prove that no landslide occurred.

#     The historical dataset is district-level, while weather values are based
#     on district reference locations. Therefore, these charts describe
#     historical district-day patterns rather than exact landslide locations.
#     """
# )


# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown("---")

# st.caption(
#     "LankaLandslide AI • Historical Analysis • "
#     "Based on the project's processed historical dataset"
# )
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Historical Analysis | LankaLandslide AI",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# FILE
# ============================================================

DATA_PATH = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "data"
    / "processed"
    / "landslide_weather_master.csv"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Historical Landslide Analysis")

st.markdown(
    """
    Explore historical landslide events and weather patterns
    used during development of LankaLandslide AI.
    """
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        DATA_PATH
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["year"] = (
        df["date"]
        .dt.year
    )

    df["month"] = (
        df["date"]
        .dt.month
    )

    return df


try:

    df = load_data()

except Exception as e:

    st.error(
        f"Could not load historical dataset:\n\n{e}"
    )

    st.stop()


# ============================================================
# DATASET INFO
# ============================================================

st.markdown("---")

st.subheader("📁 Dataset Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Records",
        f"{len(df):,}"
    )


with c2:

    st.metric(
        "Districts",
        df["district"].nunique()
    )


with c3:

    st.metric(
        "Landslide Events",
        int(df["landslide_events"].sum())
    )


with c4:

    st.metric(
        "Years",
        f"{df['year'].min()}–{df['year'].max()}"
    )


# ============================================================
# YEARLY TRENDS
# ============================================================

st.markdown("---")

st.header("📅 Yearly Landslide Events")


yearly = (
    df.groupby("year")["landslide_events"]
    .sum()
    .reset_index()
)


fig = px.line(
    yearly,
    x="year",
    y="landslide_events",
    markers=True,
    title="Historical Landslide Events by Year"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MONTHLY PATTERN
# ============================================================

st.header("🗓️ Monthly Pattern")


monthly = (
    df.groupby("month")["landslide_events"]
    .sum()
    .reset_index()
)


month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


monthly["month_name"] = (
    monthly["month"]
    .apply(
        lambda x:
        month_names[int(x) - 1]
    )
)


fig = px.bar(
    monthly,
    x="month_name",
    y="landslide_events",
    title="Landslide Events by Month"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DISTRICT COMPARISON
# ============================================================

st.header("📍 District Comparison")


districts = (
    df.groupby("district")["landslide_events"]
    .sum()
    .reset_index()
    .sort_values(
        "landslide_events",
        ascending=False
    )
)


fig = px.bar(
    districts,
    x="landslide_events",
    y="district",
    orientation="h",
    title="Historical Landslide Events by District"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# RAINFALL VS LANDSLIDES
# ============================================================

st.header("🌧️ Rainfall vs Landslide Events")


rainfall_summary = (
    df.groupby("date")
    .agg(
        rainfall=("rainfall_mm", "sum"),
        landslide_events=(
            "landslide_events",
            "sum"
        )
    )
    .reset_index()
)


fig = px.scatter(
    rainfall_summary,
    x="rainfall",
    y="landslide_events",
    title="Daily Rainfall vs Landslide Events",
    trendline="ols"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# YEARLY RAINFALL VS EVENTS
# ============================================================

st.header("🌧️ Yearly Rainfall vs Events")


yearly_combined = (
    df.groupby("year")
    .agg(
        rainfall=(
            "rainfall_mm",
            "mean"
        ),
        landslide_events=(
            "landslide_events",
            "sum"
        )
    )
    .reset_index()
)


fig = px.scatter(
    yearly_combined,
    x="rainfall",
    y="landslide_events",
    text="year",
    title="Yearly Rainfall vs Landslide Events"
)


fig.update_traces(
    textposition="top center"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SELECTED DISTRICT
# ============================================================

st.markdown("---")

st.header("📍 District Profile")


selected_district = st.selectbox(
    "Select District",
    sorted(
        df["district"]
        .dropna()
        .unique()
    )
)


district_df = df[
    df["district"] ==
    selected_district
].copy()


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Recorded Events",
        int(
            district_df[
                "landslide_events"
            ].sum()
        )
    )


with c2:

    st.metric(
        "Average Rainfall",
        f"{district_df['rainfall_mm'].mean():.2f} mm"
    )


with c3:

    st.metric(
        "Maximum Daily Rainfall",
        f"{district_df['rainfall_mm'].max():.2f} mm"
    )


# ============================================================
# DISTRICT YEARLY CHART
# ============================================================

district_yearly = (
    district_df
    .groupby("year")
    ["landslide_events"]
    .sum()
    .reset_index()
)


fig = px.line(
    district_yearly,
    x="year",
    y="landslide_events",
    markers=True,
    title=f"{selected_district} — Historical Events"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TOP EVENT DAYS
# ============================================================

st.header("🔥 Highest Historical Event Days")


event_days = (
    df[
        df["landslide_events"] > 0
    ]
    .groupby("date")
    ["landslide_events"]
    .sum()
    .reset_index()
    .sort_values(
        "landslide_events",
        ascending=False
    )
    .head(20)
)


st.dataframe(
    event_days,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RAW DATA
# ============================================================

st.markdown("---")

with st.expander(
    "🔍 View Historical Dataset"
):

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )


# ============================================================
# DOWNLOAD
# ============================================================

csv = df.to_csv(
    index=False
)


st.download_button(
    "⬇️ Download Historical Dataset",
    csv,
    file_name="landslide_weather_master.csv",
    mime="text/csv"
)


# ============================================================
# LIMITATIONS
# ============================================================

st.markdown("---")

st.warning(
    """
    **Historical analysis limitations**

    • The historical dataset contains recorded events.

    • A day with zero recorded events does not necessarily
      prove that no landslide occurred.

    • Historical analysis covers the available dataset period.

    • Historical analysis should not be interpreted as
      future forecast information.
    """
)