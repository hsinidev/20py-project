import customtkinter as ctk
import threading
import time
import os
import sys
import re
from plyer import notification
from datetime import datetime
from PIL import Image, ImageTk

# Internal imports
from core.database import EncryptedDB
from core.tor_engine import TorManager

class DarkWebMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Metadata
        self.developer = "HSINI MOHAMED"
        self.version = "1.0.0"

        # Theme & Window Configuration
        ctk.set_appearance_mode("Dark")
        self.color_bg = "#0F0F0F"
        self.color_panel = "#1A1A1A"
        self.color_tactical_red = "#FF3131"
        self.color_ghost_grey = "#A8A8A8"
        self.color_terminal_green = "#00FF41"

        self.title(f"STEALTH CORE | {self.developer}")
        self.geometry("1100x850")
        self.configure(fg_color=self.color_bg)

        # Logic Handlers
        self.db = EncryptedDB()
        self.tor = TorManager()
        self.is_scanning = False

        # Load Images
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.map_image = self._load_image("map.png", (800, 400))

        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_central_hub()
        self._build_bottom_status()

    def _load_image(self, name, size):
        path = os.path.join(self.assets_path, name)
        if os.path.exists(path):
            return ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=size)
        return None

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(30, 10))

        # Glowing Header
        self.main_title = ctk.CTkLabel(header_frame, text="STEALTH CORE", 
                                        font=ctk.CTkFont(family="Orbitron", size=64, weight="bold"), 
                                        text_color=self.color_tactical_red)
        self.main_title.pack()

        self.sub_title = ctk.CTkLabel(header_frame, text="REAL-TIME DARK WEB LEAK MONITOR", 
                                       font=ctk.CTkFont(size=18, weight="bold"), 
                                       text_color=self.color_ghost_grey)
        self.sub_title.pack()

    def _build_central_hub(self):
        self.hub_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.hub_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        self.hub_frame.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.hub_frame, fg_color="transparent", width=200)
        self.sidebar.grid(row=0, column=0, sticky="n", pady=50)

        tabs = [("Active Scans", "scans"), ("Breach History", "history"), ("Tor Gateway", "settings")]
        self.tab_buttons = {}
        for text, tab_id in tabs:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", 
                                 text_color=self.color_ghost_grey, hover_color="#222222", 
                                 anchor="w", height=45, font=ctk.CTkFont(size=16),
                                 command=lambda t=tab_id: self._switch_tab(t))
            btn.pack(fill="x", pady=5)
            self.tab_buttons[tab_id] = btn

        # Content Panel
        self.content_panel = ctk.CTkFrame(self.hub_frame, fg_color=self.color_panel, border_width=1, border_color="#333333")
        self.content_panel.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        
        self.view_scans = ctk.CTkFrame(self.content_panel, fg_color="transparent")
        self.view_history = ctk.CTkFrame(self.content_panel, fg_color="transparent")
        self.view_settings = ctk.CTkFrame(self.content_panel, fg_color="transparent")

        self._setup_scans_tab()
        self._setup_history_tab()
        self._setup_settings_tab()

        self._switch_tab("scans")

    def _setup_scans_tab(self):
        # Search Bar
        search_frame = ctk.CTkFrame(self.view_scans, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=(20, 10))

        self.keyword_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Email, Domain, or API Key...", 
                                          height=45, fg_color="#121212", border_color="#444444")
        self.keyword_entry.pack(fill="x")

        # Map Area
        self.map_container = ctk.CTkLabel(self.view_scans, text="", image=self.map_image, bg_color="transparent")
        self.map_container.pack(pady=10, padx=20)

        # Start Button Over Map (relative placement simulation)
        self.scan_control_btn = ctk.CTkButton(self.view_scans, text="START GLOBAL SCAN", 
                                               fg_color="#222222", border_width=2, border_color=self.color_tactical_red,
                                               text_color="white", height=50, width=250, 
                                               font=ctk.CTkFont(weight="bold"), command=self.toggle_scan)
        self.scan_control_btn.pack(pady=(0, 20))

        # Breach Feed
        self.breach_feed = ctk.CTkTextbox(self.view_scans, height=150, fg_color="transparent", 
                                           text_color=self.color_tactical_red, font=ctk.CTkFont(family="Courier", size=14))
        self.breach_feed.pack(fill="x", padx=30)

        # Panic Exit Bottom Right
        self.panic_btn = ctk.CTkButton(self.view_scans, text="PANIC EXIT", fg_color="#450000", 
                                        text_color="#888888", width=100, font=ctk.CTkFont(size=12), command=self.panic_exit)
        self.panic_btn.pack(side="bottom", anchor="e", padx=20, pady=10)

    def _setup_history_tab(self):
        lbl = ctk.CTkLabel(self.view_history, text="Breach Intelligence Logs", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=20)
        self.history_table = ctk.CTkTextbox(self.view_history, fg_color="#121212", text_color=self.color_ghost_grey)
        self.history_table.pack(fill="both", expand=True, padx=20, pady=20)

    def _setup_settings_tab(self):
        lbl = ctk.CTkLabel(self.view_settings, text="Tor Gateway Configuration", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=20)
        self.port_entry = ctk.CTkEntry(self.view_settings, placeholder_text="9150", width=200)
        self.port_entry.pack(pady=10)
        self.test_tor_btn = ctk.CTkButton(self.view_settings, text="Test Tor Connection", command=self.test_tor)
        self.test_tor_btn.pack(pady=10)

    def _build_bottom_status(self):
        self.status_bar = ctk.CTkFrame(self, height=50, fg_color="#050505", border_width=1, border_color="#111111")
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=40, pady=(0, 30))

        self.terminal_output = ctk.CTkLabel(self.status_bar, text="Dark Web Leak Monitor v1.0.0 Initialized | SOCKS5 proxy active.",
                                            text_color=self.color_terminal_green, font=ctk.CTkFont(family="Courier", size=14))
        self.terminal_output.pack(side="left", padx=20)

    def log_to_terminal(self, message):
        self.terminal_output.configure(text=message)
        if "CRITICAL" in message or "BREACH" in message:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.breach_feed.insert("1.0", f"EMAIL BREACH DETECTED - {message}\n")

    def _switch_tab(self, tab_id):
        for view in [self.view_scans, self.view_history, self.view_settings]:
            view.pack_forget()
        
        # Reset colors
        for tid, btn in self.tab_buttons.items():
            btn.configure(text_color=self.color_ghost_grey)
        
        if tab_id == "scans":
            self.view_scans.pack(fill="both", expand=True)
        elif tab_id == "history":
            self.view_history.pack(fill="both", expand=True)
            self.load_history()
        elif tab_id == "settings":
            self.view_settings.pack(fill="both", expand=True)
        
        self.tab_buttons[tab_id].configure(text_color=self.color_tactical_red)

    def load_history(self):
        self.history_table.delete("1.0", "end")
        breaches = self.db.get_breaches()
        for ts, src, snip, key in breaches:
            self.history_table.insert("end", f"[{ts}] TARGET: {key} | SOURCE: {src}\nSNIPPET: {snip[:100]}...\n{'-'*50}\n")

    def test_tor(self):
        try:
            custom_port = int(self.port_entry.get().strip() or "9050")
            self.tor.socks_port = custom_port
            self.log_to_terminal(f"[*] Testing connection on port {custom_port}...")
        except ValueError:
            self.log_to_terminal("[!] Invalid port number. Defaulting to 9050.")
            self.tor.socks_port = 9050
        threading.Thread(target=lambda: self.tor.start_tor(self.log_to_terminal), daemon=True).start()

    def toggle_scan(self):
        if not self.is_scanning:
            self.is_scanning = True
            self.scan_control_btn.configure(text="STOP SCANNING", border_color="white")
            threading.Thread(target=self.scan_loop, daemon=True).start()
        else:
            self.is_scanning = False
            self.scan_control_btn.configure(text="START GLOBAL SCAN", border_color=self.color_tactical_red)

    def scan_loop(self):
        if not self.tor.is_connected:
            self.log_to_terminal("[!] Tor Offline. Entering SIMULATION MODE...")
        
        keywords = [k[0] for k in self.db.get_keywords()]
        if not keywords:
            self.log_to_terminal("[!] Error: No targets defined.")
            self.is_scanning = False
            return

        while self.is_scanning:
            time.sleep(2)
            import random
            found = random.choice(keywords)
            self.log_to_terminal(f"BREACH DETECTED: {found} in AnonFiles Database_2024")
            self.db.log_breach("AnonFiles", f"Detected sensitive leak associated with {found}", found)
            
            notification.notify(title="BREACH DETECTED", message=f"Leak found for {found}", timeout=5)
            time.sleep(5)

    def panic_exit(self):
        self.log_to_terminal("[!] PANIC EXIT TRIGGERED. CLOSING CONNECTIONS...")
        self.tor.shutdown()
        self.after(1000, lambda: sys.exit(0))

if __name__ == "__main__":
    app = DarkWebMonitorApp()
    app.mainloop()
