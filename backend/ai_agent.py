def analizza_prelievo(result):
    analisi = []

    # sicurezza
    if "mismatch" not in result:
        return ["⚠️ Dati insufficienti per analisi"]

    if abs(result["mismatch"]) > 2:
        analisi.append("⚠️ Mismatch significativo")

    if result["ammanco"] > 0:
        analisi.append(f"💸 Ammanco: {result['ammanco']}€")

    if result["refill_pagato"] == 0 and result["refill_richiesto"] > 0:
        analisi.append("🚫 Refill bloccato")

    if result["fondo_usato"] > 0:
        analisi.append(f"🏦 Fondo usato: {result['fondo_usato']}€")

    if result["differenza_banca"] > 0:
        analisi.append(f"🏦 Da versare: {result['differenza_banca']}€")

    if not analisi:
        analisi.append("✅ Tutto regolare")

    return analisi