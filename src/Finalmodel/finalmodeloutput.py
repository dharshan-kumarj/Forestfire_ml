# This file can be used for handling outputs from your model predictions
def save_prediction_result(result):
    with open('prediction_results.txt', 'a') as f:
        f.write(f"{result}\n")

# Example usage:
# save_prediction_result({"city": "SampleCity", "prediction": 1})
