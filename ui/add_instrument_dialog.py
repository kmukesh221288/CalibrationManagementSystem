import customtkinter as ctk
from tkinter import messagebox

from services.instrument_service import InstrumentService


class AddInstrumentDialog(ctk.CTkToplevel):

    def __init__(self, parent, instrument_data=None, edit_mode=False):

        super().__init__(parent)

        self.service = InstrumentService()
        self.edit_mode = edit_mode
        self.original_instrument_code = None

        title_text = "Edit Instrument" if self.edit_mode else "Add Instrument"
        heading_text = "Edit Instrument" if self.edit_mode else "Add New Instrument"
        button_text = "Update" if self.edit_mode else "Save"

        self.title(title_text)
        self.geometry("450x500")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text=heading_text,
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.machine_code = ctk.CTkEntry(
            self,
            placeholder_text="Machine Code"
        )
        self.machine_code.pack(fill="x", padx=20, pady=5)

        self.machine_name = ctk.CTkEntry(
            self,
            placeholder_text="Machine Name"
        )
        self.machine_name.pack(fill="x", padx=20, pady=5)

        self.department = ctk.CTkEntry(
            self,
            placeholder_text="Department"
        )
        self.department.pack(fill="x", padx=20, pady=5)

        self.instrument_code = ctk.CTkEntry(
            self,
            placeholder_text="Instrument Code"
        )
        self.instrument_code.pack(fill="x", padx=20, pady=5)

        self.instrument_name = ctk.CTkEntry(
            self,
            placeholder_text="Instrument Name"
        )
        self.instrument_name.pack(fill="x", padx=20, pady=5)

        self.frequency = ctk.CTkEntry(
            self,
            placeholder_text="Frequency (3 Months)"
        )
        self.frequency.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(
            self,
            text=button_text,
            command=self.save
        ).pack(pady=20)

        if instrument_data is not None:
            self.populate_fields(instrument_data)

    def populate_fields(self, instrument_data):
        self.original_instrument_code = instrument_data[2]
        self.machine_code.insert(0, instrument_data[0])
        self.machine_name.insert(0, instrument_data[1])
        self.department.insert(0, instrument_data[4])
        self.instrument_code.insert(0, instrument_data[2])
        self.instrument_name.insert(0, instrument_data[3])
        self.frequency.insert(0, instrument_data[5])

    def save(self):
        try:
            machine_code = self.machine_code.get().strip()
            machine_name = self.machine_name.get().strip()
            department = self.department.get().strip()
            instrument_code = self.instrument_code.get().strip()
            instrument_name = self.instrument_name.get().strip()
            frequency = self.frequency.get().strip()

            if self.edit_mode:
                self.service.update_instrument(
                    self.original_instrument_code,
                    machine_code,
                    machine_name,
                    department,
                    instrument_code,
                    instrument_name,
                    frequency,
                )
                messagebox.showinfo(
                    "Success",
                    "Instrument Updated Successfully"
                )
            else:
                self.service.add_instrument(
                    machine_code,
                    machine_name,
                    department,
                    instrument_code,
                    instrument_name,
                    frequency,
                )
                messagebox.showinfo(
                    "Success",
                    "Instrument Added Successfully"
                )

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
