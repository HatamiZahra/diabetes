import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List

model = joblib.load("../../models/diabetes_model.pkl")
app = FastAPI()


class Diabetes(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict_diabetes(age: float, sex: float, bmi: float,
                                     bp: float, s1: float, s2: float, s3:
                                     float, s4: float, s5: float, s6: float):
    print(age, sex, bmi, bp, s1, s2, s3, s4, s5, s6)
    model_input = np.array(
        [age, sex, bmi, bp, s1, s2, s3, s4, s5, s6]).reshape(1, -1)
    pro = model.predict(model_input)
  
    print(f"model input {model_input}")
    return pro[0]

@app.post("/predict_patients")
async def predict_diabetes(patients: List[Diabetes]):
    pro = {}
    for pno, patient in enumerate(patients):
        model_input = np.array([patient.age, patient.sex, patient.bmi, patient.bp, patient.s1, patient.s2, patient.s3, patient.s4, patient.s5, patient.s6]).reshape(1, -1)
        pro[str(pno)] = float(model.predict(model_input))
   
    print(pro)
    pro = json.dumps(pro, indent = 4) 
    print(f"model input {model_input}")
    return pro