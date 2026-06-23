import traci
import csv

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

with open("../data/double_metrics.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "time",
        "j0_queue",
        "j1_queue"
    ])

    while traci.simulation.getMinExpectedNumber() > 0:

        traci.simulationStep()

        j0_queue = (
            traci.edge.getLastStepVehicleNumber("-E1")
            + traci.edge.getLastStepVehicleNumber("-E2")
        )

        j1_queue = (
            traci.edge.getLastStepVehicleNumber("-E3")
            + traci.edge.getLastStepVehicleNumber("-E4")
        )

        writer.writerow([
            traci.simulation.getTime(),
            j0_queue,
            j1_queue
        ])

traci.close()