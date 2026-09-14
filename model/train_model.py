import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("data/training_dataset.csv")

# These are the columns the model will actually learn from
feature_columns = [
    "soil_moisture", "tilt_x", "vibration_count",
    "rainfall_24h", "rainfall_72h", "slope_angle", "ndvi"
]

X = df[feature_columns]
y = df["landslide_occurred"]

# Split: 80% to train on, 20% held back to test on unseen data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,      # number of decision trees in the forest
    max_depth=8,           # keeps trees simple - reduces overfitting on a small dataset
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate on the held-back test data
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification report:\n", classification_report(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# Show which features matter most - great for your report/viva
importances = pd.Series(model.feature_importances_, index=feature_columns)
print("\nFeature importance:\n", importances.sort_values(ascending=False))

# Save the trained model to a file so other scripts can use it
joblib.dump(model, "model/landslide_model.joblib")
print("\nModel saved to model/landslide_model.joblib")