import customtkinter as ctk
from services.dashboard_service import DashboardService


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.service = DashboardService()

        self.build_ui()

    def build_ui(self):

        data = self.service.get_counts()

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", pady=(10, 20))

        # ================= Cards =================

        cards = ctk.CTkFrame(self)
        cards.pack(fill="x")

        cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.create_card(cards, "🏭 Machines", data["machines"], 0)
        self.create_card(cards, "🔧 Instruments", data["instruments"], 1)
        self.create_card(cards, "📅 Due in 7 Days", data["due_next7"], 2)
        self.create_card(cards, "❌ Overdue", data["overdue"], 3)

        # ================= Upcoming =================

        title2 = ctk.CTkLabel(
            self,
            text="Upcoming Calibrations",
            font=("Arial", 22, "bold")
        )
        title2.pack(anchor="w", pady=(30, 10))

        table = ctk.CTkFrame(self)
        table.pack(fill="both", expand=True)

        headers = ["Machine", "Instrument", "Due Date"]

        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                table,
                text=text,
                font=("Arial", 16, "bold")
            )
            lbl.grid(row=0, column=col, padx=20, pady=10, sticky="w")

        upcoming = self.service.get_upcoming_calibrations()

        for r, row in enumerate(upcoming, start=1):
            for c, value in enumerate(row):
                lbl = ctk.CTkLabel(
                    table,
                    text=str(value)
                )
                lbl.grid(row=r, column=c, padx=20, pady=6, sticky="w")

    def create_card(self, parent, title, value, column):

        card = ctk.CTkFrame(
            parent,
            height=120,
            corner_radius=15
        )

        card.grid(
            row=0,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold")
        )
        lbl_title.pack(pady=(20, 10))

        lbl_value = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 34, "bold")
        )
        lbl_value.pack()