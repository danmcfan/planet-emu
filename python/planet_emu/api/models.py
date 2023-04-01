from planet_emu.api.database import Base
from sqlalchemy import JSON, Column, Float, Integer, String


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    year = Column(Integer)
    properties = Column(JSON)
