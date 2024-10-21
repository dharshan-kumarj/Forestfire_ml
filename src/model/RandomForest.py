import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_data(file_path):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Handle missing values by forward filling
    df.ffill(inplace=True)  # Updated to use ffill() method as per the warning

    # Check for duplicate rows and remove them
    df.drop_duplicates(inplace=True)

    # Rename the target column for consistency
    df.rename(columns={'Fire Occurrence': 'Fire_Occurrence'}, inplace=True)
    
    # Select the relevant features (use actual column names)
    selected_columns = ['Oxygen', 'Temperature', 'Humidity']
    X = df[selected_columns]  # Use only the selected features
    y = df['Fire_Occurrence']  # Target variable

    return X, y

def main():
    # Load and preprocess data
    df = load_data('Forest_fire.csv')  # Update with your CSV file path
    print("DataFrame:")
    print(df)

    # Check for first few rows
    print("\nFirst few rows:")
    print(df.head())

    # Check columns in the DataFrame
    print("\nColumns in the DataFrame:")
    print(df.columns)

    X, y = preprocess_data(df)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Create a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", accuracy)

    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model and scaler to files
    model_path = 'finalmodeloutput.pkl'
    scaler_path = 'scaler.pkl'
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

if __name__ == '__main__':
    main()
