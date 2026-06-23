import customtkinter as ctk
import pandas as pd
from PIL import Image
import subprocess
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ATOCEnterpriseHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ATOC - Enterprise Intelligence Console")
        self.geometry("1600x900")
        self.configure(fg_color="#070A0F")
        
        self.scenarios = {
            "Double Junction": {"csv": "../data/live_traffic.csv", "script": "double_complete_agent.py", "pos": "../data/double_vehicle_positions.csv"},
            "Cross Junction": {"csv": "../data/cross_live_traffic.csv", "script": "cross_complete_agent.py", "pos": "../data/cross_vehicle_positions.csv"},
            "T Junction": {"csv": "../data/t_live_traffic.csv", "script": "t_complete_agent.py", "pos": "../data/t_vehicle_positions.csv"}
        }
        self.active_scenario = "Double Junction"
        self.viewport_path = "../data/live_viewport.png"
        
        self.last_step_count = -1
        self.current_display_mode = "viewport"

        # Sidebar Framework
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#0A0E17", border_width=1, border_color="#1E293B")
        self.sidebar.pack(side="left", fill="y")
        self.build_sidebar_controls()
        
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        self.build_workspace()
        self.init_charts()
        
        self.update_telemetry_loop()

    def build_sidebar_controls(self):
        title = ctk.CTkLabel(self.sidebar, text="🚦 ATOC MATRIX", font=ctk.CTkFont(family="JetBrains Mono", size=20, weight="bold"), text_color="#38BDF8")
        title.pack(pady=(25, 5), padx=20, anchor="w")
        
        caption = ctk.CTkLabel(self.sidebar, text="Enterprise Core Terminal", font=ctk.CTkFont(size=11), text_color="#64748B")
        caption.pack(pady=(0, 30), padx=20, anchor="w")
        
        lbl = ctk.CTkLabel(self.sidebar, text="TARGET NODE FOCUS", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl.pack(padx=20, anchor="w")
        
        self.selector = ctk.CTkOptionMenu(self.sidebar, values=list(self.scenarios.keys()), command=self.change_scenario, fg_color="#1E293B", button_color="#0F172A", text_color="#F8FAFC")
        self.selector.pack(padx=20, fill="x", pady=(5, 15))
        
        self.run_btn = ctk.CTkButton(self.sidebar, text="🚀 DEPLOY ACTIVE AGENT", command=self.launch_simulation_agent, font=ctk.CTkFont(weight="bold", size=13), fg_color="#059669", hover_color="#10B981")
        self.run_btn.pack(padx=20, fill="x", pady=10)
        
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="#0F172A", height=40, corner_radius=6)
        self.status_frame.pack(padx=20, fill="x", pady=20)
        self.status_lbl = ctk.CTkLabel(self.status_frame, text="🟢 ENGINE READY: IDLE", font=ctk.CTkFont(family="JetBrains Mono", size=11), text_color="#38BDF8")
        self.status_lbl.pack(pady=8, padx=10, anchor="center")

    def build_workspace(self):
        self.header_title = ctk.CTkLabel(self.main_content, text="Double Junction Control Node", font=ctk.CTkFont(size=24, weight="bold"), text_color="#F8FAFC")
        self.header_title.pack(anchor="w")
        
        self.workspace_layout = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.workspace_layout.pack(fill="both", expand=True, pady=10)
        
        # Left Deck (Graphs + Logs Panel)
        self.left_deck = ctk.CTkFrame(self.workspace_layout, fg_color="transparent")
        self.left_deck.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.kpi_frame = ctk.CTkFrame(self.left_deck, fg_color="#0A0E17", border_width=1, border_color="#1E293B", corner_radius=8)
        self.kpi_frame.pack(fill="x", pady=(0, 10), ipady=5)
        
        self.lbl_one_val = ctk.CTkLabel(self.kpi_frame, text="0 Active Units Tracked", font=ctk.CTkFont(size=20, weight="bold"), text_color="#10B981")
        self.lbl_one_val.pack(pady=(12, 2), padx=15, anchor="w")
        self.lbl_two_val = ctk.CTkLabel(self.kpi_frame, text="CRITERIA STATE: MONITORING", font=ctk.CTkFont(family="JetBrains Mono", size=11), text_color="#38BDF8")
        self.lbl_two_val.pack(pady=(0, 12), padx=15, anchor="w")

        self.chart_frame = ctk.CTkFrame(self.left_deck, fg_color="#0A0E17", border_width=1, border_color="#1E293B", corner_radius=8)
        self.chart_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Human-Eye Optimized Insights Terminal
        self.insights_frame = ctk.CTkFrame(self.left_deck, fg_color="#0A0E17", border_width=1, border_color="#1E293B", corner_radius=8, height=210)
        self.insights_frame.pack(fill="x")
        self.insights_frame.pack_propagate(False)
        
        self.insights_title = ctk.CTkLabel(self.insights_frame, text="🧠 HUMAN INSIGHTS TERMINAL", font=ctk.CTkFont(family="JetBrains Mono", size=11, weight="bold"), text_color="#A855F7")
        self.insights_title.pack(pady=(8, 4), padx=15, anchor="w")
        
        self.insights_box = ctk.CTkTextbox(self.insights_frame, fg_color="transparent", text_color="#F1F5F9", font=ctk.CTkFont(family="Segoe UI", size=12), wrap="word")
        self.insights_box.pack(fill="both", expand=True, padx=15, pady=(0, 8))
        self.insights_box.insert("0.0", "System idle. Awaiting live data stream activation...")

        # Right Panel (Interactive Map Container)
        self.right_deck = ctk.CTkFrame(self.workspace_layout, fg_color="#0A0E17", border_width=1, border_color="#1E293B", width=680, corner_radius=8)
        self.right_deck.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.view_header = ctk.CTkFrame(self.right_deck, fg_color="transparent")
        self.view_header.pack(fill="x", pady=8, padx=15)
        
        self.viewport_title = ctk.CTkLabel(self.view_header, text="🖥 Honor Map Vector Engine", font=ctk.CTkFont(family="JetBrains Mono", size=11, weight="bold"), text_color="#64748B")
        self.viewport_title.pack(side="left", anchor="w")
        
        self.toggle_btn = ctk.CTkButton(self.view_header, text="🗺️ TOGGLE HEATMAP", width=130, height=26, font=ctk.CTkFont(size=11, weight="bold"), fg_color="#1E293B", hover_color="#334155", command=self.toggle_display_mode)
        self.toggle_btn.pack(side="right")
        
        self.display_container = ctk.CTkFrame(self.right_deck, fg_color="transparent")
        self.display_container.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        
        self.viewport_display = ctk.CTkLabel(self.display_container, text="[SYSTEM STREAM IDLE - DISCONNECTED]", font=ctk.CTkFont(size=12), text_color="#475569")
        self.viewport_display.pack(expand=True, fill="both")

    def init_charts(self):
        plt.style.use('dark_background')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 5))
        self.fig.patch.set_facecolor('#0A0E17')
        self.ax1.set_facecolor('#0A0E17')
        self.ax2.set_facecolor('#0A0E17')
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.heatmap_fig, self.heatmap_ax = plt.subplots(figsize=(6, 6))
        self.heatmap_fig.patch.set_facecolor('#0A0E17')
        self.heatmap_ax.set_facecolor('#0A0E17')
        self.heatmap_canvas = FigureCanvasTkAgg(self.heatmap_fig, master=self.display_container)

    def toggle_display_mode(self):
        if self.current_display_mode == "viewport":
            self.current_display_mode = "heatmap"
            self.toggle_btn.configure(text="🖥️ TOGGLE VIEWPORT", fg_color="#A855F7", hover_color="#9333EA")
            self.viewport_display.pack_forget()
            self.heatmap_canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            self.current_display_mode = "viewport"
            self.toggle_btn.configure(text="🗺️ TOGGLE HEATMAP", fg_color="#1E293B", hover_color="#334155")
            self.heatmap_canvas.get_tk_widget().pack_forget()
            self.viewport_display.pack(expand=True, fill="both")

    def change_scenario(self, selection):
        self.active_scenario = selection
        self.header_title.configure(text=f"{selection} Control Node")
        self.last_step_count = -1
        self.insights_box.delete("0.0", "end")
        self.insights_box.insert("0.0", "Switched network context. System ready for deployment sequence...")
        if os.path.exists(self.viewport_path):
            try: os.remove(self.viewport_path)
            except: pass

    def launch_simulation_agent(self):
        script_to_run = self.scenarios[self.active_scenario]["script"]
        try:
            subprocess.Popen([sys.executable, script_to_run])
            self.status_lbl.configure(text="🚀 AGENT ACTIVE: SYNC LIVE", text_color="#34D399")
        except Exception:
            self.status_lbl.configure(text="🔴 SYSTEM RUNTIME FAILED", text_color="#F87171")

    def generate_ai_insights(self, latest):
        """Translates machine indices into natural, human-friendly operational updates."""
        action = str(latest.get("agent_action", "MONITORING"))
        congestion = str(latest.get("congestion_level", "LOW"))
        
        log_lines = []

        # Double Junction Translation Mapping (j0 -> Junction A, j1 -> Junction B)
        if "j0_queue" in latest.index:
            j0_cars = int(latest["j0_queue"])
            j1_cars = int(latest["j1_queue"])
            
            log_lines.append(f"• Junction A (Main Terminal): Currently experiencing a queue buildup of {j0_cars} waiting vehicles.")
            log_lines.append(f"• Junction B (Secondary Exit): Traffic is lighter with {j1_cars} cars idling on the approach lanes.")
            
            if action == "PROPAGATE_J0_TO_J1":
                log_lines.append("⚠️ [CRITICAL EXTENSION ACTIVE]: Traffic queue at Junction A has exceeded safety parameters! Extending green light intervals dynamically to force structural clearing into Junction B lanes.")
            elif "EXTEND" in action:
                log_lines.append(f"⏳ [ADAPTIVE RESPONSE]: Congestion detected. The system has automatically lengthened the green signal phase duration to prevent trailing gridlocks.")
            else:
                log_lines.append("🟢 [NOMINAL FLOW]: All approaches are running within standard capacities. Lights are following baseline cycling intervals.")

        # Cross Junction Translation Mapping (J3 -> Center Cross Roads)
        elif "north_score" in latest.index:
            n_load = float(latest["north_score"])
            w_load = float(latest["west_score"])
            
            log_lines.append(f"• North Corridor Load: Evaluated index at {n_load:.1f} accumulation factor.")
            log_lines.append(f"• West Corridor Load: Evaluated index at {w_load:.1f} accumulation factor.")
            
            if "NORTH_GREEN" in action:
                log_lines.append("⏳ [ADAPTIVE RESPONSE]: Substantial waiting times observed on the North Corridor. Overriding scheduler loop to assign immediate Green Signal Extension to relieve backup.")
            elif "WEST_GREEN" in action:
                log_lines.append("⏳ [ADAPTIVE RESPONSE]: Substantial waiting times observed on the West Corridor. System extended the Green phase to clear waiting segments clean.")

        # T Junction Translation Mapping (J0 -> T-Intersection Stem)
        elif "left_vehicles" in latest.index:
            l, r, t = int(latest["left_vehicles"]), int(latest["right_vehicles"]), int(latest["top_vehicles"])
            log_lines.append(f"• T-Junction Overview: Main lateral lanes running {l + r} active components; structural upper stem holding {t} components.")
            
            if congestion == "HIGH":
                log_lines.append("⚠️ [CRITICAL LOG]: Heavy delays recorded at the main upper intersection lane. Modifying phase timers to avoid long vehicle queues.")
            else:
                log_lines.append("🟢 [NOMINAL FLOW]: Intersections running safely with clear gridline conditions.")

        # Print cleanly into the layout viewport and slide focus downward smoothly
        self.insights_box.delete("0.0", "end")
        self.insights_box.insert("0.0", "\n\n".join(log_lines))
        self.insights_box.see("end")

    def update_telemetry_loop(self):
        sc = self.scenarios[self.active_scenario]
        csv_file = sc["csv"]
        pos_file = sc["pos"]
        
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                if not df.empty:
                    latest = df.iloc[-1]
                    step_val = len(df)
                    
                    if step_val != self.last_step_count:
                        self.last_step_count = step_val
                        
                        total_v = latest.get("total_vehicles", latest.get("north_vehicles", 0) + latest.get("west_vehicles", 0))
                        self.lbl_one_val.configure(text=f"{int(total_v)} Active Units Tracked")
                        
                        readable_action = str(latest.get('agent_action', 'MONITORING')).replace('_', ' ')
                        self.lbl_two_val.configure(text=f"CRITERIA STATE: {readable_action}")
                        
                        # Process our newly translated human logs
                        self.generate_ai_insights(latest)
                        
                        self.ax1.clear()
                        self.ax2.clear()
                        history = df.tail(30)
                        
                        if "north_score" in df.columns:
                            self.ax1.plot(history['time'], history['north_score'], color='#38BDF8', label='North Score', linewidth=2)
                            self.ax1.plot(history['time'], history['west_score'], color='#F43F5E', label='West Score', linewidth=2)
                            self.ax1.legend(loc="upper left", fontsize=8)
                        elif "j0_queue" in df.columns:
                            self.ax1.plot(history.index, history['j0_queue'], color='#F59E0B', label='Junction A Queue')
                            self.ax1.plot(history.index, history['j1_queue'], color='#3B82F6', label='Junction B Queue')
                            self.ax1.legend(loc="upper left", fontsize=8)
                            
                        self.ax1.set_title("Neural Load Factor Evaluation Indices", fontsize=10, color="#94A3B8", loc="left")
                        self.ax1.grid(True, color="#1E293B", linestyle="--")
                        
                        if "north_vehicles" in latest.index:
                            self.ax2.barh(['North Corridor', 'West Corridor'], [latest['north_vehicles'], latest['west_vehicles']], color=['#38BDF8', '#F43F5E'], height=0.4)
                        elif "left_vehicles" in latest.index:
                            self.ax2.barh(['Left Lane', 'Right Lane', 'Upper Stem'], [latest['left_vehicles'], latest['right_vehicles'], latest['top_vehicles']], color=['#10B981', '#3B82F6', '#F59E0B'], height=0.5)
                        else:
                            self.ax2.barh(['Junction A Approach', 'Junction B Approach'], [latest['j0_queue'], latest['j1_queue']], color=['#F59E0B', '#3B82F6'], height=0.4)
                            
                        self.ax2.set_title("Instantaneous Section Queue Density Distribution", fontsize=10, color="#94A3B8", loc="left")
                        self.canvas.draw()
            except Exception:
                pass
                
        if self.current_display_mode == "viewport" and os.path.exists(self.viewport_path):
            try:
                raw_img = Image.open(self.viewport_path)
                display_w = self.viewport_display.winfo_width()
                display_h = self.viewport_display.winfo_height()
                
                if display_w > 100 and display_h > 100:
                    img_w, img_h = raw_img.size
                    scaling_factor = min(display_w / img_w, display_h / img_h)
                    final_w, final_h = int(img_w * scaling_factor), int(img_h * scaling_factor)
                    
                    resized_img = raw_img.resize((final_w, final_h), Image.Resampling.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=resized_img, dark_image=resized_img, size=(final_w, final_h))
                    self.viewport_display.configure(image=ctk_img, text="")
                    self.viewport_display.image = ctk_img 
            except Exception:
                pass
                
        elif self.current_display_mode == "heatmap" and os.path.exists(pos_file):
            try:
                pos_df = pd.read_csv(pos_file)
                if not pos_df.empty and "x" in pos_df.columns and "y" in pos_df.columns:
                    self.heatmap_ax.clear()
                    self.heatmap_ax.hexbin(pos_df['x'], pos_df['y'], gridsize=15, cmap='magma', mincnt=1)
                    self.heatmap_ax.scatter(pos_df['x'], pos_df['y'], color='#00F5FF', s=15, edgecolors='black', alpha=0.8)
                    self.heatmap_ax.set_title("Spatial Vehicle Vector Hotspots", fontsize=10, color="#64748B")
                    self.heatmap_ax.axis('off')
                    self.heatmap_canvas.draw()
            except Exception:
                pass

        self.after(300, self.update_telemetry_loop)

if __name__ == "__main__":
    app = ATOCEnterpriseHub()
    app.mainloop()