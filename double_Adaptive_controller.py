import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    # Traffic near J0
    j0_traffic = (
        traci.edge.getLastStepVehicleNumber("-E1")
        + traci.edge.getLastStepVehicleNumber("-E2")
    )

    # Traffic near J1
    j1_traffic = (
        traci.edge.getLastStepVehicleNumber("-E3")
        + traci.edge.getLastStepVehicleNumber("-E4")
    )

    j0_phase = traci.trafficlight.getPhase("J0")
    j1_phase = traci.trafficlight.getPhase("J1")

    if j0_traffic > 5 and j0_phase == 0:
        traci.trafficlight.setPhaseDuration("J0", 20)

    if j1_traffic > 5 and j1_phase == 0:
        traci.trafficlight.setPhaseDuration("J1", 20)

    print(
        f"J0={j0_traffic} | J1={j1_traffic}"
    )

traci.close()