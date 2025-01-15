from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler

app = FastAPI()

# Загрузка обученной модели
model = xgb.XGBRegressor()
model.load_model('model.json')

# Загрузка параметров нормализации
scaler = joblib.load('scalerДля 4х столбиков.pkl')
target_scaler = joblib.load('scalerДля Trip_duration.pkl')

class TripDurationRequest(BaseModel):
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float

class TripDurationResponse(BaseModel):
    duration: float

@app.post("/predict_trip_duration", response_model=TripDurationResponse)
async def predict_trip_duration(request: Request, data: TripDurationRequest):
    # Создание DataFrame для ввода
    input_data = pd.DataFrame({
        'pickup_longitude': [data.pickup_longitude],
        'pickup_latitude': [data.pickup_latitude],
        'dropoff_longitude': [data.dropoff_longitude],
        'dropoff_latitude': [data.dropoff_latitude]
    })

    # Нормализация данных
    input_data_scaled = scaler.transform(input_data)

    # Предсказание
    prediction_scaled = model.predict(input_data_scaled)

    # Обратное преобразование нормализованных данных в исходные
    prediction_original = target_scaler.inverse_transform(prediction_scaled.reshape(-1, 1))[0][0]

    return TripDurationResponse(duration=prediction_original)