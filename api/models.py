from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Hero(Base):
    __tablename__ = "heroes"

    name = Column(String, primary_key=True, nullable=False)
    wry_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='heroes')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    heroes = relationship('Hero', back_populates='creator')
