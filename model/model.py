import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Function to read CSV file and load data into a DataFrame
def load_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Display the DataFrame and first few rows
    print("DataFrame:")
    print(df)
    print("\nFirst few rows:")
    print(df.head())
    
    # Print the columns of the DataFrame
    print("\nColumns in the DataFrame:")
    print(df.columns.tolist())

    return df

# Function to preprocess the data
def preprocess_data(df):
    # Fill missing values if any
    df.fillna(method='ffill', inplace=True)  # Forward fill to handle missing values

    # Features and target variable
    X = df[['Oxygen', 'Temperature', 'Humidity']]  # Features
    
    # Make sure to update the column name to match the correct one found
    y = df['Fire Occurrence']  # Target variable

    return X, y

# Function to train a logistic regression model
def train_model(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return model, accuracy, report

# Main function to execute the workflow
def main():
    # Specify the file path for your CSV file
    file_path = 'Forest_fire.csv'  # Adjust the path as needed

    # Load the data
    df = load_data(file_path)

    # Preprocess the data
    X, y = preprocess_data(df)

    # Train the model and evaluate it
    model, accuracy, report = train_model(X, y)

    # Output the results
    print("\nModel Accuracy:", accuracy)
    print("\nClassification Report:\n", report)

# Entry point of the script
if __name__ == "__main__":
    main()
