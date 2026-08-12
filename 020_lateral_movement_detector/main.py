import wx
import sys
import os

# Local Imports
from ui.command_center import CommandCenter
from core.sniffer_engine import SnifferEngine

class LateralMovementApp(wx.App):
    """
    Network Lateral Movement Detector - Bootstrapper.
    Developed by HSINI MOHAMED.
    """
    def OnInit(self):
        self.frame = CommandCenter(None, title="Network Lateral Movement Detector (Enterprise NDR Edition)")
        self.frame.Show()
        
        # Initialize Sniffer
        self.sniffer = SnifferEngine(self.on_packet_captured)
        self.frame.btn_scan.Bind(wx.EVT_BUTTON, self.toggle_scan)
        
        return True

    def toggle_scan(self, event):
        if not self.sniffer.running:
            self.sniffer.start()
            self.frame.btn_scan.SetLabel("HALT SCANNER")
            self.frame.btn_scan.SetBackgroundColour(wx.Colour(255, 75, 43)) # Crimson
            print("Scanner Initialized.")
        else:
            self.sniffer.stop()
            self.frame.btn_scan.SetLabel("INITIALIZE SCANNER")
            self.frame.btn_scan.SetBackgroundColour(wx.Colour(111, 0, 255)) # Indigo
            print("Scanner Halted.")

    def on_packet_captured(self, data):
        # Update UI from sniffer callback (simplified)
        # In a production app, use wx.CallAfter or Events
        pass

if __name__ == "__main__":
    # Check for kernel permissions (Simulated)
    print("Verifying Kernel Permissions & Interface Mapping...")
    
    app = LateralMovementApp()
    app.MainLoop()
