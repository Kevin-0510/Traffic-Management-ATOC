import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    j0_traffic = (
        traci.edge.getLastStepVehicleNumber("-E1")
        + traci.edge.getLastStepVehicleNumber("-E2")
    )

    j1_traffic = (
        traci.edge.getLastStepVehicleNumber("-E3")
        + traci.edge.getLastStepVehicleNumber("-E4")
    )

    # -------------------------------
    # J0 Adaptive Control
    # -------------------------------
    if j0_traffic > 5 and traci.trafficlight.getPhase("J0") == 0:

        remaining = (
            traci.trafficlight.getNextSwitch("J0")
            - traci.simulation.getTime()
        )

        if remaining < 5:

            traci.trafficlight.setPhaseDuration("J0", 20)

            # Propagation Logic
            if j1_traffic < 5:

                traci.trafficlight.setPhaseDuration("J1", 20)

                print(
                    "Propagation Agent: "
                    "J0 congestion detected -> preparing J1"
                )

    # -------------------------------
    # J1 Adaptive Control
    # -------------------------------
    if j1_traffic > 5 and traci.trafficlight.getPhase("J1") == 0:

        remaining = (
            traci.trafficlight.getNextSwitch("J1")
            - traci.simulation.getTime()
        )

        if remaining < 5:
            traci.trafficlight.setPhaseDuration("J1", 20)

    print(
        f"J0={j0_traffic}  J1={j1_traffic}"
    )

traci.close()