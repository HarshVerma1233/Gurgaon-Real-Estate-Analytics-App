


https://github.com/user-attachments/assets/a341be06-b9d1-4df1-bc22-4c33bbc5dda8




# 🏢 Gurgaon Real Estate Analytics & Price Predictor

A comprehensive, end-to-end Machine Learning and Data Analytics web application built with **Streamlit**. This app provides data-driven insights into the Gurgaon real estate market and includes a predictive engine to estimate property prices based on key housing attributes.

---

## 🚀 Key Features

### 1. 📈 Interactive Analytics Dashboard (`analysis.py`)
* Fully interactive charts visualizing real estate distribution, price variations across sectors, and feature distributions.
* Powered by **Pandas**, **Plotly**, **Seaborn**, and **Matplotlib** to parse and plot trends dynamically from clean property data.

### 2. 🔮 Intelligent Price Predictor (`price_predictor.py`)
* Predicts property valuations (in Crores) using an advanced Machine Learning pipeline.
* Takes multiple user inputs: *Property Type, Sector, Bedrooms, Bathrooms, Balconies, Property Age, Built-up Area, Servant Room, Store Room, Furnishing Status, Luxury Rating, and Floor Level*.
* Outputs a calculated target price range based on the model's structural margin of error.

---

## 🛠️ Machine Learning Pipeline Details

The underlying predictive engine is built on **Scikit-Learn (v1.6.1)** and trained using the following architecture:

* **Target Variable Transformation:** Applied a Logarithmic Transformation (`np.log1p`) on the property prices to normalize skewed distributions and improve regression convergence.
* **Feature Engineering & Preprocessing (`ColumnTransformer`):**
  * **Numerical Columns:** Scaled via `StandardScaler()` (`property_type`, `bedRoom`, `bathroom`, `built_up_area`, `servant room`, `store room`).
  * **Categorical Columns:** Encoded via `OneHotEncoder(drop='first')` (`sector`, `balcony`, `agePossession`, `furnishing_type`, `Floor_level`).
  * **Pass-through Features:** Kept intact (`luxury_score`).
* **Model Baseline Exploration:** Explored multiple regression strategies including **Linear Regression** (R² ~ 0.85) and optimized **Support Vector Regression (SVR)** with an RBF kernel (R² ~ 0.88, reducing Mean Absolute Error significantly).

---

## 📂 Project Structure

Code output

File written successfully.

```text
gurgaon-real-estate-analytics-app/
│
├── app.py                  # Main entry point for the Streamlit multi-page application
├── requirements.txt        # Exact python environment dependency constraints
├── README.md               # Project documentation and deployment guide
│
├── pages/
│   ├── price_predictor.py  # User input form and picklen-pipeline prediction engine
│   ├── analysis.py         # Visual analytics dashboard and plotting code
│   ├── pipeline.pkl        # Serialized Scikit-Learn ML preprocessing & model pipeline
│   └── df.pkl              # Pickled structural DataFrame map for drop-down uniqueness
│
└── notebooks/
    └── baseline_model.ipynb # Jupyter Notebook containing model exploration, training, and evaluations
