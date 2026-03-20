# Modulo Prelievo AWP

## 🎯 Obiettivo

Gestire il prelievo delle AWP garantendo:

- correttezza dei calcoli

- coerenza con lo storico

- controllo degli errori operativi

- tracciabilità delle anomalie


# 🧠 CONCETTI BASE

## Prelievo lordo

Somma del delta cassetto di tutte le AWP coinvolte.

delta\_cassetto = cassetto\_attuale - cassetto\_precedente

prelievo\_lordo = somma(delta\_cassetto)


## Refill richiesto

Differenza tra refill attuale e refill precedente.

delta\_refill = refill\_attuale - refill\_precedente

refill\_richiesto = somma(delta\_refill)


## Prelievo netto

prelievo\_netto = prelievo\_lordo - refill\_pagato


## Da versare

da\_versare = prelievo\_netto - anticipo


# 📊 GESTIONE STORICO

Ogni AWP deve avere uno storico:

- ultimo\_cassetto

- ultimo\_refill

## Regole

- Il cassetto\_precedente deve essere uguale allo storico

- Il refill\_precedente deve essere uguale allo storico

## Se NON coincidono:

- generare alert

- il dato è considerato incoerente

## Se storico mancante:

- generare alert

- il prelievo non è affidabile


# 🔀 PRELIEVO PARZIALE

È possibile fare prelievi su solo alcune AWP del locale.

## Regole

- Le AWP non incluse NON vengono calcolate

- Se manca una AWP attesa → alert

- Il sistema NON assume mai che il prelievo sia completo


# 💥 MISMATCH (REGOLA CRITICA)

mismatch = contante\_dichiarato - prelievo\_lordo

## Regole

- Se |mismatch| \<= 2€: → tollerato

- Se |mismatch| \> 2€: → considerato errore grave → il refill NON può essere pagato correttamente


# 🚫 BLOCCO REFILL

Se mismatch \> 2€:

- refill\_pagato = 0

- generare alert: "Mismatch superiore a 2€, refill bloccato"


# 💰 FONDO ESATTORE

Caso: il contante disponibile non copre il refill

## Regola

Se: refill\_pagato \> contante\_dichiarato

allora:

fondo\_usato = refill\_pagato - contante\_dichiarato

## Azioni

- segnalare utilizzo fondo

- tracciare importo fondo usato


# 💸 ANTICIPO ESERCENTE

## Regola fondamentale

anticipo \<= prelievo\_netto

## Se violata:

- bloccare operazione

- restituire errore


# 🚨 SISTEMA ALERT

Gli alert devono segnalare:

- storico mancante

- incoerenza cassetto

- incoerenza refill

- mismatch \> 2€

- utilizzo fondo esattore

Gli alert NON bloccano sempre il flusso, ma devono essere visibili.


# 🧠 PRINCIPI FONDAMENTALI

## 1. Il sistema NON si fida dei dati

Tutto deve essere verificato:

- storico

- contante

- refill


## 2. Il dominio viene prima del codice

Le regole non possono essere semplificate per comodità tecnica.


## 3. I calcoli devono essere deterministici

Nessuna AI decide:

- soldi

- formule

- logiche economiche


## 4. Separazione tra richiesto e reale

Distinguere sempre:

- refill richiesto

- refill effettivamente pagato


## 5. Tracciabilità

Ogni anomalia deve:

- essere visibile

- essere salvata

- essere analizzabile


# 📌 STATO ATTUALE (v3)

Il sistema gestisce:

✔ prelievo lordo  
✔ refill richiesto  
✔ refill pagato  
✔ mismatch  
✔ fondo esattore  
✔ anticipo  
✔ storico  
✔ validazioni coerenza  
✔ alert operativi


# 🚧 PROSSIMI STEP (v4)

Da implementare:

- versamenti banca

- gestione ammanco

- recupero ammanco

- chiusura in ditta

- audit completo operazioni


# 🏦 VERSAMENTO BANCA

Il versamento in banca NON è parte del prelievo diretto.

## Regole

- Il versamento può avvenire:

  - lo stesso giorno

  - giorni successivi

- Il versamento NON modifica il prelievo

- Serve solo per tracciare dove finiscono i soldi

## Concetti

- da\_versare = soldi teorici

- versato\_banca = quanto effettivamente versato

## Differenza

differenza\_banca = da\_versare - versato\_banca


# 📉 AMMANCO

Caso: i soldi reali non tornano.

## Definizione

ammanco = quando: contante\_dichiarato \< prelievo\_lordo

## Regole

- anche 1€ è ammanco

- se \> 2€ → errore grave

- blocca refill (già gestito)

## Output

- deve essere tracciato

- non deve essere nascosto


# 🔁 RECUPERO AMMANCO

L'ammanco NON sparisce.

## Regole

- viene riportato nella cassa successiva

- può essere recuperato con:

  - incassi futuri

  - rettifiche

## Comportamento sistema

- memorizza ammanco

- lo propone come recupero futuro

- non lo annulla automaticamente


# 🧾 CHIUSURA IN DITTA

Il prelievo NON è chiuso finché non arriva in ditta.

## Stati

- APERTO → appena fatto

- IN\_ATTESA → non ancora chiuso

- CHIUSO → verificato in ditta

## Regole

- può essere chiuso anche con ammanco

- la chiusura conferma i dati finali

- dopo chiusura:

  - i dati NON devono cambiare


# 📊 STATO DEL PRELIEVO

Ogni prelievo deve avere uno stato:

- draft → appena creato

- validato → controlli ok

- chiuso → confermato in ditta


# 🧠 PRINCIPI AGGIUNTIVI

## 1. Separazione eventi

Il sistema deve separare:

- prelievo

- versamento banca

- chiusura


## 2. I soldi devono sempre "tornare"

Il sistema deve permettere di capire:

- dove sono i soldi

- cosa manca

- cosa è stato versato


## 3. Nessuna perdita silenziosa

Ogni differenza deve:

- essere visibile

- essere tracciata


# 📌 ESTENSIONE OUTPUT PRELIEVO

Il sistema deve ora restituire anche:

- ammanco

- stato prelievo

- versato\_banca (se presente)

- differenza\_banca

