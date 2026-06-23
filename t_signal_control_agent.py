import traci
import time

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/t_intersection.sumocfg"
]

traci.start(sumoCmd)

for step in range(200):

    traci.simulationStep()

    horizontal = (
        traci.edge.getLastStepVehicleNumber("-E1")
        +
        traci.edge.getLastStepVehicleNumber("-E2")
    )

    vertical = (
        traci.edge.getLastStepVehicleNumber("-E0")
    )

    print("\n================")
    print(f"STEP {step}")
    print("================")

    print(f"Horizontal = {horizontal}")
    print(f"Vertical   = {vertical}")

    # Get current signal phase
    current_phase = traci.trafficlight.getPhase("J0")

    # Decision logic
    if horizontal > vertical:

        if current_phase != 0:
            traci.trafficlight.setPhase("J0", 0)

        print("ACTION -> HORIZONTAL GREEN")

    else:

        if current_phase != 2:
            traci.trafficlight.setPhase("J0", 2)

        print("ACTION -> VERTICAL GREEN")

    time.sleep(0.2)

traci.close()