import requests
import pandas as pd
from datetime import date, timedelta


# ============================================================
# SRI LANKA DISTRICT CENTERS
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
    "Ampara": (7.2917, 81.6720),
}


# ============================================================
# API URLS
# ============================================================

HISTORICAL_API = (
    "https://archive-api.open-meteo.com/v1/archive"
)

FORECAST_API = (
    "https://api.open-meteo.com/v1/forecast"
)


# ============================================================
# WEATHER VARIABLES
# ============================================================

DAILY_VARIABLES = [
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
]


# ============================================================
# GET DISTRICT COORDINATES
# ============================================================

def get_coordinates(district):

    if district not in DISTRICTS:
        raise ValueError(
            f"Unknown district: {district}"
        )

    return DISTRICTS[district]


# ============================================================
# VALIDATE PREDICTION DATE
# ============================================================

def validate_prediction_date(prediction_date):

    requested_date = pd.to_datetime(
        prediction_date
    ).date()

    today = date.today()

    maximum_date = today + timedelta(days=16)

    if requested_date > maximum_date:

        raise ValueError(
            f"Future weather forecasts are available only "
            f"up to {maximum_date}."
        )

    return requested_date


# ============================================================
# GET HISTORICAL WEATHER
# ============================================================

def get_historical_weather(
    district,
    start_date,
    end_date
):

    latitude, longitude = get_coordinates(
        district
    )

    params = {

        "latitude": latitude,
        "longitude": longitude,

        "start_date": start_date,
        "end_date": end_date,

        "daily": ",".join(
            DAILY_VARIABLES
        ),

        "timezone": "Asia/Colombo",

        "models": "era5",
    }

    response = requests.get(
        HISTORICAL_API,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if "daily" not in data:

        raise ValueError(
            "Historical API did not return daily data."
        )

    df = pd.DataFrame(
        data["daily"]
    )

    if df.empty:

        raise ValueError(
            "Historical weather data is empty."
        )

    df["date"] = pd.to_datetime(
        df["time"]
    )

    df = df.drop(
        columns=["time"]
    )

    return format_weather_dataframe(
        df,
        district
    )


# ============================================================
# GET FORECAST WEATHER
# ============================================================

def get_forecast_weather(
    district,
    start_date,
    end_date
):

    latitude, longitude = get_coordinates(
        district
    )

    today = date.today()

    maximum_date = today + timedelta(days=16)

    requested_start = pd.to_datetime(
        start_date
    ).date()

    requested_end = pd.to_datetime(
        end_date
    ).date()

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if requested_start < today:

        raise ValueError(
            "Forecast start date cannot be before today."
        )

    if requested_end > maximum_date:

        raise ValueError(
            f"Forecast only available until "
            f"{maximum_date}."
        )

    params = {

        "latitude": latitude,
        "longitude": longitude,

        "daily": ",".join(
            DAILY_VARIABLES
        ),

        "timezone": "Asia/Colombo",

        "forecast_days": 16,
    }

    response = requests.get(
        FORECAST_API,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if "daily" not in data:

        raise ValueError(
            "Forecast API did not return daily data."
        )

    df = pd.DataFrame(
        data["daily"]
    )

    if df.empty:

        raise ValueError(
            "Forecast weather data is empty."
        )

    df["date"] = pd.to_datetime(
        df["time"]
    )

    df = df.drop(
        columns=["time"]
    )

    # --------------------------------------------------------
    # Keep requested range
    # --------------------------------------------------------

    df = df[
        (df["date"] >= pd.to_datetime(start_date))
        &
        (df["date"] <= pd.to_datetime(end_date))
    ].copy()

    if df.empty:

        raise ValueError(
            f"No forecast data available between "
            f"{start_date} and {end_date}."
        )

    return format_weather_dataframe(
        df,
        district
    )


# ============================================================
# FORMAT WEATHER DATA
# ============================================================

def format_weather_dataframe(
    df,
    district
):

    rename_map = {

        "precipitation_sum":
            "rainfall_mm",

        "rain_sum":
            "rain_mm",

        "precipitation_hours":
            "rain_hours",

        "temperature_2m_max":
            "temp_max",

        "temperature_2m_min":
            "temp_min",

        "temperature_2m_mean":
            "temp_mean",

        "wind_speed_10m_max":
            "wind_max",

        "wind_gusts_10m_max":
            "wind_gust_max",
    }

    df = df.rename(
        columns=rename_map
    )

    # --------------------------------------------------------
    # District
    # --------------------------------------------------------

    df["district"] = district

    latitude, longitude = get_coordinates(
        district
    )

    df["latitude"] = latitude
    df["longitude"] = longitude

    # --------------------------------------------------------
    # Expected columns
    # --------------------------------------------------------

    expected_columns = [

        "date",

        "rainfall_mm",
        "rain_mm",
        "rain_hours",

        "temp_max",
        "temp_min",
        "temp_mean",

        "wind_max",
        "wind_gust_max",

        "district",

        "latitude",
        "longitude",
    ]

    # --------------------------------------------------------
    # Create missing columns
    # --------------------------------------------------------

    for column in expected_columns:

        if column not in df.columns:

            df[column] = 0.0

    # --------------------------------------------------------
    # Select columns
    # --------------------------------------------------------

    df = df[
        expected_columns
    ]

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = (
        df
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df


# ============================================================
# HYBRID WEATHER SERVICE
# ============================================================

def get_weather_for_prediction(
    district,
    prediction_date
):

    requested_date = validate_prediction_date(
        prediction_date
    )

    today = date.today()

    # ========================================================
    # CASE 1 — PAST DATE
    # ========================================================

    if requested_date < today:

        historical_start = (
            requested_date -
            timedelta(days=35)
        )

        historical_end = requested_date

        return get_historical_weather(

            district=district,

            start_date=
                historical_start.strftime(
                    "%Y-%m-%d"
                ),

            end_date=
                historical_end.strftime(
                    "%Y-%m-%d"
                )
        )

    # ========================================================
    # CASE 2 — TODAY
    # ========================================================

    if requested_date == today:

        # ----------------------------------------------------
        # Previous 35 days
        # ----------------------------------------------------

        historical_start = (
            today -
            timedelta(days=35)
        )

        historical_end = (
            today -
            timedelta(days=1)
        )

        historical_df = get_historical_weather(

            district=district,

            start_date=
                historical_start.strftime(
                    "%Y-%m-%d"
                ),

            end_date=
                historical_end.strftime(
                    "%Y-%m-%d"
                )
        )

        # ----------------------------------------------------
        # Today's forecast
        # ----------------------------------------------------

        forecast_df = get_forecast_weather(

            district=district,

            start_date=
                today.strftime(
                    "%Y-%m-%d"
                ),

            end_date=
                today.strftime(
                    "%Y-%m-%d"
                )
        )

        # ----------------------------------------------------
        # Combine
        # ----------------------------------------------------

        combined = pd.concat(
            [
                historical_df,
                forecast_df
            ],
            ignore_index=True
        )

        combined = (
            combined
            .drop_duplicates(
                subset=["date"],
                keep="last"
            )
            .sort_values("date")
            .reset_index(drop=True)
        )

        return combined

    # ========================================================
    # CASE 3 — FUTURE DATE
    # ========================================================

    # --------------------------------------------------------
    # Historical period
    #
    # IMPORTANT:
    # Historical API stops at yesterday.
    # --------------------------------------------------------

    historical_start = (
        today -
        timedelta(days=35)
    )

    historical_end = (
        today -
        timedelta(days=1)
    )

    historical_df = get_historical_weather(

        district=district,

        start_date=
            historical_start.strftime(
                "%Y-%m-%d"
            ),

        end_date=
            historical_end.strftime(
                "%Y-%m-%d"
            )
    )

    # --------------------------------------------------------
    # Forecast period
    #
    # Starts today and continues to prediction date.
    # --------------------------------------------------------

    forecast_df = get_forecast_weather(

        district=district,

        start_date=
            today.strftime(
                "%Y-%m-%d"
            ),

        end_date=
            requested_date.strftime(
                "%Y-%m-%d"
            )
    )

    # --------------------------------------------------------
    # Combine historical + forecast
    # --------------------------------------------------------

    combined = pd.concat(
        [
            historical_df,
            forecast_df
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # Remove duplicate dates
    #
    # If today's date appears in both sources,
    # keep the forecast version.
    # --------------------------------------------------------

    combined = (
        combined
        .drop_duplicates(
            subset=["date"],
            keep="last"
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    return combined