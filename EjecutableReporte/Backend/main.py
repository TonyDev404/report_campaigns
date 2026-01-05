import os
import sys
import certifi
from dotenv import load_dotenv

def resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

load_dotenv(resource_path(".env"))

cert_path = certifi.where()
os.environ["SSL_CERT_FILE"] = cert_path
os.environ["REQUESTS_CA_BUNDLE"] = cert_path

import uvicorn
import webbrowser
import threading
import time
import multiprocessing
import requests

from app import app
from splash import show_splash

def server_is_running():
    try:
        r = requests.get(
            "http://127.0.0.1:8000/", 
            timeout=0.5, 
            headers={"Cache-Control": "no-cache"}
        )
        return r.status_code == 200
    except:
        return False


def start_server():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_config=None,
        access_log=True
    )


def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    multiprocessing.freeze_support()

    # 🔑 CLAVE: NO intentar levantar dos veces
    if server_is_running():
        webbrowser.open("http://127.0.0.1:8000")
    else:    
        threading.Thread(target=show_splash, daemon=True).start()
        threading.Thread(target=open_browser, daemon=True).start()
        start_server()
