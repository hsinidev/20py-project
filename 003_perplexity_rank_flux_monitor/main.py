import dearpygui.dearpygui as dpg
import threading
import time
import random
from datetime import datetime

from core.models import COLORS, Keyword, RankHistory
from core.db import init_db, get_session
from core.monitor import PerplexityAutomator
from core.forecast import RankForecaster
from ui.theme import setup_theme

class RankFluxApp:
    def __init__(self):
        self.running = False
        self.automator = PerplexityAutomator()
        self.keywords = ["AI Search Trends", "GEO Optimization", "Perplexity Ranking", "LLM Citations"]
        self.keyword_data = {k: [] for k in self.keywords}
        self.logs = []
        
        init_db()
        self.setup_dpg()

    def setup_dpg(self):
        dpg.create_context()
        setup_theme()
        
        with dpg.window(label="PERPLEXITY RANK FLUX MONITOR | HSINI MOHAMED", tag="Primary", no_title_bar=True):
            # -- Top Header ---------------------------------------------------
            with dpg.group(horizontal=True):
                dpg.add_text("⚡ SYSTEM STATUS:", color=COLORS["text"])
                self.status_txt = dpg.add_text("STANDBY", color=COLORS["yellow"])
                dpg.add_spacer(width=20)
                dpg.add_text("LIVE FLUX:", color=COLORS["text"])
                self.flux_txt = dpg.add_text("0.0%", color=COLORS["green"])
                dpg.add_spacer(width=20)
                dpg.add_button(label="START MONITORING", callback=self.toggle_monitoring, tag="RunBtn")
                dpg.add_button(label="PANIC RESET", callback=lambda: self.log("System Panic Reset Issued", COLORS["red"]))

            dpg.add_separator()

            # -- Main Content -------------------------------------------------
            with dpg.group(horizontal=True):
                # Left Column: Rank Ladder
                with dpg.child_window(width=400, border=True):
                    dpg.add_text("📊 LIVE RANK LADDER", color=COLORS["blue"])
                    with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                        dpg.add_table_column(label="POS")
                        dpg.add_table_column(label="DOMAIN")
                        dpg.add_table_column(label="FLUX")
                        dpg.add_table_column(label="TREND")
                        
                        self.table_rows = []
                        for i in range(1, 11):
                            with dpg.table_row():
                                dpg.add_text(str(i))
                                dpg.add_text("---", tag=f"dom_{i}")
                                dpg.add_text("0.0", tag=f"flux_{i}")
                                dpg.add_text("STABLE", tag=f"trend_{i}")

                # Right Column: Charts & Logs
                with dpg.group():
                    with dpg.child_window(height=400, border=True):
                        dpg.add_text("📈 VOLATILITY SPARKLINE", color=COLORS["blue"])
                        with dpg.plot(label="Real-time Rank Drift", height=-1, width=-1):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis, label="Time (Ticks)")
                            with dpg.plot_axis(dpg.mvYAxis, label="Position"):
                                dpg.set_axis_limits(dpg.last_item(), 0, 12)
                                self.series_tag = dpg.add_line_series([], [], label="Avg Rank")

                    with dpg.child_window(height=-1, border=True):
                        dpg.add_text("📑 SYSTEM TELEMETRY", color=COLORS["blue"])
                        self.log_box = dpg.add_text("")

        dpg.create_viewport(title='Perplexity Rank Flux', width=1200, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary", True)

    def log(self, msg, color=COLORS["text"]):
        ts = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{ts}] {msg}")
        if len(self.logs) > 20: self.logs.pop(0)
        dpg.set_value(self.log_box, "\n".join(self.logs))
        # Logic for panic alert
        if "DROP" in msg.upper() and color == COLORS["red"]:
            self.trigger_panic_alert(msg)

    def trigger_panic_alert(self, msg):
        # In a real app, this would use a toast notification or sound
        print(f"!!! PANIC ALERT: {msg} !!!")

    def toggle_monitoring(self):
        self.running = not self.running
        if self.running:
            dpg.configure_item("RunBtn", label="STOP MONITORING")
            dpg.set_value(self.status_txt, "ACTIVE")
            dpg.configure_item(self.status_txt, color=COLORS["green"])
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            dpg.configure_item("RunBtn", label="START MONITORING")
            dpg.set_value(self.status_txt, "STANDBY")
            dpg.configure_item(self.status_txt, color=COLORS["yellow"])

    def monitor_loop(self):
        ticks = 0
        y_data = []
        x_data = []
        
        while self.running:
            kw = random.choice(self.keywords)
            self.log(f"Scanning '{kw}'...")
            
            ranks = self.automator.scrape_rank(kw)
            
            # Update UI Table
            avg_pos = 0
            for r in ranks:
                idx = r["position"]
                if idx <= 10:
                    dpg.set_value(f"dom_{idx}", r["domain"])
                    dpg.set_value(f"flux_{idx}", f"{r['volatility']:+.1f}")
                    
                    color = COLORS["green"] if r["volatility"] > 0 else COLORS["red"] if r["volatility"] < 0 else COLORS["text"]
                    dpg.configure_item(f"flux_{idx}", color=color)
                    
                    trend = "BULL" if r["volatility"] > 1 else "BEAR" if r["volatility"] < -1 else "STABLE"
                    dpg.set_value(f"trend_{idx}", trend)
                    dpg.configure_item(f"trend_{idx}", color=color)
                    
                    avg_pos += idx

            # Update Chart
            ticks += 1
            avg_pos /= len(ranks)
            y_data.append(avg_pos)
            x_data.append(ticks)
            if len(y_data) > 50:
                y_data.pop(0)
                x_data.pop(0)
            
            dpg.set_value(self.series_tag, [x_data, y_data])
            
            # Forecast
            if len(y_data) > 5:
                f = RankForecaster.predict_shift([int(y) for y in y_data])
                dpg.set_value(self.flux_txt, f"{f['probability']}% {f['direction']}")
                dpg.configure_item(self.flux_txt, color=COLORS["green"] if f['direction']=="UP" else COLORS["red"])

            # Check for drop (Panic logic)
            if any(r["volatility"] < -5 for r in ranks):
                self.log(f"CRITICAL DROP detected in {kw}!", COLORS["red"])

            time.sleep(2)

    def run(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

if __name__ == "__main__":
    app = RankFluxApp()
    app.run()
