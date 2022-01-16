import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class MovementView(ControllerAwareFrame):

    ARRIVALS_COLUMNS = (
        "ShipID",
        "Ship Name",
        "Flag",
        "Arrival Date"
    )

    DEPARTURES_COLUMNS = (
        "ShipID",
        "Ship Name",
        "Flag",
        "Departure Date"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        tk.Label(self, text="Arrivals").pack(anchor=tk.CENTER, pady=10)

        self.arrivals_treeview = ColumnTreeView(self, columns=MovementView.ARRIVALS_COLUMNS, 
                                                      updater=self.controller.get_arrivals, 
                                                      id_col=0)

        self.arrivals_treeview.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=10, pady=10)

        tk.Label(self, text="Deparures").pack(anchor=tk.CENTER, pady=10)

        self.departures_treeview = ColumnTreeView(self, columns=MovementView.DEPARTURES_COLUMNS, 
                                                        updater=self.controller.get_departures, 
                                                        id_col=0)

        self.departures_treeview.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=10, pady=10)

