import customtkinter as ctk
import os
import sys
from datetime import datetime

# Local Imports
from engine.framework_manager import FrameworkManager
from ui.charts_integration import ComplianceGauge
from reports.generator import ReportGenerator
from tkinter import messagebox

class ComplianceAuditApp(ctk.CTk):
    """
    Automated Compliance Audit Suite - Executive GRC Edition.
    Developed by HSINI MOHAMED.
    """
    def __init__(self):
        super().__init__()
        self.title("Automated Compliance Audit Suite - HSINI MOHAMED")
        self.geometry("1280x800")
        
        # Theme Configuration
        ctk.set_appearance_mode("dark")
        self.primary_color = "#87A96B"
        self.bg_color = "#1A1C1E"
        self.surface_color = "#2D3135"
        self.accent_color = "#D4AF37"

        # State
        self.framework = FrameworkManager(os.path.join("data", "frameworks", "iso27001.yaml"))
        self.report_gen = ReportGenerator()
        self.current_step = 1
        self.stepper_labels = []
        
        self.init_ui()

    def init_ui(self):
        self.configure(fg_color=self.bg_color)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Top Header & Stepper
        self.header_frame = ctk.CTkFrame(self, fg_color=self.surface_color, height=120, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 10))
        
        header_title = ctk.CTkLabel(self.header_frame, text="GRC EXECUTIVE AUDIT CONTROL", 
                                    font=("Segoe UI", 24, "bold"), text_color=self.primary_color)
        header_title.pack(pady=(10, 5))
        
        self.stepper_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.stepper_frame.pack(fill="x", padx=50)
        self.create_stepper()

        # 2. Main Content Area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # 2a. Left Column: Gauge & Summary
        self.left_col = ctk.CTkFrame(self.content_frame, fg_color=self.surface_color, corner_radius=15)
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(self.left_col, text="CURRENT POSTURE", font=("Segoe UI", 18, "bold")).pack(pady=10)
        self.gauge_frame = ctk.CTkFrame(self.left_col, fg_color="transparent", height=250)
        self.gauge_frame.pack(fill="x", padx=10)
        self.gauge = ComplianceGauge(self.gauge_frame)
        self.gauge.update_gauge(68) # Sample score
        
        self.summary_box = ctk.CTkTextbox(self.left_col, height=300, fg_color=self.bg_color)
        self.summary_box.pack(fill="both", expand=True, padx=20, pady=20)
        self.summary_box.insert("0.0", "AUDIT SUMMARY\n" + "="*20 + "\n\n"
                                "Framework: ISO 27001:2022\n"
                                "Controls Verified: 12/93\n"
                                "Critical Gaps: 2\n"
                                "Next Review: " + datetime.now().strftime("%Y-%m-%d") + "\n\n"
                                "Status: IN PROGRESS")

        # 2b. Right Column: Control Table
        self.right_col = ctk.CTkFrame(self.content_frame, fg_color=self.surface_color, corner_radius=15)
        self.right_col.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(self.right_col, text="CONTROL VALIDATION MATRIX", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        self.control_list = ctk.CTkScrollableFrame(self.right_col, fg_color="transparent")
        self.control_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.populate_controls()

        # 3. Bottom Action Bar
        self.action_bar = ctk.CTkFrame(self, fg_color=self.surface_color, height=80, corner_radius=0)
        self.action_bar.grid(row=2, column=0, sticky="nsew", padx=0, pady=(10, 0))
        
        self.prev_btn = ctk.CTkButton(self.action_bar, text="PREVIOUS STEP", fg_color=self.surface_color, 
                                     border_width=1, border_color=self.primary_color, text_color=self.primary_color,
                                     command=self.prev_step)
        self.prev_btn.pack(side="left", padx=20, pady=20)
        
        self.report_btn = ctk.CTkButton(self.action_bar, text="GENERATE EXECUTIVE REPORT", 
                                       fg_color=self.accent_color, text_color="black",
                                       command=self.generate_report)
        self.report_btn.pack(side="right", padx=20, pady=20)
        
        self.next_btn = ctk.CTkButton(self.action_bar, text="NEXT STEP", fg_color=self.primary_color,
                                     command=self.next_step)
        self.next_btn.pack(side="right", padx=20, pady=20)

    def create_stepper(self):
        steps = ["Scope", "Assets", "Risks", "Policies", "Technical", "Operations", "Evidence", "Review", "Approval", "Report"]
        self.stepper_labels = []
        for i, step in enumerate(steps, 1):
            color = self.primary_color if i <= self.current_step else "#555"
            label = ctk.CTkLabel(self.stepper_frame, text=f"{i}. {step}", font=("Segoe UI", 10), text_color=color)
            label.pack(side="left", expand=True)
            self.stepper_labels.append(label)

    def update_stepper_ui(self):
        for i, label in enumerate(self.stepper_labels, 1):
            color = self.primary_color if i <= self.current_step else "#555"
            label.configure(text_color=color)

    def next_step(self):
        if self.current_step < 10:
            self.current_step += 1
            self.update_stepper_ui()
            if self.current_step == 10:
                messagebox.showinfo("Audit Complete", "You have reached the final step. You can now generate the executive report.")

    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1
            self.update_stepper_ui()

    def generate_report(self):
        audit_data = {
            "framework": "ISO 27001:2022",
            "score": 68,
            "status": "IN PROGRESS",
            "gaps": [
                "A.8.1: User Endpoint Devices (Missing Registry Policy)",
                "A.12.1: Operational Procedures (Manual Documentation Required)"
            ]
        }
        pdf_path = self.report_gen.generate_pdf(audit_data)
        docx_path = self.report_gen.generate_docx(audit_data)
        
        messagebox.showinfo("Report Generated", 
                            f"Executive reports have been successfully generated:\n\n"
                            f"PDF: {os.path.basename(pdf_path)}\n"
                            f"DOCX: {os.path.basename(docx_path)}\n\n"
                            "Location: /reports directory")

    def populate_controls(self):
        for ctrl in self.framework.controls:
            item = ctk.CTkFrame(self.control_list, fg_color=self.bg_color, height=80)
            item.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(item, text=f"{ctrl['id']}", font=("Consolas", 14, "bold"), text_color=self.accent_color).pack(side="left", padx=10)
            ctk.CTkLabel(item, text=f"{ctrl['name']}", font=("Segoe UI", 12)).pack(side="left", padx=10)
            
            status_color = "#87A96B" if ctrl['id'] != "A.8.1" else "#FF4B2B"
            status_text = "PASS" if ctrl['id'] != "A.8.1" else "FAIL"
            
            ctk.CTkLabel(item, text=status_text, text_color=status_color, font=("Segoe UI", 12, "bold")).pack(side="right", padx=20)
            ctk.CTkButton(item, text="Details", width=60, height=25, fg_color=self.surface_color).pack(side="right", padx=5)

if __name__ == "__main__":
    app = ComplianceAuditApp()
    app.mainloop()
