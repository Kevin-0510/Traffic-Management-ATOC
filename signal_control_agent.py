import traci
import joblib
import pandas as pd

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
]

traci.start(sumoCmd)

# Load trained congestion model
model = joblib.load("congestion_model.pkl")

current_green = 0   # 0 = North Green, 2 = West Green

for step in range(3600):

    traci.simulationStep()

    # Make decision every 20 simulation steps
    if step % 20 == 0:

        north = traci.edge.getLastStepVehicleNumber("E1")
        west = traci.edge.getLastStepVehicleNumber("E2")

        # ==================================
        # CONGESTION AGENT
        # ==================================

        north_input = pd.DataFrame(
            [[north, 0, 0, 0]],
            columns=["north", "west", "east", "south"]
        )

        west_input = pd.DataFrame(
            [[0, west, 0, 0]],
            columns=["north", "west", "east", "south"]
        )

        north_congestion = model.predict(north_input)[0]
        west_congestion = model.predict(west_input)[0]

        # ==================================
        # EMISSION AGENT
        # ==================================

        north_emission = north_congestion * 2
        west_emission = west_congestion * 2

        # ==================================
        # PRIORITY AGENT
        # ==================================

        north_score = north_congestion + north_emission
        west_score = west_congestion + west_emission

        # ==================================
        # DECISION REPORT
        # ==================================

        print("\n====================================")
        print("STEP:", step)
        print("====================================")

        print(
            "Vehicles ->",
            f"North:{north}",
            f"West:{west}"
        )

        print(
            "Congestion ->",
            f"North:{round(north_congestion,2)}",
            f"West:{round(west_congestion,2)}"
        )

        print(
            "Emission ->",
            f"North:{round(north_emission,2)}",
            f"West:{round(west_emission,2)}"
        )

        print(
            "Priority Score ->",
            f"North:{round(north_score,2)}",
            f"West:{round(west_score,2)}"
        )

        # ==================================
        # SIGNAL CONTROL AGENT
        # ==================================

        if north_score > west_score:

            if current_green != 0:
                traci.trafficlight.setPhase("J3", 0)
                current_green = 0

            print("\nACTION: NORTH GREEN")

        elif west_score > north_score:

            if current_green != 2:
                traci.trafficlight.setPhase("J3", 2)
                current_green = 2

            print("\nACTION: WEST GREEN")

        else:

            print("\nACTION: KEEP CURRENT PHASE")

        print(
            "Current Signal State:",
            traci.trafficlight.getRedYellowGreenState("J3")
        )

traci.close()