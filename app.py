from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib



# Load pipeline
pipeline = joblib.load("house_price_pipeline.joblib")

app = FastAPI(title="House Price Predictor API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow only your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class House(BaseModel):
    SquareFeet: float
    Bedrooms: int
    Bathrooms: int
    Neighborhood: str
    YearBuilt: int

@app.post("/predict")
def predict_house_price(house: House):
    df = pd.DataFrame([house.dict()])
    df["HouseAge"] = 2025 - df["YearBuilt"]
    df["BathPerBed"] = df["Bathrooms"] / df["Bedrooms"]
    predicted_price = pipeline.predict(df)[0]
    return {"predicted_price": float(predicted_price)}
