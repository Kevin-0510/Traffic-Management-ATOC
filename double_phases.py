import traci

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

for tls in traci.trafficlight.getIDList():
    print("\nTraffic Light:", tls)

    logic = traci.trafficlight.getAllProgramLogics(tls)

    for program in logic:
        for i, phase in enumerate(program.phases):
            print(i, phase.state)

traci.close()