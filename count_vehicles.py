import traci
import os

sumoBinary = "sumo-gui"

sumoCmd = [
    sumoBinary,
    "-c",
    r"E:\Downloads\Agentic Traffic management\sumo\network\cross.sumocfg"
]

traci.start(sumoCmd)

step = 0

while step < 100:
    traci.simulationStep()

    vehicle_count = traci.vehicle.getIDCount()

    print(f"Step {step}: Vehicles = {vehicle_count}")

    step += 1

traci.close()