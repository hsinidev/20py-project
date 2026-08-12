import flet as ft
from ui.styles.clinical_theme import ClinicalTheme
from ui.components.policy_check_list import PolicyCard
from engine.scanner_core import AuditScanner
import asyncio

class AuditDashboard(ft.Column):
    """
    Stateful Dashboard with Health Gauges and Audit Controls.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.scanner = AuditScanner()
        self.cards = {}

        # Gauge Components
        self.health_score = ft.Text("0%", size=45, weight="bold", color=ClinicalTheme.PRIMARY)
        self.compliance_bar = ft.ProgressBar(value=0, color=ClinicalTheme.PRIMARY, bgcolor=ft.Colors.GREY_200, height=10)
        
        self.init_ui()

    def init_ui(self):
        # Header Gauge Section
        gauge_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SHIELD_MOON, color=ClinicalTheme.PRIMARY, size=30),
                    ft.Text("SYSTEM COMPLIANCE HEALTH", weight="bold", size=16, color=ClinicalTheme.TEXT_SUB)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.health_score], alignment=ft.MainAxisAlignment.CENTER),
                self.compliance_bar,
                ft.Text("Overall Endpoint Security Score", size=12, color=ClinicalTheme.TEXT_SUB)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=30,
            bgcolor=ClinicalTheme.SURFACE,
            border_radius=20,
            margin=10
        )

        # Controls
        self.scan_btn = ft.ElevatedButton(
            "START SECURITY AUDIT", 
            icon=ft.Icons.PLAY_ARROW, 
            on_click=self.start_audit,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        
        self.profile_dropdown = ft.Dropdown(
            label="Audit Profile",
            options=[
                ft.dropdown.Option("workstation", "Standard Workstation"),
                ft.dropdown.Option("server", "Hardened Server")
            ],
            value="workstation",
            width=200
        )

        # Policy List
        self.policy_list = ft.ListView(expand=True, spacing=10, padding=10)

        self.controls = [
            gauge_container,
            ft.Container(
                content=ft.Row([self.profile_dropdown, self.scan_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10
            ),
            ft.Container(
                content=ft.Text("DETAILED POLICY CHECKS", weight="bold", size=14, color=ClinicalTheme.TEXT_SUB),
                padding=10
            ),
            self.policy_list
        ]
        self.expand = True

    async def start_audit(self, e):
        self.scan_btn.disabled = True
        self.policy_list.controls.clear()
        self.cards = {}
        self.health_score.value = "0%"
        self.compliance_bar.value = 0
        self.update()

        self.scanner = AuditScanner(profile=self.profile_dropdown.value)
        policies = self.scanner.policies
        
        # Initialize Cards
        for p in policies:
            card = PolicyCard(p["name"], p["description"], on_remediate=lambda x, p=p: self.remediate(p))
            self.cards[p["id"]] = card
            self.policy_list.controls.append(card)
        self.update()

        # Run Scan
        passed = 0
        total = len(policies)
        
        def on_progress(result, progress):
            nonlocal passed
            card = self.cards[result["id"]]
            card.update_status(result)
            if result["status"] == "PASS":
                passed += 1
            
            score = int((passed / total) * 100)
            self.health_score.value = f"{score}%"
            self.compliance_bar.value = progress
            self.update()

        await self.scanner.scan_all(progress_callback=on_progress)
        self.scan_btn.disabled = False
        self.update()

    def remediate(self, policy):
        # Open a bottom sheet or dialog with the script
        def close_bs(e):
            bs.open = False
            self._page.update()

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column([
                    ft.Text("REMEDIATION STEPS", weight="bold", size=18, color=ClinicalTheme.DANGER),
                    ft.Divider(),
                    ft.Text(f"Target: {policy['name']}", weight="bold"),
                    ft.Container(
                        content=ft.Text(policy['remediation'], font_family="monospace", color=ft.Colors.BLUE_GREY_900),
                        bgcolor=ft.Colors.GREY_100,
                        padding=15,
                        border_radius=5
                    ),
                    ft.Text("Run the above command in PowerShell as Administrator.", size=12, italic=True),
                    ft.ElevatedButton("Close", on_click=close_bs)
                ], tight=True, spacing=20),
                padding=30
            ),
            open=True
        )
        self._page.overlay.append(bs)
        self._page.update()
