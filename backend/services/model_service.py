import os
import json
import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "lankalandslide_final_model.pkl"
)

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "deployment_feature_columns.json"
)

CONFIG_PATH = os.path.join(
    MODEL_DIR,
    "deployment_config.json"
)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

if not os.path.exists(FEATURE_PATH):
    raise FileNotFoundError(
        f"Feature file not found: {FEATURE_PATH}"
    )

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(
        f"Config file not found: {CONFIG_PATH}"
    )


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    MODEL_PATH
)


# ============================================================
# LOAD FEATURE COLUMNS
# ============================================================

with open(
    FEATURE_PATH,
    "r"
) as file:

    FEATURE_COLUMNS = json.load(
        file
    )


# ============================================================
# HANDLE DIFFERENT JSON FORMATS
# ============================================================

if isinstance(
    FEATURE_COLUMNS,
    dict
):

    if "features" in FEATURE_COLUMNS:

        FEATURE_COLUMNS = FEATURE_COLUMNS["features"]

    elif "feature_columns" in FEATURE_COLUMNS:

        FEATURE_COLUMNS = FEATURE_COLUMNS["feature_columns"]


# ============================================================
# LOAD CONFIG
# ============================================================

with open(
    CONFIG_PATH,
    "r"
) as file:

    DEPLOYMENT_CONFIG = json.load(
        file
    )


# ============================================================
# THRESHOLD
# ============================================================

THRESHOLD = float(
    DEPLOYMENT_CONFIG.get(
        "threshold",
        0.50
    )
)


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_model_information():

    return {

        "model_name": DEPLOYMENT_CONFIG.get(
            "model_name",
            "LankaLandslide XGBoost"
        ),

        "model_type": type(model).__name__,

        "threshold": THRESHOLD,

        "number_of_features": len(
            FEATURE_COLUMNS
        ),

        "features": FEATURE_COLUMNS
    }


# ============================================================
# PREDICTION
# ============================================================

def predict(
    input_data
):

    # --------------------------------------------------------
    # Check missing features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in input_data
    ]

    if missing_features:

        raise ValueError(
            "Missing model features: "
            +
            ", ".join(
                missing_features
            )
        )


    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    input_df = pd.DataFrame(
        [input_data]
    )


    # --------------------------------------------------------
    # EXACT FEATURE ORDER
    # --------------------------------------------------------

    input_df = input_df[
        FEATURE_COLUMNS
    ]


    # --------------------------------------------------------
    # Convert numeric
    # --------------------------------------------------------

    for column in FEATURE_COLUMNS:

        input_df[column] = pd.to_numeric(
            input_df[column],
            errors="raise"
        )


    # --------------------------------------------------------
    # Check missing values
    # --------------------------------------------------------

    if input_df.isnull().any().any():

        raise ValueError(
            "Model input contains missing values."
        )


    # --------------------------------------------------------
    # Probability
    # --------------------------------------------------------

    if hasattr(
        model,
        "predict_proba"
    ):

        probability = float(
            model.predict_proba(
                input_df
            )[0][1]
        )

    else:

        prediction = int(
            model.predict(
                input_df
            )[0]
        )

        probability = float(
            prediction
        )


    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    risk = (
        "HIGH"
        if probability >= THRESHOLD
        else "LOW"
    )


    return {

        "probability": probability,

        "risk": risk,

        "threshold": THRESHOLD
    }