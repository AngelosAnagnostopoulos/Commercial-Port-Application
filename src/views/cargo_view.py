import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class CargoView(ControllerAwareFrame):

    COLUMNS = (
        "Ship Name",
        "Product",
        "Amount",
        "Transcaction Date"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)
        
    
        self.cargo_treeview = ColumnTreeView(self, columns=CargoView.COLUMNS, updater=self.controller.get_cargo)
     
        self.cargo_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

