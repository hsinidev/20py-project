import wx
import wx.lib.newevent
import random
import time
import math

# New Event for thread communication
TrafficEvent, EVT_TRAFFIC = wx.lib.newevent.NewEvent()

class CommandCenter(wx.Frame):
    """
    Main WxPython Dashboard for Network Lateral Movement Detection.
    Theme: Network-Command (Electric Indigo on Obsidian).
    """
    def __init__(self, parent, title):
        super(CommandCenter, self).__init__(parent, title=title, size=(1200, 800))
        
        self.primary_color = wx.Colour(111, 0, 255) # Electric Indigo
        self.bg_color = wx.Colour(11, 12, 16)      # Obsidian
        self.surface_color = wx.Colour(31, 40, 51)  # Space Blue
        self.text_color = wx.Colour(197, 198, 199) # Silver
        
        self.SetBackgroundColour(self.bg_color)
        self.init_ui()
        
    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header = wx.Panel(self)
        header.SetBackgroundColour(self.surface_color)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(header, label="NETWORK COMMAND - LATERAL MOVEMENT DETECTOR")
        title.SetForegroundColour(self.primary_color)
        title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        header_sizer.Add(title, 0, wx.ALL | wx.CENTER, 15)
        
        credit = wx.StaticText(header, label="Developed by HSINI MOHAMED")
        credit.SetForegroundColour(self.text_color)
        header_sizer.AddStretchSpacer()
        header_sizer.Add(credit, 0, wx.ALL | wx.CENTER, 15)
        
        header.SetSizer(header_sizer)
        main_sizer.Add(header, 0, wx.EXPAND)

        # Content Area
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left Panel: Live Topology Map
        self.map_panel = wx.Panel(self)
        self.map_panel.SetBackgroundColour(self.bg_color)
        self.map_panel.Bind(wx.EVT_PAINT, self.on_paint_map)
        content_sizer.Add(self.map_panel, 3, wx.EXPAND | wx.ALL, 5)
        
        # Right Panel: Threat Feed
        self.feed_panel = wx.Panel(self)
        self.feed_panel.SetBackgroundColour(self.surface_color)
        feed_sizer = wx.BoxSizer(wx.VERTICAL)
        
        feed_label = wx.StaticText(self.feed_panel, label="REAL-TIME THREAT FEED")
        feed_label.SetForegroundColour(self.primary_color)
        feed_sizer.Add(feed_label, 0, wx.ALL, 10)
        
        self.feed_list = wx.ListCtrl(self.feed_panel, style=wx.LC_REPORT | wx.BORDER_NONE)
        self.feed_list.InsertColumn(0, "Source IP", width=120)
        self.feed_list.InsertColumn(1, "Type", width=120)
        self.feed_list.InsertColumn(2, "Score", width=60)
        self.feed_list.SetBackgroundColour(self.bg_color)
        self.feed_list.SetForegroundColour(self.text_color)
        feed_sizer.Add(self.feed_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Controls
        self.btn_scan = wx.Button(self.feed_panel, label="INITIALIZE SCANNER")
        self.btn_scan.SetBackgroundColour(self.primary_color)
        self.btn_scan.SetForegroundColour(wx.WHITE)
        feed_sizer.Add(self.btn_scan, 0, wx.EXPAND | wx.ALL, 10)
        
        self.feed_panel.SetSizer(feed_sizer)
        content_sizer.Add(self.feed_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        main_sizer.Add(content_sizer, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        # Timer for pulsing animations
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(50) # 20 FPS
        self.pulse_phase = 0

    def on_paint_map(self, event):
        dc = wx.PaintDC(self.map_panel)
        dc.SetBackground(wx.Brush(self.bg_color))
        dc.Clear()
        
        w, h = self.map_panel.GetSize()
        center_x, center_y = w // 2, h // 2
        
        # Draw some mock nodes with Indigo Pulse
        nodes = [
            (center_x, center_y, "Gate-01", False),
            (center_x - 150, center_y - 100, "User-X", False),
            (center_x + 150, center_y - 100, "DB-Server", True), # Suspicious
            (center_x, center_y + 150, "Admin-Vault", False)
        ]
        
        pulse_size = 5 * (1 + 0.5 * math.sin(self.pulse_phase))
        
        dc.SetPen(wx.Pen(self.primary_color, 2))
        for x, y, label, suspicious in nodes:
            color = wx.Colour(255, 75, 43) if suspicious else self.primary_color
            dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_TRANSPARENT))
            
            # Draw pulse perimeter
            dc.SetPen(wx.Pen(color, 1))
            dc.DrawCircle(x, y, int(30 + pulse_size))
            
            # Draw core node
            dc.SetBrush(wx.Brush(color))
            dc.DrawCircle(x, y, 15)
            
            dc.SetTextForeground(self.text_color)
            dc.DrawText(label, x - 20, y + 25)
            
            # Draw links to Gateway
            if x != center_x or y != center_y:
                dc.SetPen(wx.Pen(color, 1, wx.PENSTYLE_DOT))
                dc.DrawLine(x, y, center_x, center_y)

    def on_timer(self, event):
        self.pulse_phase += 0.2
        self.map_panel.Refresh()

    def add_threat(self, src, type, score):
        index = self.feed_list.InsertItem(0, src)
        self.feed_list.SetItem(index, 1, type)
        self.feed_list.SetItem(index, 2, str(score))
        if score > 80:
            self.feed_list.SetItemTextColour(index, wx.Colour(255, 75, 43))
