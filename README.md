# LankaLandslide AI

**Machine Learning-Based Landslide Risk Prediction and Location Intelligence System for Sri Lanka**

LankaLandslide AI is a district-level decision-support application that combines historical landslide records, daily weather information, and terrain features to estimate landslide risk for a selected Sri Lankan district and date. It integrates data preparation, machine learning, an API backend, and a user-facing web application.

> **Important:** This is an academic prototype, not an official warning system. Predictions are estimates and must not replace guidance from relevant Sri Lankan authorities.

## Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Data Sources](#data-sources)
- [Machine Learning Approach](#machine-learning-approach)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Evaluation](#evaluation)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## Project Overview

Landslides are a significant natural hazard in Sri Lanka. Their occurrence can be associated with rainfall patterns and terrain conditions. This project explores how machine learning can combine these factors to estimate landslide risk at **district-day level**.

The source collections cover different periods: landslide records span **1974–2019**, and the collected weather dataset spans **1998–2025**. The supervised modelling dataset uses the overlapping period **1998–2019**, when the required landslide labels and weather data are available. Terrain measurements are treated as static features rather than a time series.

## Key Features

- District-level risk prediction for a selected date.
- Historical weather inputs and available forecast data for supported near-future dates.
- Weather summaries, including rainfall, temperature, rain hours, and wind.
- A map view for comparing predicted risk across districts.
- Historical analysis of recorded landslide events.
- Model information and evaluation metrics.
- FastAPI backend and Streamlit frontend.

## Data Sources

| Data | Source | Coverage / use |
|---|---|---|
| Historical landslide records | [DesInventar Sri Lanka](https://www.desinventar.net/) | Source records span 1974–2019; the modelling dataset uses the overlapping period 1998–2019. |
| Daily weather | [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) and [Forecast API](https://open-meteo.com/en/docs) | Collected historical weather data spans 1998–2025; forecast inputs support selected near-future dates. |
| Terrain / elevation | [OpenTopography](https://opentopography.org/) using the Copernicus GLO-30 elevation dataset | Elevation and derived slope summaries used as static terrain features. |

The processed modelling dataset contains **192,840 district-day rows** across 24 districts for 1998–2019, with 844 positive recorded-event rows. A negative target means that no landslide was recorded for that district-day in the source dataset; it does not prove that no landslide occurred.

Most source landslide records did not include reliable coordinates. For this reason, the application is designed for district-level predictions rather than exact-site predictions.

## Machine Learning Approach

1. Collect landslide, weather, and terrain data.
2. Clean and standardize dates and district names.
3. Aggregate landslide records to district-day level and merge data by district and date.
4. Engineer rainfall accumulation features, heavy-rain indicators, seasonal features, weather features, and terrain features.
5. Train and compare Logistic Regression, Random Forest, XGBoost, and LSTM models.
6. Evaluate models using several metrics, with particular attention to recall and Precision–Recall AUC because recorded landslide days are rare.
7. Package the selected XGBoost model for API-based prediction.

Rainfall accumulation features use previous days' data to reduce target leakage. Target columns are not used as model input features.

### Deployed model

- **Model:** XGBoost (`XGBClassifier`)
- **Input features:** 27
- **Configured decision threshold:** 0.49

The threshold is a classification decision threshold; it must not be interpreted as a 49% real-world probability of a landslide.

### Final test-set results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7953 | 0.0110 | 0.9302 | 0.0218 | 0.9275 | 0.0261 |
| Random Forest | 0.9549 | 0.0254 | 0.4651 | 0.0481 | 0.8687 | 0.0241 |
| XGBoost | 0.9375 | 0.0236 | 0.6047 | 0.0453 | 0.9134 | 0.0278 |
| LSTM | 0.9226 | 0.0169 | 0.5349 | 0.0328 | 0.9011 | 0.0212 |

XGBoost was selected for deployment mainly because it achieved higher recall and PR-AUC than Random Forest on the final test set. It was **not** the best model on every metric. Low precision and PR-AUC also show that false positives and rare-event prediction remain important challenges.

## System Architecture

```text
Historical landslide records ─┐
Weather data / forecasts ─────┼──> Data preparation and feature engineering
Terrain features ─────────────┘                    │
                                                   ▼
                                         Trained XGBoost model
                                                   │
                                                   ▼
                                             FastAPI backend
                                                   │
                                                   ▼
                                            Streamlit frontend
                                  ┌────────────────┼────────────────┐
                                  ▼                ▼                ▼
                            Risk prediction    Risk map       Analysis pages
```

## Project Structure

```text
LankaLandslide-AI/
├── data/
│   ├── raw/
│   │   ├── landslides/
│   │   ├── weather/
│   │   └── terrain/
│   ├── processed/
│   └── features/
├── notebooks/
│   ├── 01_collect_landslide_data.ipynb
│   ├── 02_collect_weather_data.ipynb
│   ├── 03_clean_and_merge_data.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_collect_terrain_data.ipynb
│   ├── 06_train_models.ipynb
│   ├── 07_evaluate_model.ipynb
│   ├── 08_explain_model.ipynb
│   ├── 09_train_lstm.ipynb
│   └── 10_deployment_preparation.ipynb
├── models/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   ├── services/
│   └── routes/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── pages/
├── tests/
├── .gitignore
└── README.md
```

*The exact files present may vary as the project develops. Large raw datasets and trained model files may be stored separately from source control.*

## Getting Started

### Requirements

- Python 3.10 or a compatible Python version supported by the project dependencies.
- Git (optional, for cloning the repository).
- Internet access for live weather/forecast API requests.
- The trained model and deployment configuration files expected by the backend.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd LankaLandslide-AI
```

Replace the placeholder with your repository URL.

### 2. Set up and run the backend

On Windows Command Prompt:

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

The API should be available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Set up and run the frontend

Open a **second terminal** from the repository root:

```bat
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

If the frontend uses a configurable API URL, make sure it points to `http://127.0.0.1:8000`. Keep the backend running while using the frontend.

> **Setup note:** The backend must be able to locate the deployment model and its configuration files. If these files are not included in a fresh clone, obtain them from the project's approved storage or run the model-preparation notebook before starting the API.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Basic backend health check |
| `GET` | `/api/districts` | List supported districts |
| `GET` | `/api/model-info` | Return deployed model information |
| `GET` | `/api/prediction-health` | Check prediction service readiness |
| `POST` | `/api/predict` | Request a district-date risk prediction |

Example request body for `POST /api/predict`:

```json
{
  "district": "Colombo",
  "prediction_date": "2025-09-15"
}
```

The response includes the estimated probability, risk category, model name, configured threshold, and prediction unit. Exact response fields depend on the current API implementation.

## Limitations

- **Class imbalance:** Recorded landslide cases represent a small fraction of district-day rows.
- **Incomplete labels:** A day without a recorded event is treated as negative, although an event may have gone unreported.
- **Geographic resolution:** Predictions are at district level because reliable coordinates are missing for most source records.
- **Terrain representation:** Terrain summaries were derived from areas around district centres, not complete district-boundary polygons.
- **Forecast uncertainty:** Predictions for future dates depend on available weather forecasts and can change as forecasts update.
- **Model performance:** Low precision means false positives are a significant concern; predictions should be interpreted cautiously.
- **Decision support only:** This prototype is not validated or authorized as an official public warning system.

## Future Improvements

- Obtain more complete, georeferenced landslide records and improve label quality.
- Use district-boundary terrain summaries and more detailed spatial features.
- Evaluate probability calibration and tune decision thresholds for a clearly defined operational objective.
- Conduct additional temporal and geographic validation.
- Add monitoring, automated tests, logging, and model-version tracking.
- Work with relevant domain experts and authorities before considering operational use.

## Acknowledgements

This project uses publicly available disaster, weather, and elevation data from DesInventar, Open-Meteo, and OpenTopography/Copernicus. Please consult each provider's terms and attribution requirements before redistributing source data.

---

**Project:** LankaLandslide AI  
**Purpose:** Academic capstone project and machine-learning decision-support prototype  
**Prediction unit:** District-day
