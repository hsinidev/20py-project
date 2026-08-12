import flet as ft
import asyncio
from core.engine import PersonaEngine
from core.analysis import BiasAnalyzer
from core.models import COLORS

class PersonaBiasApp:
    def __init__(self):
        self.engine = PersonaEngine()
        self.analyzer = BiasAnalyzer()

    async def main(self, page: ft.Page):
        self.page = page
        page.title = "CROSS-MODEL PERSONA BIAS SIMULATOR | HSINI MOHAMED"
        page.bgcolor = COLORS["bg"]
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.window_width = 1200
        page.window_height = 900

        # -- Inputs & Config --
        self.openai_key = ft.TextField(label="OpenAI Key", password=True, can_reveal_password=True, text_size=12, expand=True)
        self.gemini_key = ft.TextField(label="Gemini Key", password=True, can_reveal_password=True, text_size=12, expand=True)
        
        self.cloud_model_dropdown = ft.Dropdown(
            label="CLOUD MODEL",
            options=[
                ft.dropdown.Option("gpt-4o"),
                ft.dropdown.Option("gemini-1.5-pro"),
                ft.dropdown.Option("gemini-1.5-flash"),
                ft.dropdown.Option("gemini-pro"),
            ],
            value="gpt-4o",
            width=150
        )
        
        self.ollama_dropdown = ft.Dropdown(
            label="LOCAL MODEL",
            options=[],
            width=150,
            border_color=COLORS["burgundy"]
        )
        
        self.enable_local = ft.Switch(label="LOCAL", value=True, active_color=COLORS["burgundy"], on_change=lambda _: self.on_toggle_change())
        self.enable_cloud = ft.Switch(label="CLOUD", value=True, active_color=COLORS["accent"], on_change=lambda _: self.on_toggle_change())
        
        self.persona_a = ft.TextField(label="PERSONA A", value="Conservative CFO", border_color=COLORS["burgundy"], expand=True)
        self.persona_b = ft.TextField(label="PERSONA B", value="Gen-Z Techie", border_color=COLORS["accent"], expand=True)
        self.prompt_input = ft.TextField(label="ENTER UNIVERSAL PROMPT", multiline=True, min_lines=3, expand=True)

        # -- Results --
        self.output_a_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.output_b_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.output_a_container.controls = [ft.Text("Ollama Response...", color="white60")]
        self.output_b_container.controls = [ft.Text("Cloud Response...", color=COLORS["accent"])]

        self.divergence_bar = ft.ProgressBar(value=0, color=COLORS["burgundy"], bgcolor="white24", height=10)
        self.divergence_text = ft.Text("DIVERGENCE: 0%", size=14, weight="bold")
        
        self.heatmap_row = ft.Row(wrap=True, spacing=5)

        # -- UI Sections --
        header = ft.Container(
            content=ft.Row([
                ft.Text("PERSONA BIAS SIMULATOR", size=24, color="white", weight="bold"),
                ft.Text("HSINI MOHAMED", size=12, color="white60"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=COLORS["burgundy"],
            padding=20,
        )

        config_panel = ft.Container(
            content=ft.Row([
                self.openai_key,
                self.gemini_key,
                ft.Column([self.enable_local, self.enable_cloud], spacing=0),
                self.ollama_dropdown,
                self.cloud_model_dropdown,
                ft.FilledButton("REFRESH", icon="refresh", on_click=self.load_models)
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(left=20, right=20, top=10, bottom=10),
            bgcolor="white",
            border=ft.Border(bottom=ft.BorderSide(1, COLORS["warm_grey"]))
        )

        input_panel = ft.Container(
            content=ft.Column([
                ft.Row([self.persona_a, self.persona_b], spacing=20),
                self.prompt_input,
                ft.Row([
                    ft.FilledButton(
                        "EXECUTE A/B BIAS ANALYSIS",
                        style=ft.ButtonStyle(bgcolor=COLORS["burgundy"], color="white"),
                        on_click=self.run_analysis,
                        height=50,
                        expand=True
                    ),
                    ft.FilledButton(
                        "RESET",
                        on_click=self.reset_ui,
                        height=50,
                        style=ft.ButtonStyle(color=COLORS["burgundy"])
                    )
                ])
            ]),
            padding=20
        )

        # Static Comparison Containers
        self.icon_a = ft.Icon("check_circle", color="white")
        self.icon_b = ft.Icon("check_circle", color=COLORS["accent"])

        self.container_a = ft.Container(
            content=self.output_a_container,
            bgcolor=COLORS["panel_a"],
            padding=20,
            expand=True,
            border_radius=15,
            border=ft.Border.all(2, "white24"),
        )
        
        self.container_b = ft.Container(
            content=self.output_b_container,
            bgcolor=COLORS["panel_b"],
            padding=20,
            expand=True,
            border_radius=15,
            border=ft.Border.all(2, COLORS["accent"]),
        )

        self.latency_text = ft.Text("", size=10, color="grey500")
        heatmap_panel = ft.Container(
            content=ft.Column([
                ft.Row([self.divergence_text, ft.Text("Semantic Heatmap Salience", size=12, color=COLORS["accent"])]),
                self.divergence_bar,
                ft.Row([
                    ft.Text("Trigger Keywords Detected:", size=11, weight="bold"),
                    self.latency_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.heatmap_row
            ]),
            padding=20,
            bgcolor="white",
            border=ft.Border.all(1, COLORS["warm_grey"]),
            border_radius=10
        )

        # Layout Assembly
        page.add(
            ft.Column([
                header,
                config_panel,
                input_panel,
                ft.Row([self.container_a, self.container_b], expand=True, spacing=10),
                heatmap_panel
            ], expand=True)
        )

        self.on_toggle_change() 
        await self.load_models(None)

    def on_toggle_change(self):
        self.container_a.opacity = 1.0 if self.enable_local.value else 0.3
        self.container_a.bgcolor = COLORS["panel_a"] if self.enable_local.value else "black26"
        self.icon_a.name = "check_circle" if self.enable_local.value else "cancel"
        
        self.container_b.opacity = 1.0 if self.enable_cloud.value else 0.3
        self.container_b.bgcolor = COLORS["panel_b"] if self.enable_cloud.value else "black12"
        self.icon_b.name = "check_circle" if self.enable_cloud.value else "cancel"
        self.page.update()

    async def load_models(self, e):
        models = self.engine.list_local_models()
        self.ollama_dropdown.options = [ft.dropdown.Option(m) for m in models]
        if models: self.ollama_dropdown.value = models[0]
        else: self.ollama_dropdown.hint_text = "No models found"
        self.page.update()

    def reset_ui(self, e):
        self.prompt_input.value = ""
        self.output_a_container.controls = [ft.Text("Ollama Response...", color="white60")]
        self.output_b_container.controls = [ft.Text("Cloud Response...", color=COLORS["accent"])]
        self.divergence_bar.value = 0
        self.divergence_text.value = "DIVERGENCE: 0%"
        self.latency_text.value = ""
        self.heatmap_row.controls.clear()
        self.page.update()

    def highlight_text(self, text, keywords, base_color="white"):
        import re
        if not text: return ft.Text("")
        
        spans = []
        # Create regex for all keywords
        pattern = "|".join([re.escape(k) for k in keywords])
        last_idx = 0
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Text before match
            spans.append(ft.TextSpan(text[last_idx:match.start()], style=ft.TextStyle(color=base_color)))
            # Highlighted keyword
            spans.append(ft.TextSpan(
                match.group(),
                style=ft.TextStyle(
                    weight="bold", 
                    bgcolor=COLORS["burgundy"] if base_color == "white" else COLORS["accent"],
                    color="white" if base_color == "white" else "black"
                )
            ))
            last_idx = match.end()
            
        spans.append(ft.TextSpan(text[last_idx:], style=ft.TextStyle(color=base_color)))
        return ft.Text(spans=spans, size=14, selectable=True)

    async def run_analysis(self, e):
        prompt = self.prompt_input.value
        if not prompt:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter a universal prompt to begin analysis!"), bgcolor=COLORS["burgundy"])
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        e.control.disabled = True
        e.control.text = "PROMPTING (Waiting for Ollama)..." if self.enable_local.value else "PROMPTING CLOUD..."
        self.page.update()

        tasks = []
        if self.enable_local.value:
            tasks.append(self.engine.get_ollama_response(self.persona_a.value, prompt, self.ollama_dropdown.value))
        else:
            tasks.append(asyncio.sleep(0, result={"text": "LOCAL COMPONENT DISABLED", "source": "None"}))

        if self.enable_cloud.value:
            provider = "openai" if self.openai_key.value else "gemini"
            key = self.openai_key.value or self.gemini_key.value
            
            # Auto-correct model if user selected incompatible provider
            current_model = self.cloud_model_dropdown.value
            if provider == "openai" and "gemini" in current_model:
                current_model = "gpt-4o"
            elif provider == "gemini" and "gpt" in current_model:
                current_model = "gemini-1.5-flash"
                
            tasks.append(self.engine.get_cloud_response(self.persona_b.value, prompt, provider, key, current_model))
        else:
            tasks.append(asyncio.sleep(0, result={"text": "CLOUD COMPONENT DISABLED", "source": "None"}))

        results = await asyncio.gather(*tasks)
        res_a, res_b = results[0], results[1]
        
        self.output_a_container.controls = [self.highlight_text(res_a["text"], ["risk", "profit", "innovative", "growth", "security", "digital", "traditional", "equity"], "white")]
        self.output_b_container.controls = [self.highlight_text(res_b["text"], ["risk", "profit", "innovative", "growth", "security", "digital", "traditional", "equity"], COLORS["text"])]
        
        total_latency = (res_a.get("latency", 0) + res_b.get("latency", 0)) / 2
        self.latency_text.value = f"Avg Latency: {total_latency:.2f}s"
        
        # Analysis results visibility (Only run if both models responded successfully)
        is_error_a = any(x in res_a["text"] for x in ["Error", "Timeout", "Missing"])
        is_error_b = any(x in res_b["text"] for x in ["Error", "Timeout", "Missing"])
        
        if (self.enable_local.value and self.enable_cloud.value) and not (is_error_a or is_error_b):
            e.control.text = "VECTORIZING RESPONSES..."
            self.page.update()
            
            # Run blocking calculation in thread
            divergence = await asyncio.to_thread(self.analyzer.calculate_divergence, res_a["text"], res_b["text"])
            self.divergence_bar.value = divergence
            self.divergence_text.value = f"SEMANTIC DIVERGENCE: {divergence*100:.1f}%"
        else:
            self.divergence_bar.value = 0
            self.divergence_text.value = "ANALYSIS PAUSED: Waiting for valid dual response"
            salience = {}
            if not (is_error_a and is_error_b): # If at least one worked, show keywords for that one
                combined_text = res_a["text"] if not is_error_a else res_b["text"]
                keywords = ["risk", "profit", "innovative", "growth", "security", "digital", "traditional", "equity"]
                salience = await asyncio.to_thread(self.analyzer.get_heatmap_data, combined_text, keywords)
            
            self.heatmap_row.controls.clear()
            for kw, count in salience.items():
                if count > 0:
                    intensity = min(count * 50, 255)
                    self.heatmap_row.controls.append(
                        ft.Container(
                            content=ft.Text(kw.upper(), size=10, weight="bold", color="white"),
                            bgcolor=f"#FF{intensity:02x}40",
                            padding=5,
                            border_radius=5
                        )
                    )
        
        e.control.disabled = False
        e.control.text = "EXECUTE A/B BIAS ANALYSIS"
        self.page.update()

if __name__ == "__main__":
    app_instance = PersonaBiasApp()
    ft.app(target=app_instance.main)
