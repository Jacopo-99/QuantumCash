from pydantic import BaseModel
from typing import List

class AWPInput(BaseModel):
    awp_id: str
    cassetto_precedente: float
    cassetto_attuale: float
    refill_precedente: float
    refill_attuale: float

class StoricoAWP(BaseModel):
    awp_id: str
    ultimo_cassetto: float
    ultimo_refill: float
    
class PrelievoInput(BaseModel):
    locale_id: str
    collector_id: str
    awps: List[AWPInput]
    storico: List[StoricoAWP]  # 👈 nuovo
    anticipo: float = 0
    contante_dichiarato: float

