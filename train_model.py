import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Load dataset
data = pd.read_csv("college_data.csv")

# Create encoders
course_encoder = LabelEncoder()
location_encoder = LabelEncoder()
interest_encoder = LabelEncoder()
college_encoder = LabelEncoder()

# Encode categorical data
data["course_encoded"] = course_encoder.fit_transform(data["course"])
data["location_encoded"] = location_encoder.fit_transform(data["location"])
data["interest_encoded"] = interest_encoder.fit_transform(data["interest"])
data["college_encoded"] = college_encoder.fit_transform(data["college"])

# Features
X = data[
    [
        "min_percentage",
        "entrance_score",
        "fees",
        "course_encoded",
        "location_encoded",
        "interest_encoded"
    ]
]

# Target
y = data["college_encoded"]

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save model and encoders
joblib.dump(
    {
        "model": model,
        "course_encoder": course_encoder,
        "location_encoder": location_encoder,
        "interest_encoder": interest_encoder,
        "college_encoder": college_encoder,
        "data": data
    },
    "college_model.pkl"
)

print("================================")
print("Model trained successfully!")
print("college_model.pkl created!")
print("================================")