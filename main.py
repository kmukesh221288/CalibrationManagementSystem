import customtkinter as ctk

from database.db_manager import Database
from controllers.navigation_controller import NavigationController

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


db = Database()
db.create_tables()

app = CalibrationApp()

app.mainloop()