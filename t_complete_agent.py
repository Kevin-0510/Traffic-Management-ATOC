import traci
import csv
import os

# =====================================
# START SUMO
# =====================================

sumoCmd = [
    "sumo-gui",
    "-c",
    "../network/t_intersection.sumocfg"
]

traci.start(sumoCmd)

# Ensure telemetry data directory exists
os.makedirs("../data", exist_ok=True)

# =====================================
# VEHICLE POSITION FILE
# =====================================

vehicle_csv = "../data/t_vehicle_positions.csv"

# =====================================
# TRAFFIC CSV
# =====================================

with open("../data/t_live_traffic.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "time",
        "left_vehicles",
        "right_vehicles",
        "top_vehicles",
        "horizontal_vehicles",
        "vertical_vehicles",
        "total_vehicles",
        "priority_direction",
        "agent_action",
        "congestion_level"
    ])

    # =====================================
    # MAIN LOOP
    # =====================================

    for step in range(1000):

        traci.simulationStep()

        # Capture view for the Desktop UI twin layout every 5 steps
        if step % 5 == 0:
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

        # =====================================
        # VEHICLE COUNTS
        # =====================================

        left = traci.edge.getLastStepVehicleNumber("-E1")
        right = traci.edge.getLastStepVehicleNumber("-E2")
        top = traci.edge.getLastStepVehicleNumber("-E0")

        horizontal = left + right
        vertical = top

        total = left + right + top

        # =====================================
        # PRIORITY AGENT
        # =====================================

        priority = "TOP"

        if left > right and left > top:
            priority = "LEFT"

        elif right > left and right > top:
            priority = "RIGHT"

        # =====================================
        # SIGNAL CONTROL AGENT
        # =====================================

        current_phase = traci.trafficlight.getPhase("J0")

        action = "MONITORING"

        if horizontal > vertical:

            if current_phase != 0:
                traci.trafficlight.setPhase("J0", 0)

            action = "HORIZONTAL_GREEN"

        else:

            if current_phase != 2:
                traci.trafficlight.setPhase("J0", 2)

            action = "VERTICAL_GREEN"

        # =====================================
        # CONGESTION AGENT
        # =====================================

        if total < 5:
            congestion = "LOW"

        elif total < 10:
            congestion = "MEDIUM"

        else:
            congestion = "HIGH"

        # =====================================
        # SAVE CSV
        # =====================================

        writer.writerow([
            step,
            left,
            right,
            top,
            horizontal,
            vertical,
            total,
            priority,
            action,
            congestion
        ])

        file.flush()

        # =====================================
        # TERMINAL OUTPUT
        # =====================================

        print(
            f"[{step}] "
            f"L={left} "
            f"R={right} "
            f"T={top} "
            f"Priority={priority} "
            f"Action={action} "
            f"Congestion={congestion}"
        )

traci.close()