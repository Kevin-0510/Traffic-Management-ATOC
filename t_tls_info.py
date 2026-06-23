import traci
import time

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/t_intersection.sumocfg"
]

traci.start(sumoCmd)

tls = "J0"

current_phase = 0
last_switch = 0

MIN_GREEN = 30

for step in range(500):

    traci.simulationStep()

    left = traci.edge.getLastStepVehicleNumber("-E1")
    right = traci.edge.getLastStepVehicleNumber("-E2")
    top = traci.edge.getLastStepVehicleNumber("-E0")

    horizontal = left + right
    vertical = top

    print("\n================")
    print(f"STEP {step}")
    print("================")

    print(f"Left       : {left}")
    print(f"Right      : {right}")
    print(f"Top        : {top}")

    print(f"Horizontal : {horizontal}")
    print(f"Vertical   : {vertical}")

    # Decide desired phase
    desired_phase = 0

    if vertical > horizontal:
        desired_phase = 2

    # Only change after minimum green time
    if step - last_switch >= MIN_GREEN:

        if desired_phase != current_phase:

            traci.trafficlight.setPhase(tls, desired_phase)

            current_phase = desired_phase
            last_switch = step

            print("PHASE CHANGED")

    if current_phase == 0:
        print("ACTION -> HORIZONTAL GREEN")
    else:
        print("ACTION -> VERTICAL GREEN")

    time.sleep(0.2)

traci.close()