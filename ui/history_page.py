import customtkinter as ctk


class HistoryPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(
            self,
            text="Calibration History",
            font=("Arial",30,"bold")
        )

        label.pack(pady=50)