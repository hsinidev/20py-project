import flet as ft
from ui.styles.clinical_theme import ClinicalTheme
from ui.views.dashboard import AuditDashboard

def main(page: ft.Page):
    # Apply Clinical Theme
    ClinicalTheme.apply(page)
    
    # Initialize UI
    dashboard = AuditDashboard(page)
    
    page.add(
        ft.AppBar(
            title=ft.Text("ENDPOINT SECURITY POLICY AUDITOR", color=ft.Colors.WHITE, weight="bold", size=16),
            bgcolor=ClinicalTheme.PRIMARY,
            center_title=False,
            actions=[
                ft.IconButton(ft.Icons.HISTORY, icon_color=ft.Colors.WHITE),
                ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE),
            ]
        ),
        dashboard
    )
    
    page.update()

if __name__ == "__main__":
    ft.run(main)
