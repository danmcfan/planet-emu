from planet_emu.api.database import Base
from sqlalchemy import JSON, Column, Float, String


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    features = Column(JSON)
    prediction = Column(Float)
