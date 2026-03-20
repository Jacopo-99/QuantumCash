def calcola_prelievo(data):
    totale_cassetto = 0
    totale_refill = 0
    alert = []

    for awp in data.awps:
        storico = trova_storico(awp.awp_id, data.storico)

        if not storico:
            alert.append(f"Storico mancante {awp.awp_id}")
            continue

        if awp.cassetto_precedente != storico.ultimo_cassetto:
            alert.append(f"Incoerenza cassetto {awp.awp_id}")

        if awp.refill_precedente != storico.ultimo_refill:
            alert.append(f"Incoerenza refill {awp.awp_id}")

        delta_cassetto = awp.cassetto_attuale - awp.cassetto_precedente
        delta_refill = awp.refill_attuale - awp.refill_precedente

        totale_cassetto += delta_cassetto
        totale_refill += delta_refill

    prelievo_lordo = totale_cassetto
    refill_richiesto = totale_refill

    # 📉 AMMANCO / MISMATCH
    mismatch = data.contante_dichiarato - prelievo_lordo

    ammanco = 0
    if mismatch < 0:
        ammanco = abs(mismatch)

    refill_pagato = refill_richiesto

    if abs(mismatch) > 2:
        alert.append("Mismatch > 2€, refill bloccato")
        refill_pagato = 0

    # 💰 FONDO
    fondo_usato = 0
    if refill_pagato > data.contante_dichiarato:
        fondo_usato = refill_pagato - data.contante_dichiarato
        alert.append("Uso fondo esattore")

    prelievo_netto = prelievo_lordo - refill_pagato

    if data.anticipo > prelievo_netto:
        return {"error": "Anticipo superiore al prelievo netto"}

    da_versare = prelievo_netto - data.anticipo

    # 🏦 BANCA (placeholder per ora)
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