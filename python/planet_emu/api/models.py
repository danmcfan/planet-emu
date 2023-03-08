from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship

from planet_emu.api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    point = Column(Geometry("POINT"), index=True)
    status = Column(String, index=True)
    result = Column(JSON, index=True)
