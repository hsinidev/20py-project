import asyncio
import sqlite3
import threading
import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

# Import custom modules
from engine.scanner import OSINTScanner
from engine.dorker import GoogleDorker
from ui.canvas_controller import CanvasController
from ui.sidebar_manager import SidebarManager
from utils.exporter import generate_report

class MainScreen(Screen):
    pass

class IntelHubApp(MDApp):
    def build(self):
        self.title = "Digital Footprint Intelligence Hub"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Amber"
        
        # Load KV styles
        Builder.load_file("ui/styles.kv")
        
        self.root_screen = MainScreen()
        return self.root_screen

    def on_start(self):
        # Initialize Managers
        self.sidebar = SidebarManager(self.root_screen)
        self.canvas_ctrl = CanvasController(self.root_screen.ids.graph_container)
        
        # Initialize Engines
        self.scanner = OSINTScanner()
        self.dorker = GoogleDorker()
        
        # Database Initialization
        self.init_db()
        
        self.sidebar.log_event("SYSTEM ONLINE: Waiting for Target Input...")
        self.investigation_data = {"accounts": [], "dorks": []}
        self.current_target = None

    def init_db(self):
        db_path = "data/investigations.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        with open("data/schema.sql", 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def start_investigation(self, target):
        if not target:
            Snackbar(text="Error: Target ID cannot be empty").open()
            return
        
        self.current_target = target
        self.investigation_data = {"accounts": [], "dorks": []}
        self.sidebar.clear_log()
        self.sidebar.log_event(f"INITIALIZING INVESTIGATION: {target}")
        
        # Add primary node to canvas
        self.canvas_ctrl.add_entity(target, type='poi')
        
        # Start scanning in a background thread to keep UI responsive
        threading.Thread(target=self.run_async_tasks, args=(target,), daemon=True).start()

    def run_async_tasks(self, target):
        """Runs async scanner and dorker in the background."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 1. Platform Scanning
        self.sidebar.log_event(f"SCANNING 50+ PLATFORMS...")
        
        def scanner_callback(result):
            self.investigation_data["accounts"].append(result)
            self.sidebar.add_result_item(result['platform'], result['url'])
            # Update Graph
            Clock.schedule_once(lambda dt: self.canvas_ctrl.add_entity(result, type='account', parent=target))
            # Save to DB
            self.save_to_db("account", result)

        loop.run_until_complete(self.scanner.run_scan(target, callback=scanner_callback))
        
        # 2. Google Dorking
        self.sidebar.log_event(f"INITIATING ADVANCED DORKING...")
        
        def dorker_callback(result):
            self.investigation_data["dorks"].append(result)
            self.sidebar.log_event(f"DORK FOUND: {result['title'][:30]}...")
            self.save_to_db("dork", result)

        loop.run_until_complete(self.dorker.run_dorking(target, callback=dorker_callback))
        
        self.sidebar.log_event("INVESTIGATION COMPLETE", type='warning')
        loop.close()

    def save_to_db(self, type, data):
        cursor = self.conn.cursor()
        if type == "account":
            cursor.execute(
                "INSERT INTO discovered_accounts (platform, url, metadata) VALUES (?, ?, ?)",
                (data['platform'], data['url'], str(data))
            )
        elif type == "dork":
            cursor.execute(
                "INSERT INTO dork_results (query, result_url, title, snippet) VALUES (?, ?, ?, ?)",
                (data['query'], data['url'], data['title'], data['snippet'])
            )
        self.conn.commit()

    def export_results(self):
        if not self.current_target:
            Snackbar(text="No data to export").open()
            return
        
        base_path = "exports"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        reports = generate_report(self.investigation_data, base_path, self.current_target)
        self.sidebar.log_event(f"REPORTS GENERATED in /exports/", type='warning')
        Snackbar(text=f"Reports exported to {base_path}").open()

if __name__ == "__main__":
    IntelHubApp().run()
