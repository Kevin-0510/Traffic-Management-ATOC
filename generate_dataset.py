import traci
import csv

sumoCmd = [
    "sumo-gui",
    "-c",
    r"E:\Downloads\Agentic Traffic management\sumo\network\cross.sumocfg"
]

traci.start(sumoCmd)

with open("traffic_dataset.csv", "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "time",
        "north",
        "west",
        "east",
        "south",
        "total"
    ])

    for step in range(3600):

        traci.simulationStep()

        north = traci.edge.getLastStepVehicleNumber("E1")
        west  = traci.edge.getLastStepVehicleNumber("E2")
        east  = traci.edge.getLastStepVehicleNumber("E3")
        south = traci.edge.getLastStepVehicleNumber("E4")

        total = north + west + east + south

        writer.writerow([
            step,
            north,
            west,
            east,
            south,
            total
        ])

traci.close()

print("Dataset created successfully")