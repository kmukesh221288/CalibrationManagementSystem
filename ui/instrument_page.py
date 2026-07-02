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

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20)

        self.search = ctk.CTkEntry(
            top,
            width=300,
            placeholder_text="Search..."
        )

        self.search.pack(side="left", padx=5)

        self.add_button = ctk.CTkButton(
            top,
            text="+ Add Instrument",
            command=self.open_add_dialog
        )

        self.add_button.pack(side="right", padx=5)

        self.refresh_button = ctk.CTkButton(
            top,
            text="Refresh",
            command=self.load_table
        )

        self.refresh_button.pack(side="right", padx=5)

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

    def open_add_dialog(self):

        AddInstrumentDialog(self)

    def load_table(self):

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

        rows = self.service.get_all_instruments()

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