import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
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
    ("regressor", GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=5
))
])

# Train
pipeline.fit(X, y)

# Save pipeline
joblib.dump(pipeline, "house_price_pipeline.joblib")
print("Pipeline saved successfully!")
