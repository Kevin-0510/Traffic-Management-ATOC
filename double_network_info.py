import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

print("Edges:")
for edge in traci.edge.getIDList():
    print(edge)

print("\nJunctions:")
for j in traci.junction.getIDList():
    print(j)

traci.close()