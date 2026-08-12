import flet as ft
from ui.styles.clinical_theme import ClinicalTheme

class PolicyCard(ft.Container):
    """
    Reactive card for individual policy status.
    """
    def __init__(self, policy_name, description, on_remediate=None):
        super().__init__()
        self.policy_name = policy_name
        self.description = description
        self.on_remediate = on_remediate
        
        self.status_icon = ft.Icon(ft.Icons.PENDING, color=ft.Colors.GREY_400)
        self.status_text = ft.Text("Waiting...", size=12, italic=True)
        self.remediate_btn = ft.ElevatedButton(
            "ONE-CLICK REMEDIATE", 
            on_click=self.on_remediate,
            visible=False,
            style=ft.ButtonStyle(bgcolor=ClinicalTheme.DANGER, color=ft.Colors.WHITE)
        )

        self.content = ft.Row([
            ft.Container(
                self.status_icon,
                padding=10,
                border_radius=50,
                bgcolor=ft.Colors.GREY_100
            ),
            ft.Column([
                ft.Text(self.policy_name, weight="bold", size=16, color=ClinicalTheme.TEXT_MAIN),
                ft.Text(self.description, size=13, color=ClinicalTheme.TEXT_SUB),
                self.status_text,
                self.remediate_btn
            ], expand=True, spacing=5)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self.padding = 15
        self.margin = 5
        self.bgcolor = ClinicalTheme.SURFACE
        self.border_radius = 12
        self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))

    def update_status(self, result):
        if result["status"] == "PASS":
            self.status_icon.name = ft.Icons.CHECK_CIRCLE
            self.status_icon.color = ClinicalTheme.SUCCESS
            self.status_text.value = "PASSED: Compliant"
            self.status_text.color = ClinicalTheme.SUCCESS
            self.remediate_btn.visible = False
        else:
            self.status_icon.name = ft.Icons.ERROR_OUTLINE
            self.status_icon.color = ClinicalTheme.DANGER
            self.status_text.value = "FAILED: Non-Compliant"
            self.status_text.color = ClinicalTheme.DANGER
            self.remediate_btn.visible = True
        self.update()
