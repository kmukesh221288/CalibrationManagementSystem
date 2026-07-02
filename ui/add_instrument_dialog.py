import customtkinter as ctk
from tkinter import messagebox

from services.instrument_service import InstrumentService


class AddInstrumentDialog(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.service = InstrumentService()

        self.title("Add Instrument")

        self.geometry("450x500")

        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Add New Instrument",
            font=("Arial",24,"bold")
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
            text="Save",
            command=self.save
        ).pack(pady=20)

    def save(self):

        try:

            self.service.add_instrument(

                self.machine_code.get(),

                self.machine_name.get(),

                self.department.get(),

                self.instrument_code.get(),

                self.instrument_name.get(),

                self.frequency.get()

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