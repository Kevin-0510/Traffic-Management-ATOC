import joblib

# Load trained model
model = joblib.load("congestion_model.pkl")

# Example values
north = 1
west = 1
east = 2
south = 1

prediction = model.predict([[north, west, east, south]])

print("\nCongestion Prediction")
print("---------------------")
print("North:", north)
print("West :", west)
print("East :", east)
print("South:", south)
print("\nPredicted Total Congestion =", prediction[0])