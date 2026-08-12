from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

class SidebarManager:
    """
    Manages the Input, Event Log and Node Inspector in the Sidebar.
    """
    def __init__(self, root_widget):
        self.root = root_widget
        self.event_log = root_widget.ids.event_log
        self.cyber_cyan = get_color_from_hex("#00F2FF")
        self.accent_gold = get_color_from_hex("#FFB300")

    def log_event(self, message, type='info'):
        """Adds an entry to the live event log."""
        def _add_item(dt):
            # Hex values for markup
            color_hex = "00F2FF" if type == 'info' else "FFB300"
            item = OneLineListItem(
                text=f"[color={color_hex}]{message}[/color]",
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1]
            )
            self.event_log.add_widget(item, index=len(self.event_log.children))
        
        # Ensure it runs on the main thread
        Clock.schedule_once(_add_item)

    def add_result_item(self, platform, url):
        """Adds a detailed result item to the log."""
        def _add_item(dt):
            item = ThreeLineListItem(
                text=f"FOUND: {platform}",
                secondary_text=url,
                tertiary_text="Status: Verified",
                theme_text_color="Custom",
                text_color=self.cyber_cyan
            )
            self.event_log.add_widget(item, index=0)
        
        Clock.schedule_once(_add_item)

    def clear_log(self):
        self.event_log.clear_widgets()
