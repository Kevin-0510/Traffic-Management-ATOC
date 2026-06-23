import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

for edge in ["E0","E1","E2","E3","E4"]:
    print(edge)
    print(" From:", traci.edge.getFromJunction(edge))
    print(" To  :", traci.edge.getToJunction(edge))
    print()

traci.close()