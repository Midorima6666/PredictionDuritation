# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# import threading
# import subprocess
# import os

# app = FastAPI()

# @app.get("/")
# async def read_root():
#     return HTMLResponse("""
#     <html>
#         <head>
#             <title>Streamlit App</title>
#         </head>
#         <body>
#             <h1>Streamlit App</h1>
#             <iframe src="/streamlit" width="100%" height="800px"></iframe>
#         </body>
#     </html>
#     """)

# @app.get("/streamlit")
# async def streamlit_app():
#     # Запуск Streamlit приложения в отдельном потоке
#     port = os.getenv('PORT', 8501)
#     threading.Thread(target=lambda: subprocess.run(["streamlit", "run", "app.py", "--server.port", str(port)])).start()
#     return HTMLResponse(f"Streamlit app is running on port {port}...")
#     # subprocess.Popen(["streamlit", "run", "app.py"])
#     # return HTMLResponse("Streamlit app is running...")

# #uvicorn main:app --reload 
from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

app = FastAPI()
class InputData(BaseModel):
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float

with open('model.pkl', 'rb') as f:
    saved_objects = pickle.load(f)

loaded_feature_engineering = saved_objects["pipeline"]
loaded_model = saved_objects["model"]
@app.post('/predict')
async def predict(input_data: InputData):
    X_new = np.array([[
        input_data.pickup_longitude,
        input_data.pickup_latitude,
        input_data.dropoff_longitude,
        input_data.dropoff_latitude,
    ]])
    X_new_transformed = loaded_feature_engineering.transform(X_new)
    prediction = loaded_model.predict(X_new_transformed)
    return {"prediction": float(prediction[0])}
