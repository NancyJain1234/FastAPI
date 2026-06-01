from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    age = Column(Integer)
    married = Column(Boolean , default= False)
    email = Column(String, unique=True , index=True)
    phone_number = Column(String)
    allergies = Column(String)
    weight = Column(Float)
    height = Column(Float)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    username = Column(String, index = True)
    hashed_password = Column(String) 