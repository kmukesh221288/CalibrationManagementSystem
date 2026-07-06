import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from services.instrument_service import InstrumentService
from ui.add_instrument_dialog import AddInstrumentDialog


class InstrumentPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.service = InstrumentService()
        self.columns = [
            ("machine_code", "Machine Code", 140),
            ("machine_name", "Machine Name", 220),
            ("instrument_code", "Instrument Code", 160),
            ("instrument_name", "Instrument Name", 220),
            ("department", "Department", 140),
            ("frequency", "Frequency", 120),
            ("status", "Status", 110),
        ]
        self.selected_row = None

        self.build_ui()
        self.load_table()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
        )

        title = ctk.CTkLabel(
            self,
            text="Instrument Register",
            font=("Segoe UI", 26, "bold"),
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            top_frame,
            width=360,
            placeholder_text="🔍 Search...",
        )
        self.search_entry.grid(row=0, column=0, sticky="w", padx=(10, 8), pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_data)

        self.refresh_button = ctk.CTkButton(
            top_frame,
            text="Refresh",
            width=110,
            command=self.load_table,
        )
        self.refresh_button.grid(row=0, column=1, sticky="e", padx=(0, 8), pady=10)

        self.add_button = ctk.CTkButton(
            top_frame,
            text="+ Add Instrument",
            width=150,
            command=self.open_add_dialog,
        )
        self.add_button.grid(row=0, column=2, sticky="e", padx=(0, 8), pady=10)

        self.edit_button = ctk.CTkButton(
            top_frame,
            text="Edit Instrument",
            width=140,
            state="disabled",
            command=self.open_edit_dialog,
        )
        self.edit_button.grid(row=0, column=3, sticky="e", padx=(0, 8), pady=10)

        self.delete_button = ctk.CTkButton(
            top_frame,
            text="Delete Instrument",
            width=140,
            state="disabled",
            command=self.delete_instrument,
        )
        self.delete_button.grid(row=0, column=4, sticky="e", padx=(0, 10), pady=10)

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

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.tree.yview,
        )
        horizontal_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.tree.xview,
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

    def open_add_dialog(self):
        dialog = AddInstrumentDialog(self)
        self.wait_window(dialog)
        self.load_table()

    def open_edit_dialog(self):
        if not self.selected_row:
            return

        dialog = AddInstrumentDialog(
            self,
            instrument_data=self.selected_row,
            edit_mode=True,
        )
        self.wait_window(dialog)
        self.load_table()

    def load_table(self):
        rows = self.service.get_all_instruments()
        self.display_rows(rows)
        self.reset_selection()

    def search_data(self, event=None):
        search_text = self.search_entry.get().strip()
        if search_text == "":
            rows = self.service.get_all_instruments()
        else:
            rows = self.service.search_instruments(search_text)
        self.display_rows(rows)

    def display_rows(self, rows):
        self.tree.delete(*self.tree.get_children())

        for index, row in enumerate(rows):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(row_tag,))

    def on_row_selected(self, event=None):
        selected = self.tree.selection()
        if not selected:
            self.reset_selection()
            return

        self.selected_row = self.tree.item(selected[0], "values")
        self.edit_button.configure(state="normal")
        self.delete_button.configure(state="normal")

    def delete_instrument(self):
        if not self.selected_row:
            messagebox.showwarning(
                "No Selection",
                "Please select an instrument to delete."
            )
            return

        instrument_code = self.selected_row[2]
        confirm = messagebox.askyesno(
            "Delete Instrument",
            f"Are you sure you want to delete Instrument {instrument_code}?"
        )

        if not confirm:
            return

        try:
            self.service.delete_instrument(instrument_code)
            messagebox.showinfo(
                "Success",
                "Instrument deleted successfully."
            )
            self.load_table()
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def reset_selection(self):
        self.selected_row = None
        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
