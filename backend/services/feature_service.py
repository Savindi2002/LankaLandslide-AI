# import os
# import numpy as np
# import pandas as pd


# # ============================================================
# # PROJECT PATH
# # ============================================================

# BASE_DIR = os.path.dirname(
#     os.path.dirname(
#         os.path.abspath(__file__)
#     )
# )


# PROJECT_DIR = os.path.dirname(
#     BASE_DIR
# )


# TERRAIN_PATH = os.path.join(
#     PROJECT_DIR,
#     "data",
#     "processed",
#     "district_terrain_features.csv"
# )


# # ============================================================
# # LOAD TERRAIN DATA
# # ============================================================

# if not os.path.exists(
#     TERRAIN_PATH
# ):

#     raise FileNotFoundError(
#         "Terrain file not found: "
#         + TERRAIN_PATH
#     )


# TERRAIN_DF = pd.read_csv(
#     TERRAIN_PATH
# )


# # ============================================================
# # STANDARDIZE DISTRICT
# # ============================================================

# def standardize_district(
#     district
# ):

#     district = district.strip()

#     if district == "Moneragala":

#         district = "Monaragala"

#     return district


# # ============================================================
# # WEATHER FEATURES
# # ============================================================

# def create_weather_features(
#     weather_df
# ):

#     df = weather_df.copy()


#     df["date"] = pd.to_datetime(
#         df["date"]
#     )


#     df = df.sort_values(
#         "date"
#     ).reset_index(
#         drop=True
#     )


#     # --------------------------------------------------------
#     # Rainfall windows
#     # --------------------------------------------------------

#     df["rainfall_1day"] = (
#         df["rainfall_mm"]
#         .shift(1)
#     )


#     df["rainfall_3day"] = (
#         df["rainfall_mm"]
#         .shift(1)
#         .rolling(
#             3,
#             min_periods=3
#         )
#         .sum()
#     )


#     df["rainfall_7day"] = (
#         df["rainfall_mm"]
#         .shift(1)
#         .rolling(
#             7,
#             min_periods=7
#         )
#         .sum()
#     )


#     df["rainfall_14day"] = (
#         df["rainfall_mm"]
#         .shift(1)
#         .rolling(
#             14,
#             min_periods=14
#         )
#         .sum()
#     )


#     df["rainfall_30day"] = (
#         df["rainfall_mm"]
#         .shift(1)
#         .rolling(
#             30,
#             min_periods=30
#         )
#         .sum()
#     )


#     # --------------------------------------------------------
#     # Rainfall averages
#     # --------------------------------------------------------

#     df["rainfall_3day_avg"] = (
#         df["rainfall_3day"] / 3
#     )

#     df["rainfall_7day_avg"] = (
#         df["rainfall_7day"] / 7
#     )

#     df["rainfall_14day_avg"] = (
#         df["rainfall_14day"] / 14
#     )

#     df["rainfall_30day_avg"] = (
#         df["rainfall_30day"] / 30
#     )


#     # --------------------------------------------------------
#     # Temperature
#     # --------------------------------------------------------

#     df["temperature_range"] = (
#         df["temp_max"]
#         -
#         df["temp_min"]
#     )


#     # --------------------------------------------------------
#     # Calendar
#     # --------------------------------------------------------

#     df["month"] = (
#         df["date"].dt.month
#     )

#     df["day_of_year"] = (
#         df["date"].dt.dayofyear
#     )


#     df["month_sin"] = np.sin(
#         2 * np.pi * df["month"] / 12
#     )


#     df["month_cos"] = np.cos(
#         2 * np.pi * df["month"] / 12
#     )


#     # --------------------------------------------------------
#     # Heavy rainfall
#     # --------------------------------------------------------

#     df["heavy_rain_10mm"] = (
#         df["rainfall_mm"] >= 10
#     ).astype(int)


#     df["heavy_rain_25mm"] = (
#         df["rainfall_mm"] >= 25
#     ).astype(int)


#     df["heavy_rain_50mm"] = (
#         df["rainfall_mm"] >= 50
#     ).astype(int)


#     df["heavy_rain_100mm"] = (
#         df["rainfall_mm"] >= 100
#     ).astype(int)


#     return df


# # ============================================================
# # TERRAIN FEATURES
# # ============================================================

# def get_terrain_features(
#     district
# ):

#     district = standardize_district(
#         district
#     )


#     matches = TERRAIN_DF[
#         TERRAIN_DF["district"].astype(str).str.lower()
#         ==
#         district.lower()
#     ]


#     if matches.empty:

#         raise ValueError(
#             f"No terrain data found for {district}"
#         )


#     row = matches.iloc[0]


#     terrain = {}


#     # --------------------------------------------------------
#     # Automatically take numeric terrain columns
#     # --------------------------------------------------------

#     for column in TERRAIN_DF.columns:

#         if column == "district":

#             continue


#         value = row[column]


#         if pd.notna(value):

#             try:

#                 terrain[column] = float(
#                     value
#                 )

#             except (
#                 ValueError,
#                 TypeError
#             ):

#                 pass


#     return terrain


# # ============================================================
# # BUILD INPUT
# # ============================================================

# def build_model_input(
#     weather_df,
#     district,
#     target_date
# ):

#     df = create_weather_features(
#         weather_df
#     )


#     target_date = pd.to_datetime(
#         target_date
#     )


#     rows = df[
#         df["date"] == target_date
#     ]


#     if rows.empty:

#         raise ValueError(
#             f"No weather data available for {target_date.date()}"
#         )


#     row = rows.iloc[-1]


#     # --------------------------------------------------------
#     # Weather features
#     # --------------------------------------------------------

#     model_input = {}


#     weather_columns = [

#         "rainfall_mm",

#         "rain_mm",

#         "rain_hours",

#         "temp_max",

#         "temp_min",

#         "temp_mean",

#         "wind_max",

#         "wind_gust_max",

#         "rainfall_1day",

#         "rainfall_3day",

#         "rainfall_7day",

#         "rainfall_14day",

#         "rainfall_30day",

#         "rainfall_3day_avg",

#         "rainfall_7day_avg",

#         "rainfall_14day_avg",

#         "rainfall_30day_avg",

#         "temperature_range",

#         "month",

#         "day_of_year",

#         "month_sin",

#         "month_cos",

#         "heavy_rain_10mm",

#         "heavy_rain_25mm",

#         "heavy_rain_50mm",

#         "heavy_rain_100mm"
#     ]


#     for column in weather_columns:

#         if column in row.index:

#             model_input[column] = float(
#                 row[column]
#             )


#     # --------------------------------------------------------
#     # Terrain
#     # --------------------------------------------------------

#     terrain = get_terrain_features(
#         district
#     )


#     model_input.update(
#         terrain
#     )


#     return model_input
import os
import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


PROJECT_DIR = os.path.dirname(
    BASE_DIR
)


TERRAIN_PATH = os.path.join(
    PROJECT_DIR,
    "data",
    "processed",
    "district_terrain_features.csv"
)


# ============================================================
# LOAD TERRAIN DATA
# ============================================================

if not os.path.exists(
    TERRAIN_PATH
):

    raise FileNotFoundError(
        "Terrain file not found: "
        + TERRAIN_PATH
    )


TERRAIN_DF = pd.read_csv(
    TERRAIN_PATH
)


# ============================================================
# STANDARDIZE DISTRICT
# ============================================================

def standardize_district(
    district
):

    district = str(
        district
    ).strip()

    if district == "Moneragala":

        district = "Monaragala"

    return district


# ============================================================
# CLEAN WEATHER DATA
# ============================================================

def clean_weather_data(
    weather_df
):

    df = weather_df.copy()


    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )


    df = df.dropna(
        subset=["date"]
    )


    df = df.sort_values(
        "date"
    ).reset_index(
        drop=True
    )


    # --------------------------------------------------------
    # Numeric weather columns
    # --------------------------------------------------------

    numeric_columns = [

        "rainfall_mm",

        "rain_mm",

        "rain_hours",

        "temp_max",

        "temp_min",

        "temp_mean",

        "wind_max",

        "wind_gust_max"
    ]


    for column in numeric_columns:

        if column not in df.columns:

            df[column] = np.nan

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    # --------------------------------------------------------
    # Fill missing values
    #
    # IMPORTANT:
    # We use previous available values first.
    # We do NOT use future values for filling.
    # --------------------------------------------------------

    for column in numeric_columns:

        series = df[column]


        # Previous available value
        series = series.ffill()


        # If the beginning is missing,
        # use the median of available observations.
        if series.isna().any():

            median_value = series.median()

            if pd.isna(
                median_value
            ):

                median_value = 0.0


            series = series.fillna(
                median_value
            )


        df[column] = series


    return df


# ============================================================
# WEATHER FEATURES
# ============================================================

def create_weather_features(
    weather_df
):

    # --------------------------------------------------------
    # Clean raw weather data first
    # --------------------------------------------------------

    df = clean_weather_data(
        weather_df
    )


    # --------------------------------------------------------
    # Rainfall windows
    #
    # shift(1) is intentional:
    # rainfall features represent rainfall BEFORE
    # the prediction day.
    # --------------------------------------------------------

    df["rainfall_1day"] = (
        df["rainfall_mm"]
        .shift(1)
    )


    df["rainfall_3day"] = (
        df["rainfall_mm"]
        .shift(1)
        .rolling(
            3,
            min_periods=3
        )
        .sum()
    )


    df["rainfall_7day"] = (
        df["rainfall_mm"]
        .shift(1)
        .rolling(
            7,
            min_periods=7
        )
        .sum()
    )


    df["rainfall_14day"] = (
        df["rainfall_mm"]
        .shift(1)
        .rolling(
            14,
            min_periods=14
        )
        .sum()
    )


    df["rainfall_30day"] = (
        df["rainfall_mm"]
        .shift(1)
        .rolling(
            30,
            min_periods=30
        )
        .sum()
    )


    # --------------------------------------------------------
    # Fill rolling feature edge cases
    # --------------------------------------------------------

    rolling_columns = [

        "rainfall_1day",

        "rainfall_3day",

        "rainfall_7day",

        "rainfall_14day",

        "rainfall_30day"
    ]


    for column in rolling_columns:

        if df[column].isna().any():

            df[column] = (
                df[column]
                .bfill()
            )


        if df[column].isna().any():

            df[column] = (
                df[column]
                .fillna(0.0)
            )


    # --------------------------------------------------------
    # Rainfall averages
    # --------------------------------------------------------

    df["rainfall_3day_avg"] = (
        df["rainfall_3day"] / 3
    )


    df["rainfall_7day_avg"] = (
        df["rainfall_7day"] / 7
    )


    df["rainfall_14day_avg"] = (
        df["rainfall_14day"] / 14
    )


    df["rainfall_30day_avg"] = (
        df["rainfall_30day"] / 30
    )


    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    df["temperature_range"] = (
        df["temp_max"]
        -
        df["temp_min"]
    )


    # --------------------------------------------------------
    # Calendar
    # --------------------------------------------------------

    df["month"] = (
        df["date"].dt.month
    )


    df["day_of_year"] = (
        df["date"].dt.dayofyear
    )


    df["month_sin"] = np.sin(
        2
        * np.pi
        * df["month"]
        / 12
    )


    df["month_cos"] = np.cos(
        2
        * np.pi
        * df["month"]
        / 12
    )


    # --------------------------------------------------------
    # Heavy rainfall
    # --------------------------------------------------------

    df["heavy_rain_10mm"] = (
        df["rainfall_mm"] >= 10
    ).astype(int)


    df["heavy_rain_25mm"] = (
        df["rainfall_mm"] >= 25
    ).astype(int)


    df["heavy_rain_50mm"] = (
        df["rainfall_mm"] >= 50
    ).astype(int)


    df["heavy_rain_100mm"] = (
        df["rainfall_mm"] >= 100
    ).astype(int)


    return df


# ============================================================
# TERRAIN FEATURES
# ============================================================

def get_terrain_features(
    district
):

    district = standardize_district(
        district
    )


    matches = TERRAIN_DF[
        TERRAIN_DF["district"]
        .astype(str)
        .str.lower()
        ==
        district.lower()
    ]


    if matches.empty:

        raise ValueError(
            f"No terrain data found for {district}"
        )


    row = matches.iloc[0]


    terrain = {}


    # --------------------------------------------------------
    # Automatically take numeric terrain columns
    # --------------------------------------------------------

    for column in TERRAIN_DF.columns:

        if column == "district":

            continue


        value = row[column]


        if pd.notna(value):

            try:

                terrain[column] = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):

                pass


    return terrain


# ============================================================
# BUILD MODEL INPUT
# ============================================================

def build_model_input(
    weather_df,
    district,
    target_date
):

    # --------------------------------------------------------
    # Create all weather features
    # --------------------------------------------------------

    df = create_weather_features(
        weather_df
    )


    target_date = pd.to_datetime(
        target_date
    )


    # --------------------------------------------------------
    # Find target date
    # --------------------------------------------------------

    rows = df[
        df["date"] == target_date
    ]


    if rows.empty:

        raise ValueError(
            f"No weather data available for "
            f"{target_date.date()}"
        )


    row = rows.iloc[-1]


    # --------------------------------------------------------
    # Weather features
    # --------------------------------------------------------

    model_input = {}


    weather_columns = [

        "rainfall_mm",

        "rain_mm",

        "rain_hours",

        "temp_max",

        "temp_min",

        "temp_mean",

        "wind_max",

        "wind_gust_max",

        "rainfall_1day",

        "rainfall_3day",

        "rainfall_7day",

        "rainfall_14day",

        "rainfall_30day",

        "rainfall_3day_avg",

        "rainfall_7day_avg",

        "rainfall_14day_avg",

        "rainfall_30day_avg",

        "temperature_range",

        "month",

        "day_of_year",

        "month_sin",

        "month_cos",

        "heavy_rain_10mm",

        "heavy_rain_25mm",

        "heavy_rain_50mm",

        "heavy_rain_100mm"
    ]


    # --------------------------------------------------------
    # Add weather features
    # --------------------------------------------------------

    for column in weather_columns:

        if column not in row.index:

            raise ValueError(
                f"Required weather feature "
                f"missing: {column}"
            )


        value = row[column]


        if pd.isna(value):

            raise ValueError(
                f"Weather feature contains "
                f"missing value: {column}"
            )


        model_input[column] = float(
            value
        )


    # --------------------------------------------------------
    # Terrain
    # --------------------------------------------------------

    terrain = get_terrain_features(
        district
    )


    model_input.update(
        terrain
    )


    # --------------------------------------------------------
    # Final NaN / Infinity safety check
    # --------------------------------------------------------

    invalid_features = []


    for key, value in model_input.items():

        try:

            numeric_value = float(
                value
            )


            if not np.isfinite(
                numeric_value
            ):

                invalid_features.append(
                    key
                )

        except (
            ValueError,
            TypeError
        ):

            invalid_features.append(
                key
            )


    if invalid_features:

        raise ValueError(
            "Model input contains invalid "
            "values: "
            +
            ", ".join(
                invalid_features
            )
        )


    return model_input