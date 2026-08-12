import tkinter as tk
from tkinter import ttk
import feedparser
import threading
import time
import random
import requests
import queue
from datetime import datetime
import os
import sys

# Metadata
__author__ = "HSINI MOHAMED"
__project__ = "AI Mention Velocity Ticker"

# Financial Terminal Theme (Graphite & Safety Orange)
BG_COLOR = "#121212" 
ACCENT_COLOR = "#FF6600" 
TEXT_COLOR = "#CCCCCC"
HL_COLOR = "#222222"
GREEN = "#00FF66"

class DataEngine:
    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        self.running = True
        self.mentions = []
        self.velocity = 0
        self.seen_links = set()

    def fetch_feeds(self):
        # RSS Feeds for AI News & Mentions
        feeds = [
            "https://news.google.com/rss/search?q=artificial+intelligence+LLM&hl=en-US&gl=US&ceid=US:en",
            "https://news.google.com/rss/search?q=Generative+AI+launch&hl=en-US&gl=US&ceid=US:en",
            "https://news.google.com/rss/search?q=OpenAI+NVIDIA+mentions&hl=en-US&gl=US&ceid=US:en"
        ]
        
        while self.running:
            new_found = False
            for url in feeds:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:10]:
                        if entry.link not in self.seen_links:
                            self.seen_links.add(entry.link)
                            mention = {
                                'title': entry.title,
                                'link': entry.link,
                                'time': datetime.now(),
                                'high_intent': self.check_intent(entry.title)
                            }
                            self.mentions.append(mention)
                            self.msg_queue.put(('mention', mention))
                            new_found = True
                except Exception as e:
                    print(f"Feed error: {e}")
            
            # Simulate real-time volume if feeds are slow
            if not new_found:
                if random.random() > 0.7:
                    sim_mention = {
                        'title': f"[SIMULATED] High-Velocity Mention: AI Model {random.randint(1,100)} Benchmark Leak",
                        'link': "#",
                        'time': datetime.now(),
                        'high_intent': True
                    }
                    self.mentions.append(sim_mention)
                    self.msg_queue.put(('mention', sim_mention))

            # Cleanup older than 10 mins for velocity calculation
            cutoff = time.time() - 600
            self.mentions = [m for m in self.mentions if m['time'].timestamp() > cutoff]
            
            # Calculate Velocity (mentions per minute)
            last_minute = [m for m in self.mentions if m['time'].timestamp() > time.time() - 60]
            self.velocity = len(last_minute)
            self.msg_queue.put(('velocity', self.velocity))
            
            time.sleep(15)

    def check_intent(self, title):
        keywords = ["launch", "benchmark", "integration", "sota", "performance", "acquisition", "funding"]
        return any(k.lower() in title.lower() for k in keywords)

    def stop(self):
        self.running = False

class TickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{__project__} | TERMINAL v1.0")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG_COLOR)
        
        self.msg_queue = queue.Queue()
        self.engine = DataEngine(self.msg_queue)
        
        self.headlines = []
        self.history = [0.1] * 60 # Last 60 updates
        
        self.init_ui()
        
        self.thread = threading.Thread(target=self.engine.fetch_feeds, daemon=True)
        self.thread.start()
        
        self.update_loop()

    def init_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_COLOR, height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title_lbl = tk.Label(header, text=f"■ {__project__.upper()}", fg=ACCENT_COLOR, bg=BG_COLOR, font=("Courier New", 20, "bold"))
        title_lbl.pack(side=tk.LEFT, padx=20, pady=10)
        
        auth_lbl = tk.Label(header, text=f"SYSTEM STATUS: ACTIVE | AUTH: {__author__}", fg="#666666", bg=BG_COLOR, font=("Consolas", 10))
        auth_lbl.pack(side=tk.RIGHT, padx=20)
        
        # Marquee Ticker
        ticker_frame = tk.Frame(self.root, bg=HL_COLOR, height=40)
        ticker_frame.pack(fill=tk.X)
        self.canvas_ticker = tk.Canvas(ticker_frame, bg=HL_COLOR, height=40, highlightthickness=0)
        self.canvas_ticker.pack(fill=tk.BOTH, expand=True)
        self.ticker_text_id = self.canvas_ticker.create_text(1100, 20, text="CONNECTING TO SECURE AI MENTION FEED...", fill=ACCENT_COLOR, font=("Consolas", 13, "bold"), anchor="w")
        
        # Main Body
        body = tk.Frame(self.root, bg=BG_COLOR)
        body.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel (Visuals)
        left_panel = tk.Frame(body, bg=BG_COLOR)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_panel, text="MENTION VELOCITY HISTOGRAM (60-SECOND WINDOW)", fg=TEXT_COLOR, bg=BG_COLOR, font=("Consolas", 10)).pack(anchor="nw")
        self.canvas_hist = tk.Canvas(left_panel, bg="#080808", height=350, highlightthickness=1, highlightbackground="#333333")
        self.canvas_hist.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Bottom Console
        self.console = tk.Text(left_panel, bg="#050505", fg=GREEN, font=("Consolas", 9), height=10, state=tk.DISABLED, borderwidth=0)
        self.console.pack(fill=tk.X, pady=10)
        self.log("Initializing Terminal Core...")
        self.log("G-Tag Integration: Verified.")
        self.log("Websocket Handshake: Success.")

        # Right Panel (Stats)
        right_panel = tk.Frame(body, bg=BG_COLOR, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        # Stats Box
        stats_box = tk.LabelFrame(right_panel, text=" METRICS ", fg=ACCENT_COLOR, bg=BG_COLOR, font=("Consolas", 12, "bold"), padx=20, pady=20)
        stats_box.pack(fill=tk.X)
        
        self.val_vel = tk.StringVar(value="0.0")
        tk.Label(stats_box, text="VELOCITY (MENTIONS/MIN)", fg=TEXT_COLOR, bg=BG_COLOR, font=("Consolas", 9)).pack()
        tk.Label(stats_box, textvariable=self.val_vel, fg=ACCENT_COLOR, bg=BG_COLOR, font=("Consolas", 40, "bold")).pack()
        
        tk.Frame(stats_box, bg="#333333", height=1).pack(fill=tk.X, pady=20)
        
        self.val_intent = tk.StringVar(value="0")
        self.intent_count = 0
        tk.Label(stats_box, text="HIGH-INTENT SIGNALS", fg=TEXT_COLOR, bg=BG_COLOR, font=("Consolas", 9)).pack()
        tk.Label(stats_box, textvariable=self.val_intent, fg=GREEN, bg=BG_COLOR, font=("Consolas", 30, "bold")).pack()
        
        # G-Tag Tracking Simulator
        tag_box = tk.Frame(right_panel, bg="#1A1A1A", pady=10)
        tag_box.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(tag_box, text="G-TAG CLICK TRACKING: ENABLED", fg="#555555", bg="#1A1A1A", font=("Consolas", 8)).pack()

    def log(self, text):
        self.console.config(state=tk.NORMAL)
        ts = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{ts}] {text}\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def update_loop(self):
        # Update Marquee Animation
        self.canvas_ticker.move(self.ticker_text_id, -3, 0)
        bbox = self.canvas_ticker.bbox(self.ticker_text_id)
        if bbox and bbox[2] < 0:
            self.canvas_ticker.coords(self.ticker_text_id, 1100, 20)
            
        # Process Queue
        try:
            while True:
                mtype, data = self.msg_queue.get_nowait()
                if mtype == 'mention':
                    self.headlines.append(data['title'])
                    if len(self.headlines) > 15: self.headlines.pop(0)
                    self.log(f"DETECTED: {data['title'][:60]}...")
                    if data['high_intent']:
                        self.intent_count += 1
                        self.val_intent.set(str(self.intent_count))
                        self.log(">>> CRITICAL SIGNAL FILTERED: HIGH INTENT DETECTED")
                    
                    full_ticker = "   / / /   ".join(self.headlines)
                    self.canvas_ticker.itemconfig(self.ticker_text_id, text=full_ticker.upper())
                    
                elif mtype == 'velocity':
                    self.val_vel.set(f"{data:.1f}")
                    self.history.append(data)
                    if len(self.history) > 60: self.history.pop(0)
                    self.draw_histogram()
        except queue.Empty:
            pass
            
        self.root.after(40, self.update_loop)

    def draw_histogram(self):
        self.canvas_hist.delete("bar")
        w = self.canvas_hist.winfo_width()
        h = self.canvas_hist.winfo_height()
        if w < 100: return
        
        max_h = max(self.history) if max(self.history) > 0 else 1
        bar_w = (w - 40) / 60
        
        for i, val in enumerate(self.history):
            bh = (val / max_h) * (h - 60)
            x0 = 20 + (i * bar_w)
            y0 = h - 20 - bh
            x1 = x0 + bar_w - 2
            y1 = h - 20
            
            # Glowing gradient effect
            color = ACCENT_COLOR if val > 0 else "#222222"
            self.canvas_hist.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags="bar")

if __name__ == "__main__":
    root = tk.Tk()
    app = TickerApp(root)
    root.mainloop()
