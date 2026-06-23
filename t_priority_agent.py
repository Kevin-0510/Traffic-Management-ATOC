import traci
import time

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/t_intersection.sumocfg"
]

traci.start(sumoCmd)

for step in range(300):

    traci.simulationStep()

    left = traci.edge.getLastStepVehicleNumber("-E1")
    right = traci.edge.getLastStepVehicleNumber("-E2")
    top = traci.edge.getLastStepVehicleNumber("-E0")

    print("\n===================")
    print(f"STEP {step}")
    print("===================")

    print(f"Left  : {left}")
    print(f"Right : {right}")
    print(f"Top   : {top}")

    current_phase = traci.trafficlight.getPhase("J0")

    if left > right and left > top:

        if current_phase != 0:
            traci.trafficlight.setPhase("J0", 0)

        print("PRIORITY -> LEFT ROAD")

    elif right > left and right > top:

        if current_phase != 0:
            traci.trafficlight.setPhase("J0", 0)

        print("PRIORITY -> RIGHT ROAD")

    else:

        if current_phase != 2:
            traci.trafficlight.setPhase("J0", 2)

        print("PRIORITY -> TOP ROAD")

    time.sleep(0.2)

traci.close()