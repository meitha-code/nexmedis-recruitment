from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Izinkan frontend
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

FILE_PATH = "patients.json"

def load_patients():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []


def save_patients():
    with open(FILE_PATH, "w") as file:
        json.dump(patients_db, file, indent=4)

patients_db = load_patients()

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    diagnosis: str

@app.get("/", tags=["Root"])
def root():
    print("Root endpoint accessed")
    return {"message": "Root End"}

@app.post("/patients/")
async def add_patient(patient: Patient):
    patients_db.append(patient.model_dump())
    save_patients()
    return patient

@app.get("/patients/", response_model=List[Patient])
async def get_patients():
    return patients_db

@app.delete("/patients/{index}")
async def delete_patient(index: int):
    if index < 0 or index >= len(patients_db):
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patients_db.pop(index)  # Hapus pasien dari list
    save_patients()
    return {"message": "Patient deleted"}
