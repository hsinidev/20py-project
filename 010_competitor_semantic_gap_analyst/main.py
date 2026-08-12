import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import tksheet
import plotly.graph_objects as go
import xlsxwriter
from markdown_it import MarkdownIt
import random
import os
import sys
import webbrowser

# Metadata
__author__ = "HSINI MOHAMED"
__project__ = "Competitor Semantic Gap AI Analyst"

# Theme: Executive War-Room (Forest Green & Off-White)
FOREST_GREEN = "#1B5E20"
OFF_WHITE = "#FAFAFA"
TEXT_DARK = "#212121"
ACCENT_GOLD = "#C6A15B"

class GapAnalystEngine:
    def __init__(self):
        self.keywords = [
            "AI Infrastructure", "Neural Networks", "RAG Pipeline", "LLM Scaling", "Vector Databases", 
            "Semantic Search", "GEO Strategy", "Citation Authority", "Prompt Engineering", "Cloud GPU",
            "Transformer Architecture", "Attention Mechanism", "Data Privacy", "Ethical AI", "Model Quantization",
            "Fine-tuning", "Zero-shot Learning", "Few-shot Prompting", "Reinforcement Learning", "NLP Benchmarks"
        ]
        self.df = None

    def generate_mock_data(self):
        data = {
            "Keyword": self.keywords,
            "Search Volume": [random.randint(500, 50000) for _ in range(len(self.keywords))],
            "Our Brand": [random.randint(10, 95) for _ in range(len(self.keywords))],
            "Competitor A": [random.randint(30, 98) for _ in range(len(self.keywords))],
            "Competitor B": [random.randint(20, 92) for _ in range(len(self.keywords))],
            "Competitor C": [random.randint(15, 88) for _ in range(len(self.keywords))]
        }
        self.df = pd.DataFrame(data)
        return self.df

    def find_gaps(self):
        # A critical gap is where at least one competitor is > 70 and our brand is < 40
        if self.df is None: self.generate_mock_data()
        mask = ((self.df["Competitor A"] > 70) | (self.df["Competitor B"] > 70) | (self.df["Competitor C"] > 70)) & (self.df["Our Brand"] < 40)
        return self.df[mask]

    def generate_roadmap(self, gaps):
        roadmap = f"# ROADMAP TO SEMANTIC DOMINANCE\n"
        roadmap += f"**Strategic Framework for GEO Optimization**\n"
        roadmap += f"Author: {__author__} | System: {__project__}\n\n"
        
        roadmap += "## Executive Summary\n"
        roadmap += f"Analysis of industry-standard LLM responses identified **{len(gaps)} critical semantic gaps**. "
        roadmap += "Competitors currently hold high citation authority in these domains while our brand is semantically invisible.\n\n"
        
        roadmap += "## Actionable Content Briefs\n"
        for _, row in gaps.iterrows():
            best_comp = "Competitor A" if row["Competitor A"] > row["Competitor B"] else "Competitor B"
            roadmap += f"### TARGET TOPIC: {row['Keyword']}\n"
            roadmap += f"- **Deficit Analysis**: Currently lagging by {row[best_comp] - row['Our Brand']:.1f} percentage points behind {best_comp}.\n"
            roadmap += f"- **GEO Objective**: Inject high-fidelity technical whitepapers into search index to trigger RAG retrieval.\n"
            roadmap += f"- **Brief**: Produce a 2,000-word authoritative guide on '{row['Keyword']}' with structured data schema. Use specific technical entities favored by current SOTA models.\n\n"
            
        return roadmap

class WarRoomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{__project__} | EXECUTIVE TERMINAL")
        self.root.geometry("1200x850")
        self.root.configure(bg=OFF_WHITE)
        
        self.engine = GapAnalystEngine()
        self.df = self.engine.generate_mock_data()
        
        self.init_ui()

    def init_ui(self):
        # Header
        header = tk.Frame(self.root, bg=FOREST_GREEN, height=100)
        header.pack(fill=tk.X)
        
        title_box = tk.Frame(header, bg=FOREST_GREEN)
        title_box.pack(side=tk.LEFT, padx=30)
        
        tk.Label(title_box, text=__project__.upper(), fg=OFF_WHITE, bg=FOREST_GREEN, font=("Georgia", 24, "bold")).pack(anchor="w")
        tk.Label(title_box, text="STRATEGIC COMPETITIVE INTELLIGENCE DASHBOARD", fg=ACCENT_GOLD, bg=FOREST_GREEN, font=("Arial", 10)).pack(anchor="w")
        
        tk.Label(header, text=f"CLEARANCE: {__author__}\nSYSTEM: SECURE-PANDAS-V1", fg=OFF_WHITE, bg=FOREST_GREEN, font=("Consolas", 9), justify=tk.RIGHT).pack(side=tk.RIGHT, padx=30)
        
        # Dashboard Area
        dash = tk.Frame(self.root, bg=OFF_WHITE)
        dash.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left: Matrix
        left_p = tk.Frame(dash, bg=OFF_WHITE)
        left_p.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_p, text="■ COMPETITIVE SEMANTIC MATRIX", fg=FOREST_GREEN, bg=OFF_WHITE, font=("Arial", 12, "bold")).pack(anchor="nw")
        
        self.sheet = tksheet.Sheet(left_p, 
                                   data=self.df.values.tolist(), 
                                   headers=list(self.df.columns),
                                   theme="light green",
                                   height=500)
        self.sheet.enable_bindings()
        self.sheet.pack(fill=tk.BOTH, expand=True, pady=10)

        # Row Management (Add/Delete)
        row_mgmt = tk.Frame(left_p, bg=OFF_WHITE)
        row_mgmt.pack(fill=tk.X)
        
        tk.Button(row_mgmt, text="+ ADD RECORD (ROW)", command=self.add_row, bg=FOREST_GREEN, fg=OFF_WHITE, font=("Arial", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(row_mgmt, text="- DELETE ROW", command=self.delete_row, bg="#B71C1C", fg=OFF_WHITE, font=("Arial", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(row_mgmt, text="+ ADD COMPETITOR (COL)", command=self.add_col, bg=ACCENT_GOLD, fg=TEXT_DARK, font=("Arial", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(row_mgmt, text="- DELETE COL", command=self.delete_col, bg="#E57373", fg=TEXT_DARK, font=("Arial", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Right: Actions
        right_p = tk.Frame(dash, bg=OFF_WHITE, width=320)
        right_p.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        act_box = tk.LabelFrame(right_p, text=" STRATEGIC OPERATIONS ", font=("Arial", 10, "bold"), bg=OFF_WHITE, fg=FOREST_GREEN, padx=15, pady=15)
        act_box.pack(fill=tk.X)
        
        btn_cfg = {"bg": FOREST_GREEN, "fg": OFF_WHITE, "activebackground": ACCENT_GOLD, "font": ("Arial", 10, "bold"), "pady": 12, "bd": 0}
        
        tk.Button(act_box, text="GENERATE COMPETITIVE RADAR", command=self.do_radar, **btn_cfg).pack(fill=tk.X, pady=5)
        tk.Button(act_box, text="ISOLATE SEMANTIC GAPS", command=self.do_gaps, **btn_cfg).pack(fill=tk.X, pady=5)
        tk.Button(act_box, text="IMPORT CSV DATA", command=self.do_import, **btn_cfg).pack(fill=tk.X, pady=5)
        tk.Button(act_box, text="EXPORT EXECUTIVE XLS", command=self.do_xls, **btn_cfg).pack(fill=tk.X, pady=5)
        tk.Button(act_box, text="EXPORT CSV FILE", command=self.do_export_csv, **btn_cfg).pack(fill=tk.X, pady=5)
        tk.Button(act_box, text="GENERATE ROADMAP (MD)", command=self.do_md, **btn_cfg).pack(fill=tk.X, pady=5)
        
        # Log
        tk.Label(right_p, text="INTELLIGENCE FEED", fg=FOREST_GREEN, bg=OFF_WHITE, font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 5))
        self.log = tk.Text(right_p, bg="#111111", fg="#00FF66", font=("Consolas", 9), height=15)
        self.log.pack(fill=tk.BOTH, expand=True)
        self.write_log("War-Room System Initialized.")
        self.write_log(f"Monitoring {len(self.df)} core semantic vectors.")

    def write_log(self, text):
        self.log.insert(tk.END, f"> {text}\n")
        self.log.see(tk.END)

    def add_row(self):
        try:
            # Safely get column count
            col_count = self.sheet.total_columns()
            new_row_data = ["New Item"] + [0] * (col_count - 1)
            self.sheet.insert_row(row=new_row_data, redraw=True)
            self.write_log("New record skeleton added to matrix.")
        except Exception as e:
            self.write_log(f"Add Row Error: {e}")

    def add_col(self):
        try:
            # Add a new competitor column
            from tkinter import simpledialog
            col_name = simpledialog.askstring("New Column", "Enter Competitor Name:", parent=self.root)
            if col_name:
                row_count = self.sheet.total_rows()
                column_values = [0] * row_count
                # insert_column signature uses 'column' for data and 'idx' for position
                # and 'header' boolean? No, wait. 
                # (column=None, idx=None, width=None, header=False, ...)
                # Let's use idx = col_count to add at the end
                col_count = self.sheet.total_columns()
                self.sheet.insert_column(column=column_values, idx=col_count, redraw=True)
                # Set the header separately if needed, or if it takes a string?
                # Actually, some versions take header=True/False, 
                # let's try to set header data after
                self.sheet.set_header_data(column=col_count, value=col_name)
                self.sheet.redraw()
                self.write_log(f"Added new competitor: {col_name}")
        except Exception as e:
            self.write_log(f"Add Col Error: {e}")

    def delete_col(self):
        try:
            selected = self.sheet.get_selected_columns()
            if not selected:
                messagebox.showwarning("Selection Required", "Please click a column header to select it first.")
                return
            # selected is usually a set of column indices
            for col in reversed(sorted(list(selected))):
                if col == 0: continue # Don't delete the Keyword column
                self.sheet.delete_column(col, redraw=True)
            self.write_log(f"Removed {len(selected)} columns from matrix.")
        except Exception as e:
            self.write_log(f"Delete Col Error: {e}")

    def delete_row(self):
        try:
            selected = self.sheet.get_selected_rows()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a row to delete.")
                return
            for row in reversed(sorted(list(selected))):
                self.sheet.delete_row(row, redraw=True)
            self.write_log(f"Removed {len(selected)} records from matrix.")
        except Exception as e:
            self.write_log(f"Delete Row Error: {e}")

    def do_import(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if path:
            try:
                if path.endswith('.csv'):
                    new_df = pd.read_csv(path)
                else:
                    new_df = pd.read_excel(path)
                
                self.df = new_df
                self.sheet.set_sheet_data(self.df.values.tolist())
                self.sheet.set_column_headers(list(self.df.columns))
                self.write_log(f"Imported {len(self.df)} records from {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to load file: {e}")

    def do_export_csv(self):
        # Get current data from sheet
        data = self.sheet.get_sheet_data()
        headers = self.sheet.get_column_headers()
        export_df = pd.DataFrame(data, columns=headers)
        path = "Competitive_Matrix_Export.csv"
        export_df.to_csv(path, index=False)
        self.write_log(f"Matrix exported to CSV: {path}")
        messagebox.showinfo("Success", f"Data exported to {path}")

    def do_radar(self):
        self.write_log("Compiling Radar Chart Vectors...")
        # Take top 10 keywords for clarity
        sample = self.df.head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=sample["Our Brand"], theta=sample["Keyword"], fill='toself', name='Our Brand', fillcolor='rgba(27, 94, 32, 0.3)', line_color=FOREST_GREEN))
        fig.add_trace(go.Scatterpolar(r=sample["Competitor A"], theta=sample["Keyword"], fill='toself', name='Competitor A', line_color='#FF5252'))
        fig.add_trace(go.Scatterpolar(r=sample["Competitor B"], theta=sample["Keyword"], fill='toself', name='Competitor B', line_color='#448AFF'))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#DDDDDD")),
            showlegend=True,
            title=f"Executive Competitive Radar - {__author__}",
            paper_bgcolor=OFF_WHITE,
            plot_bgcolor=OFF_WHITE
        )
        
        path = os.path.abspath("semantic_radar.html")
        fig.write_html(path)
        webbrowser.open(f"file://{path}")
        self.write_log("Radar Chart rendered to browser-embedded view.")

    def do_gaps(self):
        self.write_log("Running NLP Gap Analysis...")
        gaps = self.engine.find_gaps()
        self.write_log(f"Found {len(gaps)} Strategic Vulnerabilities.")
        for _, row in gaps.iterrows():
            self.write_log(f"GAP DETECTED: {row['Keyword']}")

    def do_xls(self):
        path = "Executive_Semantic_Gap_Report.xlsx"
        try:
            with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
                self.df.to_excel(writer, sheet_name='Full Matrix', index=False)
                gaps = self.engine.find_gaps()
                gaps.to_excel(writer, sheet_name='Critical Gaps', index=False)
                
                workbook = writer.book
                header_fmt = workbook.add_format({'bold': True, 'bg_color': FOREST_GREEN, 'font_color': OFF_WHITE, 'border': 1})
                
                for sheet_name in ['Full Matrix', 'Critical Gaps']:
                    ws = writer.sheets[sheet_name]
                    for col_num, value in enumerate(self.df.columns.values):
                        ws.write(0, col_num, value, header_fmt)
            
            self.write_log(f"Executive XLS exported: {path}")
            messagebox.showinfo("Success", f"Multi-sheet Excel generated at {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_md(self):
        gaps = self.engine.find_gaps()
        roadmap = self.engine.generate_roadmap(gaps)
        path = "Dominance_Roadmap.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(roadmap)
        self.write_log(f"GEO Roadmap generated: {path}")
        messagebox.showinfo("Success", f"Roadmap to Dominance (Markdown) generated at {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WarRoomGUI(root)
    root.mainloop()
