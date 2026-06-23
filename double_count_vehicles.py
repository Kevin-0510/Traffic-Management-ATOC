import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

for step in range(100):

    traci.simulationStep()

    j0_count = (
        traci.edge.getLastStepVehicleNumber("E0")
        + traci.edge.getLastStepVehicleNumber("-E0")
        + traci.edge.getLastStepVehicleNumber("E1")
        + traci.edge.getLastStepVehicleNumber("-E1")
    )

    j1_count = (
        traci.edge.getLastStepVehicleNumber("E2")
        + traci.edge.getLastStepVehicleNumber("-E2")
        + traci.edge.getLastStepVehicleNumber("E3")
        + traci.edge.getLastStepVehicleNumber("-E3")
    )

    print(f"Step {step}")
    print(f"J0 Vehicles = {j0_count}")
    print(f"J1 Vehicles = {j1_count}")
    print("----------------")

traci.close()