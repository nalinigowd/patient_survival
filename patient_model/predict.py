import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Union
import pandas as pd
import numpy as np

from patient_model import __version__ as _version
from patient_model.config.core import config
from patient_model.pipeline import patient_pipe
from patient_model.processing.data_manager import load_pipeline
from patient_model.processing.validation import validate_inputs


pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
patient_pipe= load_pipeline(file_name=pipeline_file_name)


def make_prediction(*,input_data:Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model """

    validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    
    #validated_data=validated_data.reindex(columns=['Pclass','Sex','Age','Fare', 'Embarked','FamilySize','Has_cabin','Title'])
    validated_data=validated_data.reindex(columns=config.model_config.features)
    #print(validated_data)
    results = {"predictions": None, "version": _version, "errors": errors}
    
    predictions = patient_pipe.predict(validated_data)

    results = {"predictions": predictions,"version": _version, "errors": errors}
    print(results)
    if not errors:

        predictions = patient_pipe.predict(validated_data)
        if predictions[0] == 1:
            prediction = "Death Event"
        else:
            prediction = "No Death Event"
        #return prediction
    
        Descriptive_result = {"predictions": prediction,"version": _version, "errors": errors}
        print(Descriptive_result)

    return results

if __name__ == "__main__":

    data_in={'age':[45],'anaemia':[1],'creatinine_phosphokinase':[981],'diabetes':[0],
             'ejection_fraction':[30],'high_blood_pressure':[0],'platelets':[136000],
             'serum_creatinine':[1.1],'serum_sodium':[137],'sex':[1],'smoking':[0],'time':[11]}
    
    make_prediction(input_data=data_in)
