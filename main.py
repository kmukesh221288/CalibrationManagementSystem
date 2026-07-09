import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

from database.db_manager import Database
from controllers.navigation_controller import NavigationController

from services.database_service import DatabaseService
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

        self.database_service = DatabaseService()
        self._create_menu()

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

    def _create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        tools_menu.add_command(label="Backup Database", command=self._backup_database)
        tools_menu.add_command(label="Restore Database", command=self._restore_database)
        tools_menu.add_command(label="Open Backup Folder", command=self._open_backup_folder)

    def _backup_database(self):
        try:
            backup_path = self.database_service.backup_database()
            backup_name = os.path.basename(backup_path)
            messagebox.showinfo("Backup Created", f"Database backup created successfully.\n{backup_name}")
        except Exception as exc:
            messagebox.showerror("Backup Failed", str(exc))

    def _restore_database(self):
        backup_file = filedialog.askopenfilename(
            title="Select Backup Database",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
        )
        if not backup_file:
            return

        try:
            self.database_service.restore_database(backup_file)
            messagebox.showinfo("Restore Successful", "Database restored successfully.")
        except Exception as exc:
            messagebox.showerror("Restore Failed", str(exc))

    def _open_backup_folder(self):
        backup_dir = os.path.abspath("backups")
        os.makedirs(backup_dir, exist_ok=True)
        os.startfile(backup_dir)

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