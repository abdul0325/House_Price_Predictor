import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score

# ----------------------------
# STEP 1: Load Dataset
# ----------------------------
df = pd.read_csv("housing.csv")

# ----------------------------
# STEP 2: Feature Engineering
# ----------------------------
df["HouseAge"] = 2025 - df["YearBuilt"]
df["BathPerBed"] = df["Bathrooms"] / df["Bedrooms"]

# ----------------------------
# STEP 3: Define Features & Target
# ----------------------------
features = ["SquareFeet", "Bedrooms", "Bathrooms", "Neighborhood", "HouseAge", "BathPerBed"]
target = "Price"

X = df[features]
y = df[target]

# ----------------------------
# STEP 4: Train-Test Split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------
# STEP 5: Preprocessing
# ----------------------------
numeric_features = ["SquareFeet", "Bedrooms", "Bathrooms", "HouseAge", "BathPerBed"]
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_features = ["Neighborhood"]
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# ----------------------------
# STEP 6: Build Pipeline with Random Forest
# ----------------------------
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(
        n_estimators=500,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    ))
])

# ----------------------------
# STEP 7: Train Model
# ----------------------------
pipeline.fit(X_train, y_train)

# ----------------------------
# STEP 8: Evaluate Model
# ----------------------------
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n✅ RANDOM FOREST PIPELINE TRAINED!")
print("📉 Mean Absolute Error:", int(mae))
print("📊 R2 Score:", round(r2, 3))

# ----------------------------
# STEP 9: Predict New House
# ----------------------------
new_house = pd.DataFrame([{
    "SquareFeet": 1800,
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Neighborhood": "Neighborhood1",  # replace with actual neighborhood
    "HouseAge": 10,
    "BathPerBed": 2/3
}])

predicted_price = pipeline.predict(new_house)
print("\n🏡 Predicted House Price:", int(predicted_price[0]))
