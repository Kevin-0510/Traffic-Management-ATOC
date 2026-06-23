import traci
import csv
import os

# =====================================
# START SUMO
# =====================================

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/double_junction.sumocfg"
]

traci.start(sumoCmd)

# Ensure telemetry data directory exists
os.makedirs("../data", exist_ok=True)

# =====================================
# VEHICLE POSITION FILE
# =====================================

vehicle_csv = "../data/double_vehicle_positions.csv"

# =====================================
# TRAFFIC CSV
# =====================================

with open("../data/live_traffic.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "time",
        "j0_queue",
        "j1_queue",
        "total_vehicles",
        "congestion_level",
        "agent_action"
    ])

    step_counter = 0

    # =====================================
    # MAIN LOOP
    # =====================================

    while traci.simulation.getMinExpectedNumber() > 0:

        traci.simulationStep()
        step_counter += 1

        # Capture view for the Desktop UI twin layout every 5 steps
        if step_counter % 5 == 0:
            try:
                traci.gui.screenshot("View #0", "../data/live_viewport.png")
            except:
                pass

        # =====================================
        # VEHICLE POSITION LOGGER
        # =====================================

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

        current_time = traci.simulation.getTime()

        j0_queue = (
            traci.edge.getLastStepVehicleNumber("-E1")
            +
            traci.edge.getLastStepVehicleNumber("-E2")
        )

        j1_queue = (
            traci.edge.getLastStepVehicleNumber("-E3")
            +
            traci.edge.getLastStepVehicleNumber("-E4")
        )

        total = j0_queue + j1_queue

        # =====================================
        # CONGESTION LEVEL
        # =====================================

        if total < 5:
            congestion = "LOW"

        elif total < 10:
            congestion = "MEDIUM"

        else:
            congestion = "HIGH"

        action = "MONITORING"

        # =====================================
        # J0 ADAPTIVE AGENT
        # =====================================

        if j0_queue > 5:

            action = "EXTEND_J0_GREEN"

            try:
                traci.trafficlight.setPhaseDuration(
                    "J0",
                    15
                )
            except:
                pass

        # =====================================
        # J1 ADAPTIVE AGENT
        # =====================================

        elif j1_queue > 5:

            action = "EXTEND_J1_GREEN"

            try:
                traci.trafficlight.setPhaseDuration(
                    "J1",
                    15
                )
            except:
                pass

        # =====================================
        # PROPAGATION AGENT
        # =====================================

        if j0_queue > 8 and j1_queue < 4:

            action = "PROPAGATE_J0_TO_J1"

            try:
                traci.trafficlight.setPhaseDuration(
                    "J1",
                    15
                )
            except:
                pass

        # =====================================
        # SAVE CSV
        # =====================================

        writer.writerow([
            current_time,
            j0_queue,
            j1_queue,
            total,
            congestion,
            action
        ])

        file.flush()

        # =====================================
        # TERMINAL OUTPUT
        # =====================================

        print(
            f"[{current_time}] "
            f"J0={j0_queue} "
            f"J1={j1_queue} "
            f"Action={action} "
            f"Congestion={congestion}"
        )

traci.close()