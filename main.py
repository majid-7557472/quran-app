from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI(title="Quran Recitation App")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

BASE_URL = "http://api.alquran.cloud/v1"
RECITER = "ar.alafasy"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    surahs = requests.get(f"{BASE_URL}/surah").json()["data"]
    return templates.TemplateResponse(request, "index.html", {"surahs": surahs})


@app.get("/surah/{surah_number}", response_class=HTMLResponse)
def get_surah(request: Request, surah_number: int):
    surahs = requests.get(f"{BASE_URL}/surah").json()["data"]
    surah_data = requests.get(f"{BASE_URL}/surah/{surah_number}/{RECITER}").json()["data"]
    return templates.TemplateResponse(request, "index.html", {
        "surahs": surahs,
        "selected_surah": surah_data,
        "ayahs": surah_data["ayahs"],
    })


@app.get("/api/surah/{surah_number}")
def api_get_surah(surah_number: int):
    return requests.get(f"{BASE_URL}/surah/{surah_number}/{RECITER}").json()
