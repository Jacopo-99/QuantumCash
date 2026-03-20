def calcola_prelievo(data):
    totale_cassetto = 0
    totale_refill = 0

    for awp in data.awps:
        delta_cassetto = awp.cassetto_attuale - awp.cassetto_precedente
        delta_refill = awp.refill_attuale - awp.refill_precedente

        totale_cassetto += delta_cassetto
        totale_refill += delta_refill

    prelievo_lordo = totale_cassetto
    refill_da_pagare = totale_refill

    # 💥 MISMATCH
    mismatch = data.contante_dichiarato - prelievo_lordo

    alert = []
    refill_pagabile = refill_da_pagare

    # 🚨 REGOLA CRITICA
    if abs(mismatch) > 2:
        alert.append("Mismatch superiore a 2€, refill NON pagabile correttamente")
        refill_pagabile = 0

    # 💰 FONDO ESATTORE
    fondo_usato = 0

    if refill_pagabile > data.contante_dichiarato:
        fondo_usato = refill_pagabile - data.contante_dichiarato
        alert.append("Utilizzato fondo esattore")

    prelievo_netto = prelievo_lordo - refill_pagabile

    # 🚫 VALIDAZIONE ANTICIPO
    if data.anticipo > prelievo_netto:
        return {
            "error": "Anticipo superiore al prelievo netto"
        }

    da_versare = prelievo_netto - data.anticipo

    return {
        "prelievo_lordo": prelievo_lordo,
        "refill_richiesto": refill_da_pagare,
        "refill_pagato": refill_pagabile,
        "prelievo_netto": prelievo_netto,
        "anticipo": data.anticipo,
        "da_versare": da_versare,
        "mismatch": mismatch,
        "fondo_usato": fondo_usato,
        "alert": alert
    }