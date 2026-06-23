import traci
import joblib
import pandas as pd
import csv
import os

# =====================================
# START SUMO
# =====================================

print("STEP 1")

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/cross.sumocfg"
]

print("STEP 2")

traci.start(sumoCmd)

print("STEP 3")

model = joblib.load("congestion_model.pkl")

# Ensure telemetry data directory exists
os.makedirs("../data", exist_ok=True)

# =====================================
# LOAD MODEL
# =====================================

model = joblib.load("congestion_model.pkl")
vehicle_csv = "../data/cross_vehicle_positions.csv"

# =====================================
# CREATE LIVE CSV
# =====================================
print ("STEP 4")
with open("../data/cross_live_traffic.csv", "w", newline="") as file:
    print ("STEP 5")

    writer = csv.writer(file)

    writer.writerow([
        "time",
        "north_vehicles",
        "west_vehicles",
        "north_congestion",
        "west_congestion",
        "north_emission",
        "west_emission",
        "north_score",
        "west_score",
        "agent_action",
        "congestion_level"
    ])
    print ("STEP 6")

    current_green = 0
    print ("STEP 7")

    # =====================================
    # SIMULATION LOOP
    # =====================================

    for step in range(3600):
        print ("LOOP", step)
        traci.simulationStep()
        
        # Capture view for the Desktop UI twin layout every 5 steps
        if step % 5 == 0:
            try:
                traci.gui.screenshot("View #0", "../data/live_viewport.png")
            except:
                pass
                
        print("AFTER SIM", step)
        
        # ==============================
        # VEHICLE POSITION LOGGER
        # ==============================

        with open(vehicle_csv, "w", newline="") as vehicle_file:

            vehicle_writer = csv.writer(vehicle_file)

            vehicle_writer.writerow([
                "vehicle_id",
                "x",
                "y",
                "speed"
            ])

            vehicles = traci.vehicle.getIDList()

            for vehicle in vehicles:

                x, y = traci.vehicle.getPosition(vehicle)

                speed = traci.vehicle.getSpeed(vehicle)

                vehicle_writer.writerow([
                    vehicle,
                    round(x, 2),
                    round(y, 2),
                    round(speed, 2)
                ])

            if step % 20 == 0:

                # ==============================
                # VEHICLE COUNTS
                # ==============================

                north = traci.edge.getLastStepVehicleNumber("E1")
                west = traci.edge.getLastStepVehicleNumber("E2")

                # ==============================
                # CONGESTION AGENT
                # ==============================

                north_input = pd.DataFrame(
                    [[north, 0, 0, 0]],
                    columns=[
                        "north",
                        "west",
                        "east",
                        "south"
                    ]
                )

                west_input = pd.DataFrame(
                    [[0, west, 0, 0]],
                    columns=[
                        "north",
                        "west",
                        "east",
                        "south"
                    ]
                )

                north_congestion = float(
                    model.predict(north_input)[0]
                )

                west_congestion = float(
                    model.predict(west_input)[0]
                )

                # ==============================
                # EMISSION AGENT
                # ==============================

                north_emission = north_congestion * 2
                west_emission = west_congestion * 2

                # ==============================
                # PRIORITY AGENT
                # ==============================

                north_score = (
                    north_congestion
                    +
                    north_emission
                )

                west_score = (
                    west_congestion
                    +
                    west_emission
                )

                # ==============================
                # SIGNAL CONTROL AGENT
                # ==============================

                action = "MONITORING"

                if north_score > west_score:

                    if current_green != 0:

                        traci.trafficlight.setPhase(
                            "J3",
                            0
                        )

                        current_green = 0

                    action = "NORTH_GREEN"

                elif west_score > north_score:

                    if current_green != 2:

                        traci.trafficlight.setPhase(
                            "J3",
                            2
                        )

                        current_green = 2

                    action = "WEST_GREEN"

                # ==============================
                # CONGESTION LEVEL
                # ==============================

                total = north + west

                if total < 5:
                    congestion = "LOW"

                elif total < 10:
                    congestion = "MEDIUM"

                else:
                    congestion = "HIGH"

                # ==============================
                # LOG CSV
                # ==============================

                writer.writerow([
                    step,
                    north,
                    west,
                    round(north_congestion, 2),
                    round(west_congestion, 2),
                    round(north_emission, 2),
                    round(west_emission, 2),
                    round(north_score, 2),
                    round(west_score, 2),
                    action,
                    congestion
                ])

                file.flush()

                # ==============================
                # TERMINAL REPORT
                # ==============================

                print(
                    f"[{step}] "
                    f"N={north} "
                    f"W={west} "
                    f"Action={action} "
                    f"Congestion={congestion}"
                )

traci.close()