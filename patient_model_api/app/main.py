import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import gradio

#from fastapi import FastAPI, Request, Response

import random
import numpy as np
import pandas as pd
from patient_model.processing.data_manager import load_dataset, load_pipeline
from patient_model import __version__ as _version
from patient_model.config.core import config
from sklearn.model_selection import train_test_split
from patient_model.predict import make_prediction

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


# FastAPI object
#app = FastAPI()

# Inputs from user
input_components = [
    gradio.Slider(label="Age", minimum=df1['age'].min(), maximum=df1['age'].max(), step=1),
    gradio.Radio(label="Anaemia", choices=["Yes", "No"]),
    gradio.Radio(label="High Blood Pressure", choices=["Yes", "No"]),
    gradio.Slider(label="Creatinine Phosphokinase", minimum=df1['creatinine_phosphokinase'].min(), maximum=df1['creatinine_phosphokinase'].max(), step=1),
    gradio.Radio(label="Diabetes", choices=["Yes", "No"]),
    gradio.Slider(label="Ejection Fraction", minimum=df1['ejection_fraction'].min(), maximum=df1['ejection_fraction'].max(), step=1),
    gradio.Slider(label="Platelets", minimum=df1['platelets'].min(), maximum=df1['platelets'].max(), step=1),
    gradio.Radio(label="Sex", choices=["Male", "Female"]),
    gradio.Slider(label="Serum Creatinine", minimum=df1['serum_creatinine'].min(), maximum=df1['serum_creatinine'].max(), step=0.1),
    gradio.Slider(label="Serum Sodium", minimum=df1['serum_sodium'].min(), maximum=df1['serum_sodium'].max(), step=1),
    gradio.Radio(label="Smoking", choices=["Yes", "No"]),
    gradio.Slider(label="Time", minimum=df1['time'].min(), maximum=df1['time'].max(), step=1),
]

# Output response
output_component = gradio.Label(label="Death Event Prediction")

def predict_death_event(age, anaemia, high_blood_pressure, creatinine_phosphokinase, diabetes, ejection_fraction, platelets, sex, serum_creatinine, serum_sodium, smoking, time): # YOUR CODE HERE for parameters

    # YOUR CODE HERE...
    # Convert categorical variables to numerical values
    anaemia = 1 if anaemia == "Yes" else 0
    high_blood_pressure = 1 if high_blood_pressure == "Yes" else 0
    diabetes = 1 if diabetes == "Yes" else 0
    smoking = 1 if smoking == "Yes" else 0
    sex = 1 if sex == "Male" else 0

    # Convert all inputs to the correct data types
    age = int(age)
    creatinine_phosphokinase = float(creatinine_phosphokinase)
    ejection_fraction = float(ejection_fraction)
    platelets = int(platelets)
    serum_creatinine = float(serum_creatinine)
    serum_sodium = float(serum_sodium)
    time = int(time)

    features = np.array([[age, anaemia, high_blood_pressure, creatinine_phosphokinase, diabetes, ejection_fraction, platelets, sex, serum_creatinine, serum_sodium, smoking, time]])

    #prediction = xgb_model.predict(features)
    result = make_prediction(input_data=input_df.replace({np.nan: None}))["predictions"]
    print(prediction[0])
    print(features)
    if prediction[0] == 1:
        prediction = "Death Event"
    else:
        prediction = "No Death Event"
    return prediction

   
    #result = make_prediction(input_data=input_df.replace({np.nan: None}))["predictions"]
    #label = "Survive" if result[0]==1 else "Not Survive"
    #return label

# Gradio interface to generate UI link
title = "Patient Survival Prediction"
description = "Predict survival of patient with heart failure, given their clinical record"

interface = gradio.Interface(fn = predict_death_event,
                         inputs = input_components,
                         outputs = output_component,
                         title = title,
                         description = description,
                         allow_flagging='never')

interface.launch(share = True, debug = True)  # server_name="0.0.0.0", server_port = 8001   # Ref: https://www.gradio.app/docs/interface


# Mount gradio interface object on FastAPI app at endpoint = '/'
#app = gradio.mount_gradio_app(app, iface, path="/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
