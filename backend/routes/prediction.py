# from datetime import date, timedelta

# import numpy as np

# from fastapi import (
#     APIRouter,
#     HTTPException
# )

# from pydantic import BaseModel


# from services.weather_service import (
#     DISTRICTS,
#     get_historical_weather
# )

# from services.feature_service import (
#     build_model_input,
#     standardize_district
# )

# from services.model_service import (
#     predict,
#     get_model_information
# )


# # ============================================================
# # ROUTER
# # ============================================================

# router = APIRouter(
#     prefix="/api",
#     tags=["Landslide Prediction"]
# )


# # ============================================================
# # REQUEST
# # ============================================================

# class PredictionRequest(
#     BaseModel
# ):

#     district: str

#     prediction_date: date


# # ============================================================
# # DISTRICTS
# # ============================================================

# @router.get(
#     "/districts"
# )
# def districts():

#     return {

#         "count": len(
#             DISTRICTS
#         ),

#         "districts": sorted(
#             DISTRICTS.keys()
#         )
#     }


# # ============================================================
# # MODEL INFORMATION
# # ============================================================

# @router.get(
#     "/model-info"
# )
# def model_info():

#     return get_model_information()


# # ============================================================
# # PREDICTION HEALTH
# # ============================================================

# @router.get(
#     "/prediction-health"
# )
# def prediction_health():

#     return {

#         "status": "ready",

#         "service":
#             "LankaLandslide AI",

#         "model":
#             "loaded"
#     }


# # ============================================================
# # PREDICTION
# # ============================================================

# @router.post(
#     "/predict"
# )
# def predict_landslide(
#     request: PredictionRequest
# ):

#     try:

#         # ----------------------------------------------------
#         # District
#         # ----------------------------------------------------

#         district = standardize_district(
#             request.district
#         )


#         if district not in DISTRICTS:

#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     f"Unsupported district: {district}"
#                 )
#             )


#         # ----------------------------------------------------
#         # Target date
#         # ----------------------------------------------------

#         target_date = request.prediction_date


#         # ----------------------------------------------------
#         # We need 30 previous days
#         # ----------------------------------------------------

#         start_date = (
#             target_date
#             -
#             timedelta(
#                 days=35
#             )
#         )


#         # ----------------------------------------------------
#         # Weather
#         # ----------------------------------------------------

#         weather_df = get_historical_weather(

#             district,

#             start_date.strftime(
#                 "%Y-%m-%d"
#             ),

#             target_date.strftime(
#                 "%Y-%m-%d"
#             )
#         )


#         # ----------------------------------------------------
#         # Check data
#         # ----------------------------------------------------

#         if len(weather_df) < 30:

#             raise HTTPException(

#                 status_code=400,

#                 detail=(
#                     "Not enough weather history "
#                     "to calculate rainfall features."
#                 )
#             )


#         # ----------------------------------------------------
#         # Build model input
#         # ----------------------------------------------------

#         model_input = build_model_input(

#             weather_df,

#             district,

#             target_date
#         )


#         # ----------------------------------------------------
#         # Prediction
#         # ----------------------------------------------------

#         result = predict(
#             model_input
#         )


#         # ----------------------------------------------------
#         # Message
#         # ----------------------------------------------------

#         if result["risk"] == "HIGH":

#             message = (
#                 "The model estimates elevated "
#                 "landslide risk for the selected "
#                 "district and date."
#             )

#         else:

#             message = (
#                 "The model estimates lower "
#                 "landslide risk for the selected "
#                 "district and date."
#             )


#         # ----------------------------------------------------
#         # Return
#         # ----------------------------------------------------

#         return {

#             "success": True,

#             "project":
#                 "LankaLandslide AI",

#             "district":
#                 district,

#             "prediction_date":
#                 target_date.strftime(
#                     "%Y-%m-%d"
#                 ),

#             "probability":
#                 round(
#                     result["probability"],
#                     4
#                 ),

#             "risk":
#                 result["risk"],

#             "threshold":
#                 result["threshold"],

#             "model":
#                 "XGBoost",

#             "prediction_unit":
#                 "district-day",

#             "message":
#                 message,

#             "features_used":
#                 {
#                     key:
#                     (
#                         round(
#                             float(value),
#                             4
#                         )
#                         if isinstance(
#                             value,
#                             (
#                                 float,
#                                 int,
#                                 np.floating,
#                                 np.integer
#                             )
#                         )
#                         else value
#                     )

#                     for key, value
#                     in model_input.items()
#                 }
#         }


#     except HTTPException:

#         raise


#     except Exception as error:

#         raise HTTPException(

#             status_code=500,

#             detail=str(error)
#         )
from datetime import date

import numpy as np

from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel


from services.weather_service import (
    DISTRICTS,
    get_weather_for_prediction,
    validate_prediction_date
)

from services.feature_service import (
    build_model_input,
    standardize_district
)

from services.model_service import (
    predict,
    get_model_information
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["Landslide Prediction"]
)


# ============================================================
# REQUEST
# ============================================================

class PredictionRequest(
    BaseModel
):

    district: str

    prediction_date: date


# ============================================================
# DISTRICTS
# ============================================================

@router.get(
    "/districts"
)
def districts():

    return {

        "count": len(
            DISTRICTS
        ),

        "districts": sorted(
            DISTRICTS.keys()
        )
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

@router.get(
    "/model-info"
)
def model_info():

    return get_model_information()


# ============================================================
# PREDICTION HEALTH
# ============================================================

@router.get(
    "/prediction-health"
)
def prediction_health():

    return {

        "status": "ready",

        "service":
            "LankaLandslide AI",

        "model":
            "loaded"
    }


# ============================================================
# PREDICTION
# ============================================================

@router.post(
    "/predict"
)
def predict_landslide(
    request: PredictionRequest
):

    try:

        # ====================================================
        # DISTRICT
        # ====================================================

        district = standardize_district(
            request.district
        )

        if district not in DISTRICTS:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported district: {district}"
                )
            )


        # ====================================================
        # TARGET DATE
        # ====================================================

        target_date = request.prediction_date

        # Validate future prediction range
        validate_prediction_date(
            target_date
        )


        # ====================================================
        # WEATHER
        # ====================================================
        #
        # IMPORTANT:
        #
        # We now use the HYBRID weather service.
        #
        # Past date:
        #     Historical weather
        #
        # Today:
        #     Historical + today's forecast
        #
        # Future date:
        #     Historical previous 35 days
        #     +
        #     Forecast today → target date
        #
        # ====================================================

        weather_df = get_weather_for_prediction(

            district=district,

            prediction_date=target_date
        )


        # ====================================================
        # CHECK WEATHER DATA
        # ====================================================

        if weather_df.empty:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No weather data was returned "
                    "for the selected date."
                )
            )


        # ====================================================
        # BUILD MODEL INPUT
        # ====================================================

        model_input = build_model_input(

            weather_df,

            district,

            target_date
        )


        # ====================================================
        # CHECK MODEL INPUT
        # ====================================================

        if model_input is None:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Unable to create model input "
                    "from weather data."
                )
            )


        # ====================================================
        # PREDICTION
        # ====================================================

        result = predict(
            model_input
        )


        # ====================================================
        # MESSAGE
        # ====================================================

        if result["risk"] == "HIGH":

            message = (
                "The model estimates elevated "
                "landslide risk for the selected "
                "district and date."
            )

        else:

            message = (
                "The model estimates lower "
                "landslide risk for the selected "
                "district and date."
            )


        # ====================================================
        # RETURN
        # ====================================================

        return {

            "success":
                True,

            "project":
                "LankaLandslide AI",

            "district":
                district,

            "prediction_date":
                target_date.strftime(
                    "%Y-%m-%d"
                ),

            "probability":
                round(
                    float(
                        result["probability"]
                    ),
                    4
                ),

            "risk":
                result["risk"],

            "threshold":
                result["threshold"],

            "model":
                "XGBoost",

            "prediction_unit":
                "district-day",

            "message":
                message,

            "features_used":
                {
                    key:
                    (
                        round(
                            float(value),
                            4
                        )

                        if isinstance(
                            value,
                            (
                                float,
                                int,
                                np.floating,
                                np.integer
                            )
                        )

                        else value
                    )

                    for key, value
                    in model_input.items()
                }
        }


    # ========================================================
    # FASTAPI HTTP ERRORS
    # ========================================================

    except HTTPException:

        raise


    # ========================================================
    # OTHER ERRORS
    # ========================================================

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )