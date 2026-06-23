import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    r"E:\Downloads\Agentic Traffic management\sumo\network\cross.sumocfg"
]

traci.start(sumoCmd)

for step in range(100):

    traci.simulationStep()

    print("\n----- STEP", step, "-----")

    for edge in ['-E1', 'E1', 'E2', 'E3', 'E4']:

        count = traci.edge.getLastStepVehicleNumber(edge)

        print(edge, ":", count)

traci.close()