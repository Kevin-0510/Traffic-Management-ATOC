import pandas as pd
import joblib

model = joblib.load("congestion_model.pkl")

# North route traffic
north_input = pd.DataFrame(
    [[4, 0, 0, 0]],
    columns=["north", "west", "east", "south"]
)

north_congestion = model.predict(north_input)[0]
north_emission = north_congestion * 2
north_score = north_congestion + north_emission

# South route traffic
south_input = pd.DataFrame(
    [[0, 0, 0, 3]],
    columns=["north", "west", "east", "south"]
)

south_congestion = model.predict(south_input)[0]
south_emission = south_congestion * 2
south_score = south_congestion + south_emission

print("North Score =", round(north_score, 2))
print("South Score =", round(south_score, 2))

if north_score > south_score:
    print("\nPRIORITIZE NORTH → EAST")
else:
    print("\nPRIORITIZE SOUTH → EAST")