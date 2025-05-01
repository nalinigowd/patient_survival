import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from patient_model.config.core import config
from patient_model.processing.features import OutlierHandler

patient_pipe = Pipeline([
    
    ######## Handle outliers ########
    ('handle_outliers_creatinine', OutlierHandler(variable = config.model_config.creatinine_var)),
    ('handle_outliers_ejection', OutlierHandler(variable = config.model_config.ejection_var)),
    ('handle_outliers_platelets', OutlierHandler(variable = config.model_config.platelets_var)),
    ('handle_outliers_serum_creat', OutlierHandler(variable = config.model_config.serum_creat_var)),
    ('handle_outliers_serum_sod', OutlierHandler(variable = config.model_config.serum_sod_var)),

    # Scale features
    ('scaler', StandardScaler()),
    
    # ML model
    ('model_rf', RandomForestClassifier(n_estimators = config.model_config.n_estimators,
                                        max_depth = config.model_config.max_depth,
                                        max_leaf_nodes = config.model_config.max_leaves,
                                        random_state = config.model_config.random_state))
    
    ])