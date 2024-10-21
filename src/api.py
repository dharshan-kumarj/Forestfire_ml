from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()
router = APIRouter()  # Create a router

# Load the model and scaler from the specified paths
model_path = os.path.join(os.path.dirname(__file__), 'Finalmodel', 'finalmodeloutput.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'Finalmodel', 'scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Define the input features according to your dataset
class InputFeatures(BaseModel):
    feature1: float  # Replace with actual feature name
    feature2: float  # Replace with actual feature name
    feature3: float  # Replace with actual feature name
    feature4: float  # Add as needed
    feature5: float  # Add as needed
    feature6: float  # Add as needed
    feature7: float  # Add as needed
    feature8: float  # Add as needed
    feature9: float  # Add as needed
    feature10: float  # Add as needed
    feature11: float  # Add as needed
    feature12: float  # Add as needed
    feature13: float  # Add as needed
    feature14: float  # Add as needed
    feature15: float  # Add as needed
    feature16: float  # Add as needed
    feature17: float  # Add as needed
    feature18: float  # Add as needed

@router.post("/predict_fire/")
async def predict_fire(features: InputFeatures):
    # Create input array from features
    input_array = np.array([[features.feature1, features.feature2, features.feature3,
                             features.feature4, features.feature5, features.feature6,
                             features.feature7, features.feature8, features.feature9,
                             features.feature10, features.feature11, features.feature12,
                             features.feature13, features.feature14, features.feature15,
                             features.feature16, features.feature17, features.feature18]])
    
    # Scale the input features
    input_scaled = scaler.transform(input_array)

    # Make prediction
    prediction = model.predict(input_scaled)

    return {"prediction": int(prediction[0])}  # Return the prediction as an integer

# Include the router in the app
app.include_router(router)

# To run the FastAPI application, use the command:
# uvicorn api:app --reload
