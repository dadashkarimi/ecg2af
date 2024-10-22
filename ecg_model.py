
import numpy as np
from tensorflow.keras.models import load_model
from ml4h.models.model_factory import get_custom_objects
from ml4h.tensormap.ukb.survival import mgb_afib_wrt_instance2
from ml4h.tensormap.ukb.demographics import age_2_wide, af_dummy, sex_dummy3

# Set up output tensormaps
output_tensormaps = {tm.output_name(): tm for tm in [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]}

# Custom objects needed for loading the model
custom_dict = get_custom_objects(list(output_tensormaps.values()))

# Load the model with custom objects
def load_ecg2af_model(model_path):
    return load_model(model_path, custom_objects=custom_dict)

def predict_af(ecg_file):
    model = load_ecg2af_model('./model_zoo/ECG2AF/ecg_5000_survival_curve_af_quadruple_task_mgh_v2021_05_21.h5')

    # Generate a random ECG array for now or replace it with actual data from the uploaded file
    ecg_tensor = np.random.random((1, 5000, 12))  # Replace this with actual ECG data

    # Get predictions from the model
    predictions = model(ecg_tensor)

    # Initialize all values
    af_risk = 0
    sex_pred_male = 0
    sex_pred_female = 0
    age_pred = 0
    af_read_no = 0
    af_read_yes = 0

    # Process and prepare the predictions
    for name, pred in zip(model.output_names, predictions):
        otm = output_tensormaps[name]
        if otm.is_survival_curve():
            intervals = otm.shape[-1] // 2
            predicted_survivals = np.cumprod(pred[:, :intervals], axis=1)
            af_risk = float(1 - predicted_survivals[0, -1])  # Convert tensor to float
        elif 'sex' in name:
            sex_pred_male = float(pred[0][0])  # Convert tensor to float
            sex_pred_female = float(pred[0][1])  # Convert tensor to float
        elif 'age' in name:
            age_pred = float(pred[0][0])  # Convert tensor to float
        elif 'af_in_read' in name:
            af_read_no = float(pred[0][0])  # Convert tensor to float
            af_read_yes = float(pred[0][1])  # Convert tensor to float

    return {
        'af_risk': af_risk,
        'sex_pred_male': sex_pred_male,
        'sex_pred_female': sex_pred_female,
        'age_pred': age_pred,
        'af_read_no': af_read_no,
        'af_read_yes': af_read_yes
    }

