import traci
import pandas as pd
import joblib

# Load trained model
model = joblib.load("congestion_model.pkl")

# Start SUMO
traci.start([
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
])

for step in range(3600):

    traci.simulationStep()

    # Vehicle counts from each direction
    north = traci.edge.getLastStepVehicleNumber("-E1")
    west  = traci.edge.getLastStepVehicleNumber("E2")
    east  = traci.edge.getLastStepVehicleNumber("E3")
    south = traci.edge.getLastStepVehicleNumber("E4")

    input_data = pd.DataFrame(
        [[north, west, east, south]],
        columns=["north", "west", "east", "south"]
    )

    predicted_congestion = model.predict(input_data)[0]

    emission = predicted_congestion * 2
    score = predicted_congestion + emission

    print("\nSTEP:", step)
    print("North:", north)
    print("West :", west)
    print("East :", east)
    print("South:", south)

    print("Predicted Congestion:",
          round(predicted_congestion, 2))

    print("Priority Score:",
          round(score, 2))

    if score > 10:
        print("ACTION: PRIORITIZE ROUTE")
    else:
        print("ACTION: NORMAL FLOW")

traci.close()