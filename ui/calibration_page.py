import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from services.instrument_service import InstrumentService
from services.calibration_service import CalibrationService


class CalibrationPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.instrument_service = InstrumentService()
        self.calibration_service = CalibrationService()
        self.certificate_path = ""
        self.build_ui()
        self.load_instrument_codes()

    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Calibration Entry",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        left_frame.grid_columnconfigure(0, weight=1)

        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        right_frame.grid_columnconfigure(0, weight=1)

        self.instrument_code = ctk.CTkComboBox(
            left_frame,
            values=["Select Instrument Code"],
            fg_color="#2f8cff",
            button_color="#1a6ad8",
            button_hover_color="#145bb7",
            command=self.on_instrument_code_change
        )
        self.instrument_code.grid(row=0, column=0, sticky="ew", pady=(10, 8))

        self.instrument_name = ctk.CTkEntry(
            left_frame,
            placeholder_text="Instrument Name",
            state="disabled"
        )
        self.instrument_name.grid(row=1, column=0, sticky="ew", pady=5)

        self.machine_code = ctk.CTkEntry(
            left_frame,
            placeholder_text="Machine Code",
            state="disabled"
        )
        self.machine_code.grid(row=2, column=0, sticky="ew", pady=5)

        self.machine_name = ctk.CTkEntry(
            left_frame,
            placeholder_text="Machine Name",
            state="disabled"
        )
        self.machine_name.grid(row=3, column=0, sticky="ew", pady=5)

        self.frequency = ctk.CTkEntry(
            left_frame,
            placeholder_text="Frequency",
            state="disabled"
        )
        self.frequency.grid(row=4, column=0, sticky="ew", pady=5)

        calibration_date_label = ctk.CTkLabel(
            right_frame,
            text="Calibration Date",
            anchor="w"
        )
        calibration_date_label.grid(row=0, column=0, sticky="ew", pady=(10, 5))

        self.calibration_date = ctk.CTkEntry(
            right_frame,
            placeholder_text="YYYY-MM-DD"
        )
        self.calibration_date.grid(row=1, column=0, sticky="ew", pady=5)

        self.calibration_type = ctk.CTkComboBox(
            right_frame,
            values=["Internal", "External"],
            fg_color="#2f8cff",
            button_color="#1a6ad8",
            button_hover_color="#145bb7"
        )
        self.calibration_type.grid(row=2, column=0, sticky="ew", pady=(10, 5))

        self.agency = ctk.CTkEntry(
            right_frame,
            placeholder_text="Agency"
        )
        self.agency.grid(row=3, column=0, sticky="ew", pady=5)

        self.certificate_number = ctk.CTkEntry(
            right_frame,
            placeholder_text="Certificate Number"
        )
        self.certificate_number.grid(row=4, column=0, sticky="ew", pady=5)

        self.cost = ctk.CTkEntry(
            right_frame,
            placeholder_text="Cost"
        )
        self.cost.grid(row=5, column=0, sticky="ew", pady=5)

        self.result = ctk.CTkComboBox(
            right_frame,
            values=["Pass", "Fail"],
            fg_color="#2f8cff",
            button_color="#1a6ad8",
            button_hover_color="#145bb7"
        )
        self.result.grid(row=6, column=0, sticky="ew", pady=(10, 5))

        self.remarks = ctk.CTkTextbox(
            right_frame,
            width=200,
            height=120
        )
        self.remarks.grid(row=7, column=0, sticky="ew", pady=5)

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.upload_button = ctk.CTkButton(
            bottom_frame,
            text="Upload Certificate",
            width=180,
            command=self.upload_certificate
        )
        self.upload_button.pack(side="left", padx=(0, 10), pady=10)

        self.upload_label = ctk.CTkLabel(
            bottom_frame,
            text="No certificate selected",
            anchor="w",
            font=("Segoe UI", 12)
        )
        self.upload_label.pack(side="left", padx=(10, 0), pady=10)

        self.save_button = ctk.CTkButton(
            bottom_frame,
            text="Save Calibration",
            width=180,
            fg_color="#219653",
            hover_color="#1d8a44",
            command=self.save_calibration
        )
        self.save_button.pack(side="right", padx=(10, 0), pady=10)

    def load_instrument_codes(self):
        instruments = self.instrument_service.get_all_instruments()
        codes = [row[2] for row in instruments if row[2]]
        values = ["Select Instrument Code"] + codes
        self.instrument_code.configure(values=values)

    def on_instrument_code_change(self, selected_code):
        if not selected_code or selected_code == "Select Instrument Code":
            self.machine_code.configure(state="normal")
            self.machine_name.configure(state="normal")
            self.instrument_name.configure(state="normal")
            self.frequency.configure(state="normal")

            self.machine_code.delete(0, "end")
            self.machine_name.delete(0, "end")
            self.instrument_name.delete(0, "end")
            self.frequency.delete(0, "end")

            self.machine_code.configure(state="disabled")
            self.machine_name.configure(state="disabled")
            self.instrument_name.configure(state="disabled")
            self.frequency.configure(state="disabled")
            return

        details = self.instrument_service.get_instrument_details(selected_code)
        if details:
            machine_code, machine_name, instrument_code, instrument_name, department, frequency = details
            self.machine_code.configure(state="normal")
            self.machine_name.configure(state="normal")
            self.instrument_name.configure(state="normal")
            self.frequency.configure(state="normal")

            self.machine_code.delete(0, "end")
            self.machine_name.delete(0, "end")
            self.instrument_name.delete(0, "end")
            self.frequency.delete(0, "end")

            self.machine_code.insert(0, machine_code)
            self.machine_name.insert(0, machine_name)
            self.instrument_name.insert(0, instrument_name)
            self.frequency.insert(0, frequency)

            self.machine_code.configure(state="disabled")
            self.machine_name.configure(state="disabled")
            self.instrument_name.configure(state="disabled")
            self.frequency.configure(state="disabled")

    def upload_certificate(self):
        instrument_code = self.instrument_code.get()
        calibration_date = self.calibration_date.get().strip()

        if not instrument_code or instrument_code == "Select Instrument Code":
            messagebox.showerror("Validation Error", "Select an Instrument Code before uploading a certificate.")
            return

        if not calibration_date:
            messagebox.showerror("Validation Error", "Enter Calibration Date before uploading a certificate.")
            return

        file_path = filedialog.askopenfilename(
            title="Select Certificate PDF",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".pdf"):
            messagebox.showerror("Invalid File", "Only PDF files are allowed.")
            return

        os.makedirs("certificates", exist_ok=True)
        invalid_chars = '/\\:*?"<>|'
        sanitized_code = ''.join('_' if c in invalid_chars else c for c in instrument_code)
        target_name = f"{sanitized_code}_{calibration_date}.pdf"
        target_path = os.path.join("certificates", target_name)

        try:
            shutil.copyfile(file_path, target_path)
            self.certificate_path = target_path
            self.upload_label.configure(text=os.path.basename(target_path))
            messagebox.showinfo("Success", "Certificate uploaded successfully.")
        except Exception as exc:
            messagebox.showerror("Upload Error", str(exc))
            self.certificate_path = ""
            self.upload_label.configure(text="No certificate selected")

    def save_calibration(self):
        instrument_code = self.instrument_code.get()
        calibration_date = self.calibration_date.get().strip()
        calibration_type = self.calibration_type.get().strip()
        agency = self.agency.get().strip()
        certificate_number = self.certificate_number.get().strip()
        cost = self.cost.get().strip()
        result = self.result.get().strip()
        remarks = self.remarks.get("1.0", "end").strip()
        certificate_path = self.certificate_path

        if not instrument_code or instrument_code == "Select Instrument Code":
            messagebox.showerror("Validation Error", "Instrument Code is required.")
            return

        if not calibration_date:
            messagebox.showerror("Validation Error", "Calibration Date is required.")
            return

        if not result:
            messagebox.showerror("Validation Error", "Result is required.")
            return

        try:
            self.calibration_service.add_calibration(
                instrument_code,
                calibration_date,
                calibration_type,
                agency,
                certificate_number,
                cost,
                result,
                remarks,
                certificate_path,
            )
        except Exception as exc:
            messagebox.showerror("Save Error", str(exc))
            return

        messagebox.showinfo(
            "Success",
            "Calibration saved successfully."
        )

        self.calibration_date.delete(0, "end")
        self.calibration_type.set("")
        self.agency.delete(0, "end")
        self.certificate_number.delete(0, "end")
        self.cost.delete(0, "end")
        self.result.set("")
        self.remarks.delete("1.0", "end")
        self.certificate_path = ""
        self.instrument_code.set("Select Instrument Code")
        self.on_instrument_code_change("Select Instrument Code")

        controller = getattr(self.master, "controller", None)
        if controller:
            history_page = controller.pages.get("history")
            if history_page is not None:
                history_page.load_history()
            dashboard_page = controller.pages.get("dashboard")
            if dashboard_page is not None and hasattr(dashboard_page, "refresh"):
                dashboard_page.refresh()