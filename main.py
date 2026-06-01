from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from database import Base, engine, get_db
from models import PatientDB, UserDB
from schemas import PatientCreate, PatientUpdate, PatientResponse, UserCreate, UserResponse, Token

app = FastAPI(title="Patient Management API")

Base.metadata.create_all(bind=engine)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes= ['bcrypt'], deprecated = "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm= ALGORITHM)

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm= [ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail = "user not found")
    
    return user

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/view", response_model=List[PatientResponse])
def view_all_patients(db: Session = Depends(get_db)):
    return db.query(PatientDB).all()

@app.get("/")
def home():
    return {"message": "FastAPI Patient API with SQLite"}

@app.post("/patients", response_model= PatientResponse, status_code = 201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db),current_user: UserDB = Depends(get_current_user)):
    existing = db.query(PatientDB).filter(PatientDB.email == patient.email).first()

    if existing:
        raise HTTPException(status_code = 400, detail = "Email already exists")
    
    new_patient = PatientDB(
        name=patient.name,
        age=patient.age,
        married=patient.married,
        email=patient.email,
        phone_number=patient.phone_number,
        allergies=patient.allergies,
        weight=patient.weight,
        height=patient.height
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id : int , db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code = 404 , detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}


@app.patch("/patients/{patient_id}" , response_model= PatientResponse)
def update_patient(patient_id : int ,patient_update :PatientUpdate , db: Session = Depends(get_db),current_user: UserDB = Depends(get_current_user)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code = 404 , detail = "Patient not found")
    
    update_data = patient_update.model_dump(exclude_unset = True)

    for key,value in update_data.items():
        setattr(patient , key , value)

    db.commit()
    db.refresh(patient)

    return patient


@app.get('/patients/{patient_id}', response_model=PatientResponse)
def get_patient(patient_id : int , db :Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code = 404 , detail = "Patient not found")
    
    return patient


@app.get("/patients", response_model=List[PatientResponse])
def get_patients(
    name: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("id"),
    db: Session = Depends(get_db)
):
    query = db.query(PatientDB)

    if name:
        query = query.filter(PatientDB.name.ilike(f"%{name}%"))

    if sort == "name":
        query = query.order_by(PatientDB.name)
    elif sort == "age":
        query = query.order_by(PatientDB.age)
    elif sort == "weight":
        query = query.order_by(PatientDB.weight)
    else:
        query = query.order_by(PatientDB.id)

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()

@app.post("/signup" , response_model= UserResponse , status_code=201)
def signup(user : UserCreate , db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing:
        raise HTTPException(status_code = 400 , detail = "Username already exists")
    
    new_user = UserDB(
        username = user.username,
        hashed_password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
