from sqlalchemy import Column, Integer, String, Float, JSON
from backend.db import Base

class PrelievoDB(Base):
    __tablename__ = "prelievi"

    id = Column(Integer, primary_key=True, index=True)
    locale_id = Column(String)
    collector_id = Column(String)
    prelievo_lordo = Column(Float)
    prelievo_netto = Column(Float)
    da_versare = Column(Float)
    ammanco = Column(Float)
    stato = Column(String)
    data = Column(String)

class StoricoAWPDB(Base):
    __tablename__ = "storico_awp"

    id = Column(Integer, primary_key=True, index=True)
    awp_id = Column(String)
    ultimo_cassetto = Column(Float)
    ultimo_refill = Column(Float)