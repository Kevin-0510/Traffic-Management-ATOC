import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

for edge in traci.edge.getIDList():
    if edge.startswith(":"):
        continue

    print(f"\n{edge} connects to:")

    try:
        connections = traci.lane.getLinks(edge + "_0")

        for conn in connections:
            print("   ->", conn[0])
    except:
        pass

traci.close()