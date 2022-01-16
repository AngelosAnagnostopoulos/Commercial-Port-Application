import tkinter as tk
from tkcalendar import DateEntry
from .utilities import ControllerAwareFrame

class AddShipView(ControllerAwareFrame):

    COLUMNS = (
        "Ship Name",
        "Flag",
        "Length",
        "GT",
        "DWT"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        tk.Label(self, text="Add Ship").grid(columnspan=2, sticky=tk.NSEW, pady=10)

        self.entries = []

        current_row = 1
        for col_name in AddShipView.COLUMNS:
            tk.Label(self, text=col_name).grid(row=current_row, sticky=tk.W, padx=10, pady=10)
            
            entry = tk.Entry(self)
            entry.grid(row=current_row, column=1, sticky=tk.NSEW, padx=10, pady=10)

            self.entries.append(entry)

            current_row += 1

        tk.Label(self, text="Construction date").grid(row=current_row, sticky=tk.W, padx=10, pady=10)
        
        self.date_entry = DateEntry(self)
        self.date_entry.grid(row=current_row, column=1, sticky=tk.W, padx=10, pady=10)

        current_row += 1

        self.add_button = tk.Button(self, text="Add", command=self.add_ship)
        self.add_button.grid(row=current_row, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        
    def add_ship(self):
        data = [e.get() for e in self.entries]
        data.append(self.date_entry.get_date())
    
        self.controller.add_ship(data)

