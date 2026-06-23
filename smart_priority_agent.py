import joblib

model = joblib.load("congestion_model.pkl")

north = 2
west = 1
east = 0
south = 3

import pandas as pd

input_data = pd.DataFrame(
    [[north, west, east, south]],
    columns=["north", "west", "east", "south"]
)

predicted_congestion = model.predict(input_data)[0]

emission = predicted_congestion * 2

score = predicted_congestion + emission

if score > 10:
    print("\nACTION: PRIORITIZE THIS ROUTE")
else:
    print("\nACTION: NORMAL FLOW")

print("Predicted Congestion:", round(predicted_congestion,2))
print("Emission:", round(emission,2))
print("Priority Score:", round(score,2))