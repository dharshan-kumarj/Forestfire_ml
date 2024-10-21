import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

def load_data(file_path):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Handle missing values by forward filling
    df.fillna(method='ffill', inplace=True)

    # Check for duplicate rows and remove them
    df.drop_duplicates(inplace=True)

    # Rename the target column for consistency
    df.rename(columns={'Fire Occurrence': 'Fire_Occurrence'}, inplace=True)
    
    # Encode categorical variables using one-hot encoding
    df = pd.get_dummies(df, columns=['Area'], drop_first=True)

    # Separate features and target variable
    X = df.drop(columns=['Fire_Occurrence'])
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

    # Create a Decision Tree Classifier
    model = DecisionTreeClassifier(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", accuracy)

    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()
