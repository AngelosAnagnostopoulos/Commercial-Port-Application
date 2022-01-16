import tkinter as tk

from .utilities import ControllerAwareFrame, GridLabeledField


class ShipDetailsView(ControllerAwareFrame):
    
    COLUMNS = (
            "Ship Name",
            "Ship ID",
            "Flag",
            "Constructuion Year",
            "Ship Length",
            "GT",
            "DWT",
            "Previous Port"
        )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.title_label = tk.Label(self, text="Ship Details")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
        self.data_display_labels = [GridLabeledField(self, field_data, row=place_row, column=0) for place_row, field_data in enumerate(ShipDetailsView.COLUMNS, start=1)]
        
        self.refresh_button = tk.Button(self, text="Referesh", command=self.fetch_ship_data)
        self.refresh_button.grid(row=len(ShipDetailsView.COLUMNS) + 2, column=0, columnspan=2)

        self.current_ship_id = 5

    def display_ship_data(self, shipid):
        self.current_ship_id = shipid
        self.fetch_ship_data()

    def fetch_ship_data(self):
        if self.current_ship_id:
            self.controller.get_ship_data(self.current_ship_id, self.__display_data)

    def __display_data(self, data):
        
        for grid_field, data_chunk in zip(self.data_display_labels, data):
            grid_field.update_data(data_chunk)
