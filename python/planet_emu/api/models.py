from sqlalchemy import JSON, Column, Enum, Float, String

from planet_emu.api.database import Base
from planet_emu.api.schemas import Status


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    status = Column(Enum(Status), default=Status.PENDING)
    result = Column(JSON, nullable=True)
