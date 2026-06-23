import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load dataset
data = pd.read_csv("E:/Downloads/Agentic Traffic management/sumo/datasets/traffic_dataset.csv")

# Features
X = data[["north", "west", "east", "south"]]

# Target
y = data["total"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Results")
print("----------------")
print("MAE:", mae)
print("R2 Score:", r2)

# Save model
joblib.dump(model, "congestion_model.pkl")

print("\nModel saved as congestion_model.pkl")