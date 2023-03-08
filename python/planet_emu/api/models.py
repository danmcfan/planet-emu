from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, JSON, Enum
from sqlalchemy.orm import relationship

from planet_emu.api.database import Base
from planet_emu.api.schemas import Status


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

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    status = Column(Enum(Status), default=Status.PENDING)
    result = Column(JSON, nullable=True)
