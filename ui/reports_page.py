import customtkinter as ctk
from tkinter import messagebox, ttk

from services.report_service import ReportService


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.build_ui()

    def build_ui(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self,
            text="Calibration Reports",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(anchor="w", pady=(0, 20))

        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        filter_frame.grid_columnconfigure(4, weight=0)

        report_type_label = ctk.CTkLabel(
            filter_frame,
            text="Report Type",
            anchor="w",
            font=("Segoe UI", 12, "bold")
        )
        report_type_label.grid(row=0, column=0, padx=(12, 8), pady=(12, 4), sticky="w")

        self.report_type = ctk.CTkComboBox(
            filter_frame,
            values=[
                "Due Calibration Report",
                "Overdue Report",
                "Calibration History",
                "Calibration Cost",
                "Certificate Missing"
            ],
            width=220,
            fg_color="#ffffff",
            button_color="#1a6ad8",
            button_hover_color="#145bb7"
        )
        self.report_type.set("Due Calibration Report")
        self.report_type.grid(row=1, column=0, padx=(12, 8), pady=(0, 12), sticky="ew")

        department_label = ctk.CTkLabel(
            filter_frame,
            text="Department",
            anchor="w",
            font=("Segoe UI", 12, "bold")
        )
        department_label.grid(row=0, column=1, padx=(8, 8), pady=(12, 4), sticky="w")

        self.department = ctk.CTkComboBox(
            filter_frame,
            values=["All"],
            width=220,
            fg_color="#ffffff",
            button_color="#1a6ad8",
            button_hover_color="#145bb7"
        )
        self.department.set("All")
        self.department.grid(row=1, column=1, padx=(8, 8), pady=(0, 12), sticky="ew")

        date_from_label = ctk.CTkLabel(
            filter_frame,
            text="Date From",
            anchor="w",
            font=("Segoe UI", 12, "bold")
        )
        date_from_label.grid(row=0, column=2, padx=(8, 8), pady=(12, 4), sticky="w")

        self.date_from = ctk.CTkEntry(
            filter_frame,
            placeholder_text="YYYY-MM-DD",
            width=220
        )
        self.date_from.grid(row=1, column=2, padx=(8, 8), pady=(0, 12), sticky="ew")

        date_to_label = ctk.CTkLabel(
            filter_frame,
            text="Date To",
            anchor="w",
            font=("Segoe UI", 12, "bold")
        )
        date_to_label.grid(row=0, column=3, padx=(8, 12), pady=(12, 4), sticky="w")

        self.date_to = ctk.CTkEntry(
            filter_frame,
            placeholder_text="YYYY-MM-DD",
            width=220
        )
        self.date_to.grid(row=1, column=3, padx=(8, 12), pady=(0, 12), sticky="ew")

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.generate_button = ctk.CTkButton(
            button_frame,
            text="Generate Report",
            fg_color="#1a6ad8",
            hover_color="#145bb7",
            width=180,
            command=self.generate_report
        )
        self.generate_button.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="w")

        self.export_excel_button = ctk.CTkButton(
            button_frame,
            text="Export Excel",
            fg_color="#6c63ff",
            hover_color="#5548c8",
            width=150,
            command=self.export_excel
        )
        self.export_excel_button.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        self.export_pdf_button = ctk.CTkButton(
            button_frame,
            text="Export PDF",
            fg_color="#34a853",
            hover_color="#2e8a49",
            width=150
        )
        self.export_pdf_button.grid(row=0, column=2, padx=(0, 10), pady=(0, 10), sticky="w")

        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(fill="both", expand=True)
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        self.report_tree = ttk.Treeview(
            preview_frame,
            columns=(
                "Instrument Code",
                "Machine Code",
                "Machine Name",
                "Department",
                "Calibration Date",
                "Next Due Date",
                "Days Remaining",
                "Status"
            ),
            show="headings"
        )
        self.report_tree.heading("Instrument Code", text="Instrument Code")
        self.report_tree.heading("Machine Code", text="Machine Code")
        self.report_tree.heading("Machine Name", text="Machine Name")
        self.report_tree.heading("Department", text="Department")
        self.report_tree.heading("Calibration Date", text="Calibration Date")
        self.report_tree.heading("Next Due Date", text="Next Due Date")
        self.report_tree.heading("Days Remaining", text="Days Remaining")
        self.report_tree.heading("Status", text="Status")

        self.report_tree.column("Instrument Code", width=140, anchor="w")
        self.report_tree.column("Machine Code", width=140, anchor="w")
        self.report_tree.column("Machine Name", width=160, anchor="w")
        self.report_tree.column("Department", width=140, anchor="w")
        self.report_tree.column("Calibration Date", width=140, anchor="w")
        self.report_tree.column("Next Due Date", width=140, anchor="w")
        self.report_tree.column("Days Remaining", width=120, anchor="w")
        self.report_tree.column("Status", width=120, anchor="w")

        self.v_scroll = ttk.Scrollbar(
            preview_frame,
            orient="vertical",
            command=self.report_tree.yview
        )
        self.h_scroll = ttk.Scrollbar(
            preview_frame,
            orient="horizontal",
            command=self.report_tree.xview
        )

        self.report_tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.report_tree.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

    def generate_report(self):
        if self.report_type.get() != "Due Calibration Report":
            return

        service = ReportService()
        rows = service.generate_due_calibration_report(department=self.department.get())

        self.report_tree.delete(*self.report_tree.get_children())
        for row in rows:
            self.report_tree.insert("", "end", values=row)

    def export_excel(self):
        rows = [self.report_tree.item(item, "values") for item in self.report_tree.get_children()]
        if not rows:
            messagebox.showinfo("Export Excel", "No data available to export.")
            return

        service = ReportService()
        service.export_to_excel(rows)
        messagebox.showinfo("Export Excel", "Excel report exported successfully.")
