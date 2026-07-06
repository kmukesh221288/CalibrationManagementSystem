import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from services.calibration_service import CalibrationService
from services.instrument_service import InstrumentService


class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.calibration_service = CalibrationService()
        self.columns = [
            ("instrument_code", "Instrument Code", 160),
            ("machine_code", "Machine Code", 140),
            ("calibration_date", "Calibration Date", 130),
            ("next_due_date", "Next Due Date", 130),
            ("calibration_type", "Calibration Type", 130),
            ("agency", "Agency", 140),
            ("certificate_number", "Certificate Number", 160),
            ("result", "Result", 100),
            ("cost", "Cost", 100),
            ("certificate", "Certificate", 180),
        ]

        self.build_ui()
        self.load_history()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=26,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
        )

        title = ctk.CTkLabel(
            self,
            text="Calibration History",
            font=("Segoe UI", 28, "bold"),
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            top_frame,
            width=360,
            placeholder_text="Instrument Code...",
        )
        self.search_entry.grid(row=0, column=0, sticky="w", padx=(10, 8), pady=10)
        self.search_entry.bind("<Return>", lambda event: self.load_history())

        self.refresh_button = ctk.CTkButton(
            top_frame,
            text="Refresh",
            width=120,
            command=self.load_history,
        )
        self.refresh_button.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=10)

        self.open_certificate_button = ctk.CTkButton(
            top_frame,
            text="Open Certificate",
            width=140,
            state="disabled",
            command=self.open_certificate
        )
        self.open_certificate_button.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=10)

        top_frame.grid_columnconfigure(0, weight=1)

        table_container = ctk.CTkFrame(self)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(
            table_container,
            columns=[column[0] for column in self.columns],
            show="headings",
            selectmode="browse",
        )

        for key, heading, width in self.columns:
            self.tree.heading(key, text=heading)
            self.tree.column(key, width=width, anchor="w", stretch=False)

        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f2f4f8")

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=vertical_scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

    def load_history(self):
        instrument_code = self.search_entry.get().strip()

        rows = self.calibration_service.get_calibration_history(instrument_code or None)
        if instrument_code and not rows:
            messagebox.showerror("Error", f"No calibration history found for {instrument_code}.")
            return

        self.display_rows(rows)

    def display_rows(self, rows):
        self.tree.delete(*self.tree.get_children())
        self.open_certificate_button.configure(state="disabled")

        for index, row in enumerate(rows):
            formatted_row = list(row)
            for pos in (2, 3):
                try:
                    formatted_row[pos] = datetime.strptime(formatted_row[pos], "%Y-%m-%d").strftime("%d-%b-%Y")
                except Exception:
                    pass
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=formatted_row, tags=(row_tag,))

    def on_row_selected(self, _event):
        selected = self.tree.selection()
        if selected:
            self.open_certificate_button.configure(state="normal")
        else:
            self.open_certificate_button.configure(state="disabled")

    def open_certificate(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        certificate_path = values[9] if len(values) > 9 else None

        if not certificate_path:
            messagebox.showerror("Error", "Certificate file not found.")
            return

        if os.path.exists(certificate_path):
            try:
                os.startfile(certificate_path)
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
        else:
            messagebox.showerror("Error", "Certificate file not found.")
