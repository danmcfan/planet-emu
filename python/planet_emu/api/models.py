from sqlalchemy import JSON, Column, Float, String, Integer

from planet_emu.api.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    year = Column(Integer)
    properties = Column(JSON)
