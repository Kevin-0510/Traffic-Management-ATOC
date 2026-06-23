# check_edges.py

import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
]

traci.start(sumoCmd)

print(traci.edge.getIDList())

traci.close()