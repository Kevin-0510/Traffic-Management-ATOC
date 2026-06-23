import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    # Vehicles approaching J0
    j0_traffic = (
        traci.edge.getLastStepVehicleNumber("-E1") +
        traci.edge.getLastStepVehicleNumber("-E2")
    )

    current_phase = traci.trafficlight.getPhase("J0")

    # If many vehicles waiting at J0
    if j0_traffic > 5:

        # Keep green longer when phase 0 is active
        if current_phase == 0:
            traci.trafficlight.setPhaseDuration("J0", 20)

    print(
        f"J0 Traffic = {j0_traffic}, "
        f"Current Phase = {current_phase}"
    )

traci.close()