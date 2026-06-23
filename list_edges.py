import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    r"E:\Downloads\Agentic Traffic management\sumo\network\cross.sumocfg"
]

traci.start(sumoCmd)

print("Edges in the network:")
print(traci.edge.getIDList())

traci.close()