import wx
import textstat
import nltk
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, ne_chunk
import sys

# Metadata
__author__ = "HSINI MOHAMED"
__project__ = "Featured-Snippet Neural Optimizer"

class OptimizerEngine:
    def __init__(self):
        self.offline_mode = False
        try:
            nltk.data.find('tokenizers/punkt')
        except (LookupError, Exception):
            self.offline_mode = True

    def deconstruct(self, text):
        if self.offline_mode:
            # Simple sentence splitting fallback
            import re
            sentences = re.split(r'(?<=[.!?]) +', text)
            return [s.strip() for s in sentences if s.strip()]
        try:
            return sent_tokenize(text)
        except:
            import re
            sentences = re.split(r'(?<=[.!?]) +', text)
            return [s.strip() for s in sentences if s.strip()]

    def rewrite_gemini(self, text):
        sentences = self.deconstruct(text)
        steps = [f"Step {i+1}: {s}" for i, s in enumerate(sentences)]
        header = "### Optimized Actionable Steps (Gemini Preferred Structure)\n\n"
        return header + "\n".join(steps)

    def rewrite_perplexity(self, text):
        sentences = self.deconstruct(text)
        if not sentences: return ""
        summary = " ".join(sentences[:3])
        header = "### Concise Neural Fact (Perplexity Preferred Structure)\n\n"
        return header + summary + " [Verified Source]"

    def calculate_geo_score(self, text):
        if not text.strip():
            return 0
        
        # 1. Readability Score (TextStat fallback)
        try:
            readability = textstat.flesch_reading_ease(text)
        except:
            # Simple fallback: average word length / sentence length
            words = text.split()
            sentences = self.deconstruct(text)
            if not sentences or not words: return 0
            avg_word_len = sum(len(w) for w in words) / len(words)
            avg_sent_len = len(words) / len(sentences)
            # Rough approximation of Flesch Reading Ease
            readability = 206.835 - (1.015 * avg_sent_len) - (84.6 * (avg_word_len / 5))
            
        r_score = max(0, min(100, readability))
        
        # 2. Entity Density
        words = text.split()
        entities = sum(1 for w in words if w and w[0].isupper() and len(w) > 1)
        e_density = (entities / len(words)) * 100 if len(words) > 0 else 0
        e_score = min(100, e_density * 10)
        
        # 3. Fact Count (Numbers + Capitalized Words)
        num_count = sum(1 for w in words if any(c.isdigit() for c in w))
        fact_score = min(100, (entities + num_count) * 4)
        
        final_score = (r_score * 0.4) + (e_score * 0.3) + (fact_score * 0.3)
        return int(final_score)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=__project__, size=(1200, 850))
        self.engine = OptimizerEngine()
        self.init_ui()
        self.Centre()

    def init_ui(self):
        # Agency-Modern Palette: Deep Navy and Electric Blue
        self.navy = wx.Colour(2, 12, 48)
        self.electric_blue = wx.Colour(0, 229, 255)
        self.dark_bg = wx.Colour(5, 5, 25)
        self.white = wx.Colour(255, 255, 255)
        
        self.SetBackgroundColour(self.dark_bg)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- TOP HEADER ---
        header = wx.Panel(self)
        header.SetBackgroundColour(self.navy)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        title = wx.StaticText(header, label=__project__.upper())
        title.SetFont(wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(self.electric_blue)
        
        h_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 25)
        h_sizer.AddStretchSpacer()
        
        meta_info = wx.StaticText(header, label=f"V1.0 | AGENTIC OPTIMIZER | BY {__author__}")
        meta_info.SetForegroundColour(wx.Colour(100, 100, 150))
        h_sizer.Add(meta_info, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 25)
        
        header.SetSizer(h_sizer)
        main_sizer.Add(header, 0, wx.EXPAND)
        
        # --- MIDDLE CONTENT ---
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # LEFT: INPUT (BEFORE)
        left_panel = wx.Panel(self)
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        
        l_label = wx.StaticText(left_panel, label="SOURCE CONTENT (ATOMIC DECONSTRUCTION TARGET)")
        l_label.SetForegroundColour(self.electric_blue)
        l_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l_sizer.Add(l_label, 0, wx.TOP | wx.LEFT, 15)
        
        self.input_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE)
        self.input_text.SetBackgroundColour(wx.Colour(10, 15, 35))
        self.input_text.SetForegroundColour(self.electric_blue)
        self.input_text.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.input_text.SetValue("Neural optimization refers to the process of refining content so that AI search engines like Gemini and Perplexity can easily extract and display facts. Atomic deconstruction breaks paragraphs into core propositions. This increases the chances of winning the Featured Snippet position on Google.")
        l_sizer.Add(self.input_text, 1, wx.EXPAND | wx.ALL, 15)
        
        left_panel.SetSizer(l_sizer)
        content_sizer.Add(left_panel, 1, wx.EXPAND)
        
        # CENTER: CONTROLS
        ctrl_panel = wx.Panel(self)
        ctrl_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.opt_btn = wx.Button(ctrl_panel, label="EXECUTE NEURAL OPTIMIZATION", size=(-1, 60))
        self.opt_btn.SetBackgroundColour(self.electric_blue)
        self.opt_btn.SetForegroundColour(self.navy)
        self.opt_btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.opt_btn.Bind(wx.EVT_BUTTON, self.on_optimize)
        ctrl_sizer.Add(self.opt_btn, 0, wx.EXPAND | wx.TOP, 15)
        
        mode_label = wx.StaticText(ctrl_panel, label="STRUCTURE PREFERENCE")
        mode_label.SetForegroundColour(wx.Colour(150, 150, 200))
        ctrl_sizer.Add(mode_label, 0, wx.TOP | wx.ALIGN_CENTER, 20)
        
        self.mode_choice = wx.Choice(ctrl_panel, choices=["Gemini (Step-by-step)", "Perplexity (Concise Fact)"])
        self.mode_choice.SetSelection(0)
        ctrl_sizer.Add(self.mode_choice, 0, wx.EXPAND | wx.TOP, 5)
        
        ctrl_sizer.AddSpacer(40)
        
        score_title = wx.StaticText(ctrl_panel, label="GEO CONFIDENCE SCORE")
        score_title.SetForegroundColour(self.white)
        ctrl_sizer.Add(score_title, 0, wx.ALIGN_CENTER)
        
        self.score_gauge = wx.Gauge(ctrl_panel, range=100, size=(-1, 20))
        ctrl_sizer.Add(self.score_gauge, 0, wx.EXPAND | wx.TOP, 5)
        
        self.score_text = wx.StaticText(ctrl_panel, label="0%")
        self.score_text.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.score_text.SetForegroundColour(self.electric_blue)
        ctrl_sizer.Add(self.score_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        ctrl_sizer.AddStretchSpacer()
        
        self.export_btn = wx.Button(ctrl_panel, label="EXPORT SEMANTIC HTML5")
        self.export_btn.Bind(wx.EVT_BUTTON, self.on_export)
        ctrl_sizer.Add(self.export_btn, 0, wx.EXPAND | wx.BOTTOM, 15)
        
        ctrl_panel.SetSizer(ctrl_sizer)
        content_sizer.Add(ctrl_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # RIGHT: OUTPUT (AFTER)
        right_panel = wx.Panel(self)
        r_sizer = wx.BoxSizer(wx.VERTICAL)
        
        r_label = wx.StaticText(right_panel, label="NEURAL-OPTIMIZED OUTPUT (COMPARISON)")
        r_label.SetForegroundColour(self.electric_blue)
        r_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        r_sizer.Add(r_label, 0, wx.TOP | wx.LEFT, 15)
        
        self.output_text = wx.TextCtrl(right_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.output_text.SetBackgroundColour(wx.Colour(10, 15, 35))
        self.output_text.SetForegroundColour(self.electric_blue)
        self.output_text.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        r_sizer.Add(self.output_text, 1, wx.EXPAND | wx.ALL, 15)
        
        right_panel.SetSizer(r_sizer)
        content_sizer.Add(right_panel, 1, wx.EXPAND)
        
        main_sizer.Add(content_sizer, 1, wx.EXPAND)
        
        # --- FOOTER ---
        footer = wx.Panel(self)
        footer.SetBackgroundColour(wx.Colour(10, 10, 30))
        f_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status = wx.StaticText(footer, label="Ready for Atomic Paragraph Deconstruction...")
        status.SetForegroundColour(wx.Colour(100, 100, 100))
        f_sizer.Add(status, 0, wx.ALL, 10)
        footer.SetSizer(f_sizer)
        main_sizer.Add(footer, 0, wx.EXPAND)
        
        self.SetSizer(main_sizer)

    def on_optimize(self, event):
        text = self.input_text.GetValue()
        if not text.strip():
            wx.MessageBox("Please enter source content first.", "Empty Input", wx.ICON_WARNING)
            return
            
        mode = self.mode_choice.GetSelection()
        if mode == 0:
            optimized = self.engine.rewrite_gemini(text)
        else:
            optimized = self.engine.rewrite_perplexity(text)
            
        self.output_text.SetValue(optimized)
        
        score = self.engine.calculate_geo_score(optimized)
        self.score_gauge.SetValue(score)
        self.score_text.SetLabel(f"{score}%")
        
        if score > 80:
            self.score_text.SetForegroundColour(wx.Colour(0, 255, 100))
        elif score > 50:
            self.score_text.SetForegroundColour(self.electric_blue)
        else:
            self.score_text.SetForegroundColour(wx.Colour(255, 100, 100))

    def on_export(self, event):
        content = self.output_text.GetValue()
        if not content.strip():
            wx.MessageBox("Generate optimized content before exporting.", "No Content", wx.ICON_ERROR)
            return
            
        html_content = content.replace('\n', '<br>').replace('###', '<h2>').replace('Steps:', '</h2><ul>').replace('Step', '<li>Step').replace('Fact:', '</h2><p>').strip()
        if '<li>' in html_content: html_content += '</ul>'
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Optimized Featured Snippet by {__project__}">
    <meta name="author" content="{__author__}">
    <title>Neural Optimized Snippet</title>
    <style>
        :root {{ --navy: #020c30; --blue: #00e5ff; --white: #ffffff; }}
        body {{ font-family: 'Inter', sans-serif; background: #050519; color: var(--white); line-height: 1.8; padding: 40px; }}
        article {{ max-width: 900px; margin: auto; background: var(--navy); padding: 40px; border-radius: 20px; border: 1px solid rgba(0, 229, 255, 0.2); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
        h1 {{ color: var(--blue); font-size: 2.5rem; border-bottom: 2px solid var(--blue); padding-bottom: 10px; }}
        h2 {{ color: var(--blue); margin-top: 30px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: rgba(255,255,255,0.05); margin: 10px 0; padding: 15px; border-radius: 8px; border-left: 4px solid var(--blue); }}
        footer {{ margin-top: 50px; font-size: 0.8rem; color: #667; text-align: center; border-top: 1px solid #223; padding-top: 20px; }}
        .score {{ display: inline-block; padding: 5px 15px; background: var(--blue); color: var(--navy); border-radius: 20px; font-weight: bold; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <article>
        <div class="score">GEO CONFIDENCE: {self.score_text.GetLabel()}</div>
        <h1>Featured Snippet Optimization</h1>
        <section>
            {html_content}
        </section>
        <footer>
            &copy; 2026 {__author__} | Built with {__project__} Neural Engine
        </footer>
    </article>
</body>
</html>"""
        
        save_path = os.path.join(os.getcwd(), "optimized_snippet.html")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html_template)
            
        wx.MessageBox(f"Exported to Semantic HTML5 successful!\nPath: {save_path}", "Export Success", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    # Ensure NLTK resources are available if possible
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
