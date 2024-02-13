# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Read the cleaned dataset
cleaned_data = pd.read_csv('linkedin.csv')

# Select relevant features and target variable
features = [ 'Company', 'Location', 'Link']  
target = 'Industry'  # Assuming 'Industry' is the target variable to predict

# Encode categorical features
label_encoders = {}
for feature in features:
    label_encoders[feature] = LabelEncoder()
    cleaned_data[feature] = label_encoders[feature].fit_transform(cleaned_data[feature])

# Normalize numerical features
scaler = MinMaxScaler()
cleaned_data[features] = scaler.fit_transform(cleaned_data[features])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(cleaned_data[features], cleaned_data[target], test_size=0.2, random_state=42)

# Initialize and train the RandomForestClassifier model
model = RandomForestClassifier(n_estimators=100, random_state=100)
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Display classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Example of predicting the Industry
new_lead = {'Company': ['Deloitte Consulting'], 'Location': ['New York, New York'], 'Link': ['https://www.linkedin.com/company/deloitteconsulting/']}
new_lead_df = pd.DataFrame(new_lead)

# Encode categorical features and normalize numerical features for the new lead
for feature in features:
    new_lead_df[feature] = label_encoders[feature].transform(new_lead_df[feature])
new_lead_df[features] = scaler.transform(new_lead_df[features])

predicted_lead_class = model.predict(new_lead_df)
print("\nPredicted Industry for the New Lead:", predicted_lead_class)
