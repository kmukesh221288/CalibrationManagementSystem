import customtkinter as ctk

from services.instrument_service import InstrumentService
from ui.add_instrument_dialog import AddInstrumentDialog


class InstrumentPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = InstrumentService()

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Instrument Register",
            font=("Arial", 30, "bold")
        )

        title.pack(anchor="w", padx=20, pady=(20, 10))

        # ============================
        # Top Frame
        # ============================

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20)

        self.search = ctk.CTkEntry(
            top,
            width=350,
            placeholder_text="Search Machine / Instrument..."
        )

        self.search.pack(side="left", padx=5)

        # Live Search
        self.search.bind("<KeyRelease>", self.search_data)

        self.refresh_button = ctk.CTkButton(
            top,
            text="Refresh",
            command=self.load_table
        )

        self.refresh_button.pack(side="right", padx=5)

        self.add_button = ctk.CTkButton(
            top,
            text="+ Add Instrument",
            command=self.open_add_dialog
        )

        self.add_button.pack(side="right", padx=5)

        # ============================
        # Table
        # ============================

        self.table = ctk.CTkTextbox(
            self,
            font=("Consolas", 13)
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_table()

    # ======================================

    def open_add_dialog(self):

        dialog = AddInstrumentDialog(self)

        self.wait_window(dialog)

        self.load_table()

    # ======================================

    def load_table(self):

        rows = self.service.get_all_instruments()

        self.display_rows(rows)

    # ======================================

    def search_data(self, event=None):

        text = self.search.get().strip()

        if text == "":

            rows = self.service.get_all_instruments()

        else:

            rows = self.service.search_instruments(text)

        self.display_rows(rows)

    # ======================================

    def display_rows(self, rows):

        self.table.delete("1.0", "end")

        header = (
            f"{'Machine Code':<15}"
            f"{'Machine Name':<30}"
            f"{'Instrument Code':<20}"
            f"{'Instrument Name':<30}"
            f"{'Department':<15}"
            f"{'Frequency':<15}"
            f"{'Status'}\n"
        )

        self.table.insert("end", header)
        self.table.insert("end", "=" * 150 + "\n")

        for row in rows:

            line = (
                f"{row[0]:<15}"
                f"{row[1]:<30}"
                f"{row[2]:<20}"
                f"{row[3]:<30}"
                f"{row[4]:<15}"
                f"{row[5]:<15}"
                f"{row[6]}\n"
            )

            self.table.insert("end", line)