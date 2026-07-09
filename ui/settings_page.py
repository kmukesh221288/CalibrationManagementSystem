import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from services.database_service import DatabaseService
from services.import_service import ImportService


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.database_service = DatabaseService()
        self.internal_calibration_file_path = None

        title_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 30, "bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 25), sticky="w")

        sections = [
            ("Database", ["Backup Database", "Restore Database"]),
            ("Folders", ["Open Backup Folder", "Open Export Folder", "Open Certificates Folder"]),
            ("Import", ["Import Internal Calibration", "Import External Calibration"]),
        ]

        for index, (section_title, buttons) in enumerate(sections, start=1):
            section_frame = ctk.CTkFrame(self, corner_radius=12)
            section_frame.grid(row=index, column=0, sticky="ew", padx=20, pady=(0, 15))
            section_frame.grid_columnconfigure(0, weight=1)

            section_label = ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=("Arial", 18, "bold")
            )
            section_label.grid(row=0, column=0, padx=20, pady=(16, 10), sticky="w")

            button_container = ctk.CTkFrame(section_frame)
            button_container.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")

            for button_index, button_text in enumerate(buttons):
                command = None
                if button_text == "Backup Database":
                    command = self._backup_database
                elif button_text == "Restore Database":
                    command = self._restore_database
                elif button_text == "Open Backup Folder":
                    command = self._open_backup_folder
                elif button_text == "Open Export Folder":
                    command = self._open_export_folder
                elif button_text == "Open Certificates Folder":
                    command = self._open_certificates_folder
                elif button_text == "Import Internal Calibration":
                    command = self._import_internal_calibration
                elif button_text == "Import External Calibration":
                    command = self._import_external_calibration

                button_width = 220 if len(buttons) == 1 else 200

                button = ctk.CTkButton(
                    button_container,
                    text=button_text,
                    width=button_width,
                    height=34,
                    corner_radius=8,
                    command=command
                )
                button.grid(row=0, column=button_index, padx=(0, 10), pady=4)

    def _backup_database(self):
        try:
            backup_path = self.database_service.backup_database()
            backup_name = os.path.basename(backup_path)
            messagebox.showinfo("Backup Created", f"Database backup created successfully.\n{backup_name}")
        except Exception as exc:
            messagebox.showerror("Backup Failed", str(exc))

    def _restore_database(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select Database Backup",
                filetypes=[("Database Files", "*.db")]
            )
            if not file_path:
                return

            self.database_service.restore_database(file_path)
            messagebox.showinfo(
                "Restore Successful",
                "Database restored successfully.\nPlease restart the application."
            )
        except Exception as exc:
            messagebox.showerror("Restore Failed", str(exc))

    def _open_backup_folder(self):
        self._open_folder("backups")

    def _open_export_folder(self):
        self._open_folder("exports")

    def _open_certificates_folder(self):
        self._open_folder("certificates")

    def _import_internal_calibration(self):
        self._import_calibration_file(
            title="Select Internal Calibration File",
            success_title="Internal Calibration Imported Successfully",
            sheet_name="Internal Calibration List",
            calibration_type="Internal",
        )

    def _import_external_calibration(self):
        self._import_calibration_file(
            title="Select External Calibration File",
            success_title="External Calibration Imported Successfully",
            sheet_name="External Calibration List",
            calibration_type="External",
        )

    def _import_calibration_file(self, title, success_title, sheet_name, calibration_type):
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("Excel Files", "*.xls")
            ]
        )
        if not file_path:
            return

        self.internal_calibration_file_path = file_path

        try:
            import_service = ImportService()
            summary = import_service.import_file(
                file_path,
                sheet_name=sheet_name,
                calibration_type=calibration_type,
            )
            messagebox.showinfo(
                success_title,
                f"{success_title}\n\n"
                f"New Instruments: {summary['new_instruments']}\n"
                f"Updated: {summary['updated']}\n"
                f"History Created: {summary['history_created']}\n"
                f"Errors: {summary['errors']}"
            )
        except Exception as exc:
            messagebox.showerror("Import Failed", str(exc))

    def _open_folder(self, folder_name):
        folder_path = os.path.abspath(folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        os.startfile(folder_path)
