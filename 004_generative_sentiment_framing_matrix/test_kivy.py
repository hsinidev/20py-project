import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (1100, 750)

KV = """
MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1
    MDLabel:
        text: "TEST WINDOW - IF YOU SEE THIS, KIVY IS WORKING"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
"""

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    TestApp().run()
