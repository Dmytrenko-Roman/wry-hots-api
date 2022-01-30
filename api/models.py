from sqlalchemy import Column, String

from database import Base

class Hero(Base):
    __tablename__ = 'heroes'

    name = Column(String, primary_key=True)
    wry_name = Column(String)
    role = Column(String)
    description = Column(String)
