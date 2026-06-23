import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

print("Traffic Lights:")
print(traci.trafficlight.getIDList())

traci.close()