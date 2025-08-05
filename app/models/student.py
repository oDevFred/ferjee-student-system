from sqlalchemy import Column, Integer, String
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rg = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)