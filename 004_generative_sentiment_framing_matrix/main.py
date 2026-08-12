import os
import threading
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from core.classifier import FramingClassifier
from core.matrix import SentimentMatrix

Window.size = (1100, 750)

KV = """
MDScreen:
    md_bg_color: [0.1, 0.1, 0.1, 1]

    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        # Header
        BoxLayout:
            size_hint_y: None
            height: "60dp"
            spacing: "10dp"
            
            MDIcon:
                icon: "matrix"
                theme_text_color: "Custom"
                text_color: [0.7, 0.6, 0.85, 1]
                font_size: "32sp"
            
            MDLabel:
                text: "GENERATIVE SENTIMENT & FRAMING MATRIX"
                theme_text_color: "Custom"
                text_color: [0.9, 0.9, 0.9, 1]
                font_style: "H6"
                bold: True
            
            MDLabel:
                text: "HSINI MOHAMED"
                halign: "right"
                theme_text_color: "Hint"
                font_style: "Caption"

        BoxLayout:
            spacing: "20dp"

            # Left Panel
            BoxLayout:
                orientation: "vertical"
                size_hint_x: 0.4
                spacing: "15dp"

                MDLabel:
                    text: "Brand / Entity Analysis"
                    theme_text_color: "Custom"
                    text_color: [0.7, 0.6, 0.85, 1]
                    font_style: "Subtitle2"

                MDTextField:
                    id: brand_name
                    hint_text: "Brand Name"
                    mode: "fill"
                    fill_color_normal: [0.15, 0.15, 0.15, 1]

                MDTextField:
                    id: input_text
                    hint_text: "LLM Response Text"
                    multiline: True
                    mode: "fill"
                    fill_color_normal: [0.15, 0.15, 0.15, 1]
                    size_hint_y: 0.6

                MDRaisedButton:
                    text: "ANALYZE FRAMING"
                    md_bg_color: [0.7, 0.6, 0.85, 1]
                    size_hint_x: 1
                    on_release: app.analyze_text()

                MDLabel:
                    id: status_log
                    text: "Ready for analysis..."
                    theme_text_color: "Hint"
                    font_style: "Caption"
                    size_hint_y: None
                    height: "40dp"

            # Right Panel
            BoxLayout:
                orientation: "vertical"
                spacing: "15dp"

                BoxLayout:
                    size_hint_y: None
                    height: "100dp"
                    spacing: "15dp"

                    MDCard:
                        padding: "12dp"
                        md_bg_color: [0.15, 0.15, 0.15, 1]
                        elevation: 0
                        radius: 12
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "SENTIMENT"
                                theme_text_color: "Hint"
                                font_style: "Caption"
                            MDLabel:
                                id: sentiment_val
                                text: "0.00"
                                font_style: "H4"

                    MDCard:
                        padding: "12dp"
                        md_bg_color: [0.15, 0.15, 0.15, 1]
                        elevation: 0
                        radius: 12
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "FRAMING"
                                theme_text_color: "Hint"
                                font_style: "Caption"
                            MDLabel:
                                id: framing_val
                                text: "None"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: [0.7, 0.6, 0.85, 1]

                MDCard:
                    md_bg_color: [0.15, 0.15, 0.15, 1]
                    elevation: 0
                    radius: 12
                    padding: "20dp"
                    BoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        MDLabel:
                            text: "3D VISUALIZATION ENGINE"
                            halign: "center"
                            theme_text_color: "Hint"
                        MDIconButton:
                            icon: "cube-outline"
                            pos_hint: {"center_x": .5}
                            user_font_size: "64sp"
                            theme_text_color: "Custom"
                            text_color: [0.7, 0.6, 0.85, 1]
                            on_release: app.open_matrix()
                        MDLabel:
                            text: "Click to generate 3D Matrix in Browser"
                            halign: "center"
                            theme_text_color: "Hint"
                            font_style: "Caption"

                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "120dp"
                    spacing: "10dp"
                    MDLabel:
                        text: "Tone-Shift Simulator (Temperature Adjustment)"
                        font_style: "Caption"
                        theme_text_color: "Hint"
                    MDSlider:
                        id: temp_slider
                        min: 0
                        max: 2
                        value: 0.7
                        color: [0.7, 0.6, 0.85, 1]
                    MDLabel:
                        text: "Current Temperature: {:.2f}".format(temp_slider.value)
                        halign: "center"
                        font_style: "Caption"
"""

class FramingMatrixApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        self.classifier = None
        self.matrix = SentimentMatrix()
        
        Clock.schedule_once(self.load_nlp, 1)
        return Builder.load_string(KV)

    def load_nlp(self, *args):
        def _load():
            self.root.ids.status_log.text = "Loading NLP Models (DistilBERT)..."
            self.classifier = FramingClassifier()
            self.root.ids.status_log.text = "NLP Engine Ready."
        threading.Thread(target=_load, daemon=True).start()

    def analyze_text(self):
        if not self.classifier:
            self.root.ids.status_log.text = "[!] Engine not ready. Please wait."
            return
        brand = self.root.ids.brand_name.text
        text = self.root.ids.input_text.text
        
        if not brand or not text:
            self.root.ids.status_log.text = "[!] Error: Missing input."
            return

        res = self.classifier.analyze(text)
        
        self.root.ids.sentiment_val.text = "{:+.2f}".format(res.score)
        self.root.ids.framing_val.text = res.framing
        
        authority = 0.5 + (res.confidence * 0.4)
        self.matrix.add_point(brand, res.score, authority, res.framing)
        
        self.root.ids.status_log.text = "[OK] Analyzed {}: {}".format(brand, res.framing)

    def open_matrix(self):
        if not self.matrix.data:
            self.root.ids.status_log.text = "[!] Error: No data points collected."
            return
        self.matrix.render_3d()
        self.root.ids.status_log.text = "[OK] 3D Matrix opened in browser."

if __name__ == "__main__":
    FramingMatrixApp().run()
