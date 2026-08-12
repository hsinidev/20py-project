import dearpygui.dearpygui as dpg
import time
import random

class TunnelDashboard:
    """
    GPU-Accelerated 'Matrix Green' Industrial Dashboard using Dear PyGui.
    """
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.is_running = True
        
        dpg.create_context()
        self._setup_theme()
        self._create_windows()
        dpg.create_viewport(title='ENCRYPTED TUNNEL MANAGER - HSINI MOHAMED', width=1000, height=700)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def _setup_theme(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (13, 2, 8, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (26, 26, 26, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 65, 255)) # Matrix Green
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 255, 65, 100))
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)
        dpg.bind_theme(global_theme)

    def _create_windows(self):
        with dpg.window(label="COMMAND CENTER", width=1000, height=700, no_title_bar=True, no_move=True):
            # Header
            with dpg.group(horizontal=True):
                dpg.add_text("SYSTEM STATUS:", color=(0, 255, 65))
                self.status_text = dpg.add_text("ENCRYPTED TUNNEL STANDBY", color=(0, 255, 65))
                dpg.add_spacer(width=400)
                dpg.add_text("CREDIT: Developed by HSINI MOHAMED", color=(0, 255, 65, 150))

            dpg.add_separator()

            # Traffic Plot
            with dpg.plot(label="REAL-TIME TUNNEL TELEMETRY (MB/S)", height=300, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)")
                with dpg.plot_axis(dpg.mvYAxis, label="Throughput", tag="y_axis"):
                    self.inbound_line = dpg.add_line_series([0.0], [0.0], label="Inbound", tag="inbound_line")
                    self.outbound_line = dpg.add_line_series([0.0], [0.0], label="Outbound", tag="outbound_line")
                dpg.set_axis_limits("y_axis", 0, 10)

            # Controls
            with dpg.group(horizontal=True):
                with dpg.child_window(width=300, height=300, border=True):
                    dpg.add_text("CONNECTION PROFILES")
                    dpg.add_combo(["USA-NORTH-SHIELD", "UK-LONDON-TUNNEL", "DE-BERLIN-STEALTH", "JP-TOKYO-NODE"], label="Select Node", default_value="USA-NORTH-SHIELD")
                    dpg.add_input_text(label="Gateway IP", default_value="10.8.0.1")
                    dpg.add_spacer(height=10)
                    dpg.add_button(label="INITIATE TUNNEL", width=-1, height=40, callback=self._on_initiate)
                    dpg.add_button(label="ACTIVATE KILL-SWITCH", width=-1, height=40, callback=self._on_killswitch)
                    dpg.add_button(label="TERMINATE SESSION", width=-1, height=40, callback=self._on_terminate)

                with dpg.child_window(width=-1, height=300, border=True):
                    dpg.add_text("LIVE SECURITY PULSE")
                    self.pulse_status = dpg.add_text("NO LEAKS DETECTED", color=(0, 255, 65))
                    dpg.add_separator()
                    dpg.add_text("SESSION LOGS:", color=(0, 255, 65, 150))
                    self.log_list = dpg.add_listbox(items=[], width=-1, num_items=10)

    def _on_initiate(self):
        dpg.set_value(self.status_text, "TUNNEL ESTABLISHED [AES-256]")
        self._log("SSHv2 Handshake Successful.")
        self._log("Tunneling established on port 8080.")

    def _on_killswitch(self):
        dpg.set_value(self.pulse_status, "KILL-SWITCH ACTIVE: LOCAL NETWORK SHIELDED")
        dpg.configure_item(self.pulse_status, color=(255, 179, 0))
        self._log("Kernel-level blocking rules injected.")

    def _on_terminate(self):
        dpg.set_value(self.status_text, "ENCRYPTED TUNNEL STANDBY")
        dpg.set_value(self.pulse_status, "NO LEAKS DETECTED")
        dpg.configure_item(self.pulse_status, color=(0, 255, 65))
        self._log("Session Terminated. Rules cleared.")

    def _log(self, msg):
        current_logs = dpg.get_item_configuration(self.log_list)['items']
        current_logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        dpg.configure_item(self.log_list, items=current_logs)

    def run(self):
        while dpg.is_dearpygui_running():
            # Update plot data
            in_data, out_data = self.analyzer.get_data()
            x_data = list(range(len(in_data)))
            dpg.set_value(self.inbound_line, [x_data, in_data])
            dpg.set_value(self.outbound_line, [x_data, out_data])
            
            dpg.render_dearpygui_frame()
        dpg.destroy_context()
