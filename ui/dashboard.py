import customtkinter as ctk
from services.dashboard_service import DashboardService


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.service = DashboardService()

        self.build_ui()

    def build_ui(self):

        total_instruments = self.service.get_total_instruments()
        total_calibrations = self.service.get_total_calibrations()
        due_this_month = self.service.get_due_this_month()
        overdue_count = self.service.get_overdue_count()
        certificate_count = self.service.get_certificate_count()
        total_cost = self.service.get_total_cost()

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", pady=(10, 20))

        cards = ctk.CTkFrame(self)
        cards.pack(fill="both", expand=True)
        cards.grid_columnconfigure((0, 1, 2), weight=1)
        cards.grid_rowconfigure((0, 1), weight=1)

        self.create_card(cards, "Total Instruments", total_instruments, 0, 0)
        self.create_card(cards, "Total Calibrations", total_calibrations, 0, 1)
        self.create_card(cards, "Due This Month", due_this_month, 0, 2)
        self.create_card(cards, "Overdue", overdue_count, 1, 0)
        self.create_card(cards, "Certificates Uploaded", certificate_count, 1, 1)
        self.create_card(cards, "Total Calibration Cost", total_cost, 1, 2)

    def create_card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(
            parent,
            corner_radius=20,
            fg_color="#ffffff",
            border_width=1,
            border_color="#d1d5db"
        )

        card.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        card.grid_rowconfigure(0, weight=0)
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        )
        lbl_title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        lbl_value = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 30, "bold"),
            anchor="w"
        )
        lbl_value.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 20))

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_ui()