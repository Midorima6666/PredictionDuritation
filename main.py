from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

@app.get("/")
async def read_root():
    return HTMLResponse("""
    <html>
        <head>
            <title>Streamlit App</title>
        </head>
        <body>
            <h1>Streamlit App</h1>
            <iframe src="/streamlit" width="100%" height="800px"></iframe>
        </body>
    </html>
    """)

@app.get("/streamlit")
async def streamlit_app():
    # Запуск Streamlit приложения
    subprocess.Popen(["streamlit", "run", "app.py"])
    return HTMLResponse("Streamlit app is running...")

#uvicorn main:app --reload
