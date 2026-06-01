from fastapi import FastAPI, Path, HTTPException , Query
from fastapi.responses import JSONResponse
from typing import Annotated, List , Dict , Optional
import json
from pydantic import BaseModel, EmailStr , Field, computed_field, field_validator, model_validator       


app = FastAPI();

def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
        return data


def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)
        
@app.get("/")
def hello():
    return {'message' : 'hello world'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{id}')
def view_patient(
    id: int = Path(
        ...,
        description="ID of the patient in the DB",
        example=1
    ),
    sort: str = Query(
        "asc",
        description="Data in sorted order"
    )
):
    data = load_data()

    for patient in data:
        if patient['id'] == id:
            return patient
        
    raise HTTPException(status_code = 404, detail = 'Patient not found')
    ##return {'message': 'patient not found'}


class Address(BaseModel):
    street : str
    house_no : int
    state : str
    city : str

class Patient(BaseModel):
    id : int 
    name : str
    married: Annotated[bool , Field(default = None)]
    phone_number : Dict[str , str] = Field(max_length = 10 , title='mobile number' ,)
    allergies : Optional[List [str]] = None
    email : EmailStr
    address : Address
    weight : float = Field(gt = 0)
    height : float = Field(gt = 0)


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height ** 2) , 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    married: Optional[bool] = None
    phone_number: Optional[Dict[str, str]] = None
    allergies: Optional[List[str]] = None
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    

# def create_patients(patient : Patient):
#     print(patient.id)
#     print(patient.name) 
#     print(patient.phone_number)
#     print(patient.allergies)

# def update_patient_info(patient : Patient):
#     print(patient.id)
#     print(patient.name) 
#     print(patient.phone_number)
#     print(patient.allergies)
 
@model_validator(mode = 'after')
def validate_emergency_contact(model):
    if model.age > 60 and 'emergency' not in model.phone_number:
        raise ValueError('Patients older than 60 must have an emergency contact')
    return model

@field_validator('email')
@classmethod
def validate_mail(cls , email):
    front = email.split('@')[-1]
    domain = ['com' , 'in']
    if front not in domain:
        raise ValueError('not a valid email')
    return email


@field_validator('name', mode = 'after')
@classmethod
def modify_name(cls , name):
    return name.upper()

address_dict = {'city' : 'kota' , 
                'state' : 'Rajasthan' , 
                'house_no' : 110 , 
                'street' : 'rangpur road'}

patient_info = {'id' : 4 , 
                'name' : 'Ashish' , 
                'phone_number' : {
        'home': '1234567890',
        'office': '9876543210'
    },
    'allergies': ['Dust', 'Pollen'] , 
    'email' : 'hello@gmail.com',
    'address' : address_dict,
    'weight' : 70,
    'height' : 1.75
}


@app.post('/create')
def create_patient(patient : Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code = 400 , detail = 'Patient already exists')
    data.append(patient.model_dump(exclude = ['id']))
    save_data(data)
    return JSONResponse(status_code = 201 , content = {'message' : 'Patient created successfully!'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id : int,patient_update : PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code = 404 , detail = f'No Patient with {patient_id}')
    else:
        for patient in data:
            if patient["id"] == patient_id:
                update_data = patient_update.model_dump(
                    exclude_unset=True
                )
                for key, value in update_data.items():
                    patient[key] = value
                save_data(data)
                raise HTTPException(status_code = 202 , content = {'message' : 'Patient info updated successfully.'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:int):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code= 404 , content = {'message' : f'{patient_id }not in data'})   
    else:
        del data[patient_id]
        save_data(data)
        return JSONResponse(status_code = 202 , content = {'message' : 'patient record deleted'})
    

# patient1 = Patient(**patient_info)

# update_patient_info(patient1)
# print(patient1)
# temp = patient1.model_dump(include = ['name' , 'age', 'bmi' ,'verdict'] )
# print(temp)
# print(type(temp))









