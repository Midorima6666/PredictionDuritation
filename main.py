from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
import subprocess
import os

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
    # Запуск Streamlit приложения в отдельном потоке
    port = os.getenv('PORT', 8501)
    threading.Thread(target=lambda: subprocess.run(["streamlit", "run", "app.py", "--server.port", str(port)])).start()
    return HTMLResponse(f"Streamlit app is running on port {port}...")
    # subprocess.Popen(["streamlit", "run", "app.py"])
    # return HTMLResponse("Streamlit app is running...")

#uvicorn main:app --reload 

