import customtkinter as ctk
import tkinter as tk

from database.db_manager import Database
from controllers.navigation_controller import NavigationController

from services.reminder_service import ReminderService

from ui.sidebar import Sidebar

from ui.dashboard import Dashboard

from ui.instrument_page import InstrumentPage

from ui.calibration_page import CalibrationPage

from ui.history_page import HistoryPage

from ui.reports_page import ReportsPage

from ui.settings_page import SettingsPage


ctk.set_appearance_mode("Light")

ctk.set_default_color_theme("blue")


class CalibrationApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Calibration Management System")

        self.geometry("1400x800")

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.controller = NavigationController()

        Sidebar(self, self.controller)

        content = ctk.CTkFrame(self)
        content.controller = self.controller

        content.grid(row=0, column=1, sticky="nsew")

        dashboard = Dashboard(content)

        instrument = InstrumentPage(content)

        calibration = CalibrationPage(content)

        history = HistoryPage(content)

        reports = ReportsPage(content)

        settings = SettingsPage(content)

        self.controller.add_page("dashboard", dashboard)

        self.controller.add_page("instrument", instrument)

        self.controller.add_page("calibration", calibration)

        self.controller.add_page("history", history)

        self.controller.add_page("reports", reports)

        self.controller.add_page("settings", settings)

        self.controller.show_page("dashboard")

        self.after(100, self.show_reminder_popup)

    def show_reminder_popup(self):
        reminder_service = ReminderService()
        counts = reminder_service.get_reminder_counts()
        if not counts:
            return

        overdue, due_within_30 = counts
        dialog = tk.Toplevel(self)
        dialog.title("Calibration Reminder")
        dialog.geometry("360x180")
        dialog.resizable(False, False)
        dialog.grab_set()

        message = ctk.CTkLabel(
            dialog,
            text=f"Overdue Instruments: {overdue}\nDue within 30 Days: {due_within_30}",
            font=("Segoe UI", 14),
            justify="left"
        )
        message.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1), weight=1)

        open_button = ctk.CTkButton(
            button_frame,
            text="Open Due Report",
            command=lambda: self._open_due_report(dialog)
        )
        open_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            fg_color="#6c63ff",
            hover_color="#5548c8",
            command=dialog.destroy
        )
        close_button.grid(row=0, column=1, sticky="ew")

    def _open_due_report(self, dialog):
        dialog.destroy()
        self.controller.show_page("reports")


db = Database()
db.create_tables()

app = CalibrationApp()

app.mainloop()