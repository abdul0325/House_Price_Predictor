import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor

# Load Dataset
df = pd.read_csv("housing.csv")

# feature engineering
df["HouseAge"] = 2025 - df["YearBuilt"]
df["BathPerBed"] = df["Bathrooms"] / df["Bedrooms"]
df["SqFtPerRoom"] = df["SquareFeet"] / (df["Bedrooms"] + df["Bathrooms"])

# remove outliers
q_low = df["Price"].quantile(0.01)
q_high = df["Price"].quantile(0.99)
df = df[(df["Price"] >= q_low) & (df["Price"] <= q_high)]

# transform price
df["LogPrice"] = np.log1p(df["Price"])

# Features & Target
features = ["SquareFeet", "Bedrooms", "Bathrooms", "Neighborhood", "HouseAge", "BathPerBed", "SqFtPerRoom"]
X = df[features]
y = df["LogPrice"]  # LOG TARGET

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# normalizing
numeric_features = ["SquareFeet", "Bedrooms", "Bathrooms", "HouseAge", "BathPerBed", "SqFtPerRoom"]
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_features = ["Neighborhood"]
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# model 
model = GradientBoostingRegressor()

param_grid = {
    "n_estimators": [300, 500],
    "learning_rate": [0.03, 0.05],
    "max_depth": [3, 5],
    "subsample": [0.8, 1.0]
}

grid = GridSearchCV(
    model,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", grid)
])

# TRAIN
pipeline.fit(X_train, y_train)

# EVALUATE
y_pred_log = pipeline.predict(X_test)
y_test_real = np.expm1(y_test)
y_pred_real = np.expm1(y_pred_log)

mae = mean_absolute_error(y_test_real, y_pred_real)
r2 = r2_score(y_test_real, y_pred_real)

print("\nHIGH ACCURACY PIPELINE TRAINED")
print("MAE:", int(mae))
print("R2:", round(r2, 3))
