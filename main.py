from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI(title="Quran Recitation App")

# static files (CSS) serve karne ke liye
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates ke liye
templates = Jinja2Templates(directory="templates")

BASE_URL = "http://api.alquran.cloud/v1"
RECITER = "ar.alafasy"  # Sheikh Mishary Alafasy ki recitation (aap koi bhi reciter edition daal sakte hain)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Home page: saari 114 Surahon ki list dikhata hai (dropdown ke liye)
    """
    response = requests.get(f"{BASE_URL}/surah")
    data = response.json()
    surahs = data["data"]  # list of all surahs with number, name, englishName

    return templates.TemplateResponse(
        request,
        "index.html",
        {"surahs": surahs, "selected_surah": None, "ayahs": None}
    )


@app.get("/surah/{surah_number}", response_class=HTMLResponse)
def get_surah(request: Request, surah_number: int):
    """
    Jab user koi surah select kare to us surah ki tamam ayaten
    audio ke saath nikal kar dikhata hai
    """
    # Surah list dobara load (dropdown ke liye)
    surah_list_response = requests.get(f"{BASE_URL}/surah")
    surahs = surah_list_response.json()["data"]

    # Is surah ki ayaten + audio (reciter edition ke sath)
    surah_response = requests.get(f"{BASE_URL}/surah/{surah_number}/{RECITER}")
    surah_data = surah_response.json()["data"]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "surahs": surahs,
            "selected_surah": surah_data,
            "ayahs": surah_data["ayahs"],
        }
    )


@app.get("/api/surah/{surah_number}")
def api_get_surah(surah_number: int):
    """
    Pure JSON API endpoint (agar aap ne JS se fetch karna ho to)
    """
    response = requests.get(f"{BASE_URL}/surah/{surah_number}/{RECITER}")
    return response.json()
