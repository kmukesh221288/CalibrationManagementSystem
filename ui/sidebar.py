import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, width=220, corner_radius=0)

        self.controller = controller

        self.grid(row=0, column=0, sticky="ns")

        self.grid_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="Calibration\nManagement",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=30)

        buttons = [

            ("🏠 Dashboard", "dashboard"),

            ("🔧 Instrument Register", "instrument"),

            ("📅 Calibration", "calibration"),

            ("📜 History", "history"),

            ("📊 Reports", "reports"),

            ("⚙ Settings", "settings")

        ]

        for text, page in buttons:

            btn = ctk.CTkButton(

                self,

                text=text,

                width=180,

                height=40,

                command=lambda p=page: self.controller.show_page(p)

            )

            btn.pack(pady=8)