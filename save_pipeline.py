import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib

# Load data
df = pd.read_csv("housing.csv")

# Feature engineering
df["HouseAge"] = 2025 - df["YearBuilt"]
df["BathPerBed"] = df["Bathrooms"] / df["Bedrooms"]

# Features & target
X = df[["SquareFeet", "Bedrooms", "Bathrooms", "Neighborhood", "HouseAge", "BathPerBed"]]
y = df["Price"]

# Preprocessing
numeric_features = ["SquareFeet", "Bedrooms", "Bathrooms", "HouseAge", "BathPerBed"]
numeric_transformer = SimpleImputer(strategy="median")

categorical_features = ["Neighborhood"]
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=500,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    ))
])

# Train
pipeline.fit(X, y)

# Save pipeline
joblib.dump(pipeline, "house_price_pipeline.joblib")
print("✅ Pipeline saved successfully!")
