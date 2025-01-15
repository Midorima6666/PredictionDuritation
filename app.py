import streamlit as st
import joblib
import json
import folium
from streamlit_folium import folium_static
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import folium_static, st_folium

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 80%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .main .block-container div[data-testid="stHorizontalBlock"] {
        gap: 2rem;
    }
    .main .block-container div[data-testid="stVerticalBlock"] {
        gap: 2rem;
    }
    .stButton>button {
        background-color: #32CD32;
        color: white;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #008000;
    }
      .cat-image {
        position: relative;
        display: inline-block;
    }
    .cat-image img {
        width: 100px;
        height: 100px;
        transition: transform 0.3s ease;
    }
    .cat-image:hover img {
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)
model = xgb.XGBRegressor()
model.load_model('model.json')
# Заголовок с измененным цветом
st.markdown(
    """
    <h1 style='color: #008000; text-align: center;'>Предсказание длительности поездки</h1>
    """,
    unsafe_allow_html=True
)

scaler = joblib.load('scalerДля 4х столбиков.pkl')
scaler2 = joblib.load('scalerДля Trip_duration.pkl')


# Функция для предсказания длительности поездки
def predict_trip_duration(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude):
    input_data = pd.DataFrame({
        'pickup_longitude': [pickup_longitude],
        'pickup_latitude': [pickup_latitude],
        'dropoff_longitude': [dropoff_longitude],
        'dropoff_latitude': [dropoff_latitude],
    })

    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)
    new_prediction = scaler2.inverse_transform(prediction.reshape(-1, 1))
    new_prediction= new_prediction/60
    return new_prediction[0]


pickup_longitude = st.number_input('Долгота места посадки', value=-73.977386)  
pickup_latitude = st.number_input('Широта места посадки', value=40.752658)
dropoff_longitude = st.number_input('Долгота места высадки', value=-73.946955)
dropoff_latitude = st.number_input('Широта места высадки', value=40.784050)

st.markdown(
    """
    <div class="cat-image">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg" alt="Котик">
    </div>
    """,
    unsafe_allow_html=True
)
# Кнопочка
if st.button('Предсказать длительность поездки'):
    duration = predict_trip_duration(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)
    st.write(f'Длительность вашей поезки составит: {duration} минут')

    
    m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=12)


    # Добавление маркеров на карту
    folium.Marker([pickup_latitude, pickup_longitude], popup='Место посадки', icon=folium.Icon(color='green', icon='home')).add_to(m)
    folium.Marker([dropoff_latitude, dropoff_longitude], popup='Место высадки', icon=folium.Icon(color='red', icon='cloud')).add_to(m)
    
    folium_static(m)
    # streamlit run app.py запуск через терминал  

