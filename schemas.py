from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Optional

class PatientCreate(BaseModel):
    name:str
    age:int
    married: Optional[bool] = False
    email : EmailStr
    phone_number : str
    allergies : Optional[str] = None
    weight: float = Field(gt=0)
    height:float = Field(gt = 0)

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        return "Obese"
    
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    married: Optional[bool] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    allergies: Optional[str] = None
    weight: Optional[float] = Field(default=None, gt=0)
    height: Optional[float] = Field(default=None, gt=0)

class PatientResponse(PatientCreate):
    id:int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username : str
    password : str


class UserResponse(BaseModel):
    id:int
    username:str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
