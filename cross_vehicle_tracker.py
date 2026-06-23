import traci
import csv

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
]

traci.start(sumoCmd)

with open("../data/cross_vehicle_positions.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "vehicle_id",
        "x",
        "y",
        "speed"
    ])

    while traci.simulation.getMinExpectedNumber() > 0:

        traci.simulationStep()

        vehicles = traci.vehicle.getIDList()

        file.seek(0)
        file.truncate()

        writer = csv.writer(file)

        writer.writerow([
            "vehicle_id",
            "x",
            "y",
            "speed"
        ])

        for vehicle in vehicles:

            x, y = traci.vehicle.getPosition(vehicle)

            speed = traci.vehicle.getSpeed(vehicle)

            writer.writerow([
                vehicle,
                round(x, 2),
                round(y, 2),
                round(speed, 2)
            ])

        file.flush()

traci.close()