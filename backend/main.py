from fastapi import FastAPI
from backend.models import PrelievoInput
from backend.services import calcola_prelievo

from backend.db import engine, SessionLocal
from backend.db_models import Base, PrelievoDB, StoricoAWPDB

# 🔧 crea tabelle DB
Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🟢 ROOT
@app.get("/")
def root():
    return {"status": "ok", "message": "AWP gestionale running"}


# 🚀 CREA PRELIEVO
@app.post("/prelievo")
def crea_prelievo(data: PrelievoInput):
    result = calcola_prelievo(data)

    # ❌ se errore logico blocca tutto
    if "error" in result:
        return result

    db = SessionLocal()

    # 💾 salva prelievo
    prelievo = PrelievoDB(
        locale_id=data.locale_id,
        collector_id=data.collector_id,
        prelievo_lordo=result["prelievo_lordo"],
        prelievo_netto=result["prelievo_netto"],
        da_versare=result["da_versare"],
        ammanco=result["ammanco"],
        stato=result["stato"],
        data="oggi"
    )

    db.add(prelievo)
    db.commit()

    # 📊 aggiorna storico AWP
    for awp in data.awps:
        storico = StoricoAWPDB(
            awp_id=awp.awp_id,
            ultimo_cassetto=awp.cassetto_attuale,
            ultimo_refill=awp.refill_attuale
        )
        db.add(storico)

    db.commit()
    db.close()

    return result


# 📊 GET TUTTI I PRELIEVI
@app.get("/prelievi")
def get_prelievi():
    db = SessionLocal()
    prelievi = db.query(PrelievoDB).all()
    db.close()
    return prelievi