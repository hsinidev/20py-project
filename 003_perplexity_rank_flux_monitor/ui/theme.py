import dearpygui.dearpygui as dpg
from core.models import COLORS

def setup_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COLORS["bg"])
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COLORS["bg"])
            dpg.add_theme_color(dpg.mvThemeCol_Border, COLORS["grey"])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (25, 25, 25, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (35, 35, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, COLORS["green"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 200, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (40, 40, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, COLORS["green"])
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (20, 20, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, COLORS["green"])
            
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)

    dpg.bind_theme(global_theme)

def setup_fonts():
    with dpg.font_registry():
        # Fallback to system fonts or embedded ones if possible
        pass
