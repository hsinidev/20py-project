import flet as ft

class ClinicalTheme:
    """
    Clinical-Blue Theme for the Policy Auditor.
    """
    PRIMARY = "#0078D7"
    BG = "#F0F4F8"
    SURFACE = "#FFFFFF"
    DANGER = "#D32F2F"
    SUCCESS = "#388E3C"
    TEXT_MAIN = "#2C3E50"
    TEXT_SUB = "#7F8C8D"

    @staticmethod
    def apply(page: ft.Page):
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ClinicalTheme.BG
        page.window_title_bar_hidden = False
        page.fonts = {
            "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit-VariableFont_wght.ttf"
        }
        page.theme = ft.Theme(
            color_scheme_seed=ClinicalTheme.PRIMARY,
            visual_density=ft.VisualDensity.COMFORTABLE
        )
