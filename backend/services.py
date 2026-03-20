def calcola_prelievo(data, db):
    # 1. Initialize totals
    totale_cassetto = 0
    totale_refill = 0
    alert = []

    # 2. Loop through machines to calculate the 'Lordo' (Gross)
    for awp in data.awps:
        # Note: 'db' needs to be passed to this function or handled via a dependency
        # For now, I'm assuming it's available or handled. 
        # If you get a 'db not defined' error, you'll need: def calcola_prelievo(data, db):
        storico = get_storico_db(db, awp.awp_id)

        if not storico:
            alert.append(f"Storico mancante {awp.awp_id}")
            continue

        # VALIDAZIONE COERENZA
        if awp.cassetto_precedente != storico.ultimo_cassetto:
            alert.append(f"Incoerenza cassetto {awp.awp_id}")

        if awp.refill_precedente != storico.ultimo_refill:
            alert.append(f"Incoerenza refill {awp.awp_id}")

        delta_cassetto = awp.cassetto_attuale - storico.ultimo_cassetto
        delta_refill = awp.refill_attuale - storico.ultimo_refill

        totale_cassetto += delta_cassetto
        totale_refill += delta_refill

    # 3. Define the missing variables based on your totals
    prelievo_lordo = totale_cassetto
    refill_richiesto = totale_refill

    # 4. AMMANCO / MISMATCH
    mismatch = data.contante_dichiarato - prelievo_lordo

    ammanco = 0
    if mismatch < 0:
        ammanco = abs(mismatch)

    refill_pagato = refill_richiesto

    if abs(mismatch) > 2:
        alert.append("Mismatch > 2€, refill bloccato")
        refill_pagato = 0

    # 5. FONDO
    fondo_usato = 0
    if refill_pagato > data.contante_dichiarato:
        fondo_usato = refill_pagato - data.contante_dichiarato
        alert.append("Uso fondo esattore")

    prelievo_netto = prelievo_lordo - refill_pagato

    # 6. Safety Check
    if data.anticipo > prelievo_netto:
        return {"error": "Anticipo superiore al prelievo netto"}

    da_versare = prelievo_netto - data.anticipo

    # 7. BANCA (placeholder)
    versato_banca = 0
    differenza_banca = da_versare - versato_banca

    return {
        "prelievo_lordo": prelievo_lordo,
        "refill_richiesto": refill_richiesto,
        "refill_pagato": refill_pagato,
        "prelievo_netto": prelievo_netto,
        "anticipo": data.anticipo,
        "da_versare": da_versare,
        "mismatch": mismatch,
        "ammanco": ammanco,
        "fondo_usato": fondo_usato,
        "versato_banca": versato_banca,
        "differenza_banca": differenza_banca,
        "stato": "draft",
        "alert": alert
    }

def trova_storico(awp_id, storico_list):
    for s in storico_list:
        if s.awp_id == awp_id:
            return s
    return None

def get_storico_db(db, awp_id):
    # Ensure StoricoAWPDB is imported here or at the top of the file
    from backend.db_models import StoricoAWPDB
    return db.query(StoricoAWPDB)\
        .filter(StoricoAWPDB.awp_id == awp_id)\
        .order_by(StoricoAWPDB.id.desc())\
        .first()