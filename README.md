<!-- Animated header -->
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=Smart%20Outcome%20Predictor&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Predict%20Course%20Completion%20and%20Final%20Score%20with%20Machine%20Learning&descAlignY=58&descSize=18" width="100%" alt="Smart Outcome Predictor banner"/>

<!-- Typing animation -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=800&color=7C3AED&center=true&vCenter=true&width=700&lines=%F0%9F%8E%93+Predict+whether+a+student+completes+the+course;%F0%9F%93%8A+Estimate+the+final+score+out+of+100;%E2%9A%A1+Powered+by+XGBoost+%2B+Streamlit;%F0%9F%A4%96+Decision+support+for+educators" alt="Typing animation"/>
</a>

<br/>

<!-- Badges -->
<img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/XGBoost-Model-189AB4?style=for-the-badge" alt="XGBoost"/>
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
<img src="https://img.shields.io/badge/pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas"/>

<br/><br/>

<!-- Link buttons -->
<a href="https://smart-outcome-predictor-mp2ss4dhafg96wgybmzxag.streamlit.app/">
  <img src="https://img.shields.io/badge/%F0%9F%9A%80%20Live%20App-Open%20in%20Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live App"/>
</a>
<a href="https://github.com/mahesh-aiml/Smart-Outcome-Predictor/tree/main">
  <img src="https://img.shields.io/badge/View%20Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="View Repository"/>
</a>
<a href="https://github.com/mahesh-aiml/Smart-Outcome-Predictor/blob/main/app.py">
  <img src="https://img.shields.io/badge/Open%20app.py-7C3AED?style=for-the-badge&logo=python&logoColor=white" alt="Open app.py"/>
</a>

</div>

---

## ✨ Overview

**Smart Outcome Predictor** ek interactive web app hai jo student aur course ki details leke do cheezein predict karta hai:

| 🎯 Task | 🧠 Type | 📤 Output |
|---|---|---|
| **Course Completion** | Classification | Completed / Not completed + probability (%) |
| **Final Score** | Regression | Predicted score (0 – 100) |

Dono models **XGBoost** se train kiye gaye hain aur `joblib` (`.pkl`) files ke roop me save hain. UI **Streamlit** me bani hai.

---

## 🎬 Features

- 🧾 **Dynamic form** – input fields `outputs/input_schema.json` se auto-generate hoti hain
- 🔢 **Smart limits** – numeric fields training-data ke min/max range me rehti hain
- 🏷️ **Categorical dropdowns** – sirf wahi values jo training me use hui
- 📈 **Completion probability** – sirf yes/no nahi, confidence bhi
- 🛟 **Self-healing** – agar `xgboost` missing ho to app khud install kar leta hai, aur schema missing ho to built-in default se rebuild kar leta hai
- ⚡ **Fast** – models aur schema `st.cache_resource` / `st.cache_data` se cache hote hain

---

## 🧩 Input Features

<details>
<summary><b>👤 Student & Course details (click to expand)</b></summary>

<br/>

**Numeric**

| Feature | Min | Max | Default |
|---|---|---|---|
| `age` | 16 | 45 | 24 |
| `week_of_year` | 1 | 52 | 27 |
| `sessions` | 1 | 94 | 17 |
| `time_spent_hours` | 0.6 | 76.8 | 16.1 |
| `videos_watched` | 0 | 158 | 23 |
| `quiz_attempts` | 0 | 20 | 7 |
| `assignments_submitted` | 0 | 12 | 4 |
| `forum_posts` | 0 | 8 | 1 |
| `avg_quiz_score` | 0 | 100 | 66.8 |
| `attendance_rate` | 0.404 | 1.0 | 0.855 |
| `couse_durection_day` | 0 | 364 | 180 |

**Categorical**

| Feature | Choices |
|---|---|
| `country_region` | Africa, Americas, Asia, Europe, Oceania |
| `device_type` | Laptop, Mobile, Tablet |
| `education_background` | Graduate, HighSchool, Undergrad, WorkingPro |
| `course_level` | Advanced, Beginner, Intermediate |
| `course_category` | Business, Data, Design, Marketing, Programming |

</details>

---

## 🚀 Quick Start

### 1️⃣ Clone the repository

```bash
git clone https://github.com/mahesh-aiml/Smart-Outcome-Predictor.git
cd Smart-Outcome-Predictor
```

### 2️⃣ (Optional) Virtual environment banao

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Dependencies install karo

```bash
pip install -r requirements.txt
```

### 4️⃣ App run karo

```bash
streamlit run app.py
```

App browser me `http://localhost:8501` par khul jayegi. 🎉

> 🌐 Live demo: [Smart Outcome Predictor · Streamlit](https://smart-outcome-predictor-mp2ss4dhafg96wgybmzxag.streamlit.app/)
>
> 📄 Source code: [`app.py`](https://github.com/mahesh-aiml/Smart-Outcome-Predictor/blob/main/app.py)

---

## 📁 Project Structure

```text
Smart-Outcome-Predictor/
├── app.py                              # Streamlit application
├── requirements.txt                    # Python dependencies
├── .gitignore
├── model/
│   ├── best_classifiction_model.pkl    # Course completion model
│   └── best_regression_model.pkl       # Final score model
└── outputs/
    └── input_schema.json               # Feature names, types, ranges, choices
```

---

## 🔄 How It Works

```mermaid
flowchart LR
    A[👤 User fills form] --> B[📋 Schema validates ranges & choices]
    B --> C[🧮 DataFrame in training column order]
    C --> D[🌲 XGBoost Classifier]
    C --> E[📈 XGBoost Regressor]
    D --> F[✅ Completed? + Probability]
    E --> G[🎯 Final Score 0-100]
```

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,pandas,numpy,sklearn,git,github,vscode&theme=dark" alt="Tech stack icons"/>

</div>

`Streamlit` · `XGBoost` · `scikit-learn` · `pandas` · `NumPy` · `joblib` · `matplotlib` · `seaborn` · `openpyxl`

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---|---|
| `Model file not found` | Project zip ko dobara extract karo taaki `model/` folder aaye |
| `xgboost` import error | `python -m pip install xgboost` chalao aur app restart karo |
| `Prediction failed` | Check karo ki `input_schema.json` ke columns training ke features se match karte hain |

---

## 📌 Disclaimer

> These are **model estimates, not guarantees**. Predictions ko educator ke judgment ke saath **decision-support** ki tarah use karo.

---

<div align="center">

### 💜 Mahesh Lohar

⭐ **Agar project pasand aaya to repo ko star zaroor karo!** ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%" alt="footer"/>

</div>
