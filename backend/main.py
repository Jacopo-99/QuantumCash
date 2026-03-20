from fastapi import FastAPI
from backend.models import PrelievoInput
from backend.services import calcola_prelievo

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/prelievo")
def crea_prelievo(data: PrelievoInput):
    result = calcola_prelievo(data)
    return result