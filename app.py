import importlib
import json
import subprocess
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit  as st

# Must be the first Streamlit command in the script.
st.set_page_config(
    page_title="Smarrt Outcome Predictor",
    page_icon="🎓",
    layout="wide"
)


def ensure_package(module_name, pip_name=None):
    """Import a package; if it is missing, install it with the same Python
    that is running this app, then import it."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pass
    try:
        st.info(f"Installing missing package '{pip_name or module_name}'. This can take a minute...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pip_name or module_name]
        )
        importlib.invalidate_caches()
        return importlib.import_module(module_name)
    except Exception as exc:
        st.error(
            f"Could not install '{pip_name or module_name}' automatically ({exc}).\n\n"
            f"Please run this in a terminal and restart the app:\n\n"
            f"python -m pip install {pip_name or module_name}"
        )
        st.stop()


# The saved models were trained with XGBoost, so it must be importable
# before the .pkl files are loaded.
ensure_package("xgboost")

# Project PAth

# Find the project folder. This also works when app.py sits one level above
# (or below) the folder that contains "model" and "outputs".
app_dir = Path(__file__).resolve().parent
_candidates = [
    app_dir,
    app_dir / "Smart-Outcome-Predictor-main",
    app_dir.parent,
]
base_path = next((p for p in _candidates if (p / "model").is_dir()), app_dir)
schema_path = base_path/"outputs"/"input_schema.json"

classifier_path = base_path/"model"/"best_classifiction_model.pkl"

regressor_path = base_path/"model"/"best_regression_model.pkl"


# Built-in copy of outputs/input_schema.json (used if that file is missing)
DEFAULT_SCHEMA = {
    "age": {
        "type": "numeric",
        "default": 24.0,
        "min": 16.0,
        "max": 45.0
    },
    "country_region": {
        "type": "categorical",
        "default": "Asia",
        "choices": [
            "Africa",
            "Americas",
            "Asia",
            "Europe",
            "Oceania"
        ]
    },
    "device_type": {
        "type": "categorical",
        "default": "Mobile",
        "choices": [
            "Laptop",
            "Mobile",
            "Tablet"
        ]
    },
    "education_background": {
        "type": "categorical",
        "default": "Undergrad",
        "choices": [
            "Graduate",
            "HighSchool",
            "Undergrad",
            "WorkingPro"
        ]
    },
    "course_level": {
        "type": "categorical",
        "default": "Beginner",
        "choices": [
            "Advanced",
            "Beginner",
            "Intermediate"
        ]
    },
    "course_category": {
        "type": "categorical",
        "default": "Data",
        "choices": [
            "Business",
            "Data",
            "Design",
            "Marketing",
            "Programming"
        ]
    },
    "week_of_year": {
        "type": "numeric",
        "default": 27.0,
        "min": 1.0,
        "max": 52.0
    },
    "sessions": {
        "type": "numeric",
        "default": 17.0,
        "min": 1.0,
        "max": 94.0
    },
    "time_spent_hours": {
        "type": "numeric",
        "default": 16.1,
        "min": 0.6,
        "max": 76.8
    },
    "videos_watched": {
        "type": "numeric",
        "default": 23.0,
        "min": 0.0,
        "max": 158.0
    },
    "quiz_attempts": {
        "type": "numeric",
        "default": 7.0,
        "min": 0.0,
        "max": 20.0
    },
    "assignments_submitted": {
        "type": "numeric",
        "default": 4.0,
        "min": 0.0,
        "max": 12.0
    },
    "forum_posts": {
        "type": "numeric",
        "default": 1.0,
        "min": 0.0,
        "max": 8.0
    },
    "avg_quiz_score": {
        "type": "numeric",
        "default": 66.8,
        "min": 0.0,
        "max": 100.0
    },
    "attendance_rate": {
        "type": "numeric",
        "default": 0.855,
        "min": 0.404,
        "max": 1.0
    },
    "couse_durection_day": {
        "type": "numeric",
        "default": 180.0,
        "min": 0.0,
        "max": 364.0
    }
}


@st.cache_data
def load_schema(path):
    """Load the input schema. If the file is missing, rebuild it from the
    built-in copy and save it so the app keeps working."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_SCHEMA, file, indent=2)
        return DEFAULT_SCHEMA
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_resource
def load_model(path):
    return joblib.load(path)



st.title("🎓 Smart Outcome Predictor")
st.write(
    "Enter student and course details to predict course completion "
    "and estimate the final score."
)

schema_file = schema_path
classifier_file = classifier_path
regressor_file = regressor_path


for model_file in (classifier_file, regressor_file):
    if not Path(model_file).exists():
        st.error(
            f"Model file not found: {model_file}\n\n"
            "Re-extract the project zip so the 'model' folder is included."
        )
        st.stop()

schema = load_schema(str(schema_file))
classifier = load_model(str(classifier_file))
regressor = load_model(str(regressor_file))


st.subheader("Student details")
st.caption("Numeric fields use training-data ranges; categorical fields use values from the training data.")

with st.form("student_input_form"):
    user_data = {}
    numeric_cols = [
        col for col,info in schema.items()
        if info.get("type") == "numeric"
    ]

    categorical_cols = [
        col for col,info in schema.items()
        if info.get("type") == "categorical"
    ]

    left,right = st.columns(2)
    columns = [left,right]

    for i,col in enumerate(numeric_cols):
        info = schema[col]
        minimum = float(info.get("min",0.0))
        maximum = float(info.get("max",100.0))
        default = float(info.get("default",0.0))


        # Streamlit requires a valid range and the default must be inside it.
        if minimum > maximum:
            minimum,maximum = maximum,minimum
        if minimum==maximum:
            user_data[col]=columns[i%2].number_input(
                col,value=minimum,key=f"num_{col}"
            )
        else:
            default = min(max(default,minimum),maximum)
            user_data[col] = columns[i % 2].number_input(
                col,
                min_value=minimum,
                max_value=maximum,
                value=default,
                key=f"num_{col}",
            )

    for i, col in enumerate(categorical_cols):
        info = schema[col]
        choices = [str(value) for value in info.get("choices", [])]
        default = str(info.get("default", choices[0] if choices else "Unknown"))

        if not choices:
            choices = [default]
        if default not in choices:
            choices.insert(0, default)

        user_data[col] = columns[i % 2].selectbox(
            col,
            options=choices,
            index=choices.index(default),
            key=f"cat_{col}",
        )

    submitted = st.form_submit_button("Predict outcomes", type="primary")

if submitted:
    input_df = pd.DataFrame([user_data])

    # Use the same feature names and order as the saved schema.
    input_df = input_df[list(schema.keys())]

    try:
        completion_prediction = classifier.predict(input_df)[0]
        score_prediction = float(regressor.predict(input_df)[0])

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.subheader("Course completion")
            if hasattr(classifier, "predict_proba"):
                probabilities = classifier.predict_proba(input_df)[0]
                classes = classifier.classes_
                positive_index = list(classes).index(1) if 1 in classes else None
                if positive_index is not None:
                    probability = float(probabilities[positive_index])
                    st.metric("Completion probability", f"{probability:.1%}")
            if completion_prediction == 1:
                st.success("Prediction: Course completed")
            else:
                st.warning("Prediction: Course not completed")

        with result_col2:
            st.subheader("Final score")
            score_prediction = max(0.0, min(100.0, score_prediction))
            st.metric("Predicted final score", f"{score_prediction:.2f} / 100")

        st.caption(
            "These are model estimates, not guarantees. Use them as decision-support "
            "information alongside educator judgment."
        )

    except Exception as exc:
        st.error(
            "Prediction failed. Check that the schema columns match the features "
            "used when the models were trained and exported."
        )
        st.exception(exc)