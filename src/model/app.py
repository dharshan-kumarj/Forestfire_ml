from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load the saved model and scaler at startup
model = None
scaler = None

@app.on_event("startup")
async def load_model():
    global model, scaler
    model_path = 'finalmodeloutput.pkl'
    scaler_path = 'scaler.pkl'
    
    # Load model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

# Input data structure (with 3 features)
class FirePredictionInput(BaseModel):
    Oxygen: float
    Temperature: float
    Humidity: float

# Predict endpoint
@app.post("/predict")
async def predict_fire_occurrence(input_data: FirePredictionInput):
    try:
        # Convert input data into a numpy array
        input_dict = input_data.dict()
        input_features = np.array(list(input_dict.values())).reshape(1, -1)

        # Scale the input features
        scaled_features = scaler.transform(input_features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Return the result
        result = "Fire" if prediction[0] == 1 else "No Fire"
        return {"prediction": result}
    
    except Exception as e:
        return {"error": str(e)}
