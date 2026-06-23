#WE ARE GOING TO PREDICT THE FUTURE CONGESTION SO WE CAN CONTROL THE TRAFFIC SIGNAL ACCORDINGLY
import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
]

traci.start(sumoCmd)

# Store previous vehicle counts
previous_north = 0
previous_west = 0

for step in range(3600):

    traci.simulationStep()

    if step % 20 == 0:

        north = traci.edge.getLastStepVehicleNumber("E1")
        west = traci.edge.getLastStepVehicleNumber("E2")

        # Simple trend forecasting
        future_north = max(0, north + (north - previous_north))
        future_west = max(0, west + (west - previous_west))

        print("\n========================")
        print("STEP:", step)
        print("========================")

        print("Current North:", north)
        print("Current West :", west)

        print("Predicted North:", future_north)
        print("Predicted West :", future_west)

        # Save values for next prediction
        previous_north = north
        previous_west = west

traci.close()