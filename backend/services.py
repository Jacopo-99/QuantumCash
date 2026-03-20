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

    prelievo_netto = prelievo_lordo - refill_da_pagare

    # validazione anticipo
    if data.anticipo > prelievo_netto:
        return {
            "error": "Anticipo superiore al prelievo netto"
        }

    return {
        "prelievo_lordo": prelievo_lordo,
        "refill_da_pagare": refill_da_pagare,
        "prelievo_netto": prelievo_netto,
        "anticipo": data.anticipo,
        "da_versare": prelievo_netto - data.anticipo
    }