import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from patient_model.config.core import config


def validate_inputs(*, input_df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    #pre_processed = pre_pipeline_preparation(data_frame=input_df)
    validated_data = input_df[config.model_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    age:Optional[int]
    anaemia: Optional[int]
    creatinine_phosphokinase: Optional[int]
    diabetes: Optional[int]
    ejection_fraction: Optional[int]
    high_blood_pressure: Optional[int]
    platelets: Optional[int]
    serum_creatinine: Optional[int]
    serum_sodium: Optional[float]
    sex: Optional[int]
    smoking: Optional[int]
    time: Optional[int]
    DEATH_EVENT: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]