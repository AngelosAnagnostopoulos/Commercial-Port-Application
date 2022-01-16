import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class ShipsView(ControllerAwareFrame):
    
    COLUMNS = ("Ship ID", "Ship Name", "Flag", "Position")


    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.options_frame = tk.Frame(self)
        tk.Label(self.options_frame, text="Search by Ship name:").grid(sticky=tk.W, padx=10, ipady=10)
        
        self.ship_name_entry = tk.Entry(self.options_frame)
        self.ship_name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        self.only_in_port_var = tk.IntVar()
        self.only_in_port_checkbox = tk.Checkbutton(self.options_frame, text="Only show ships in port", variable=self.only_in_port_var)
        self.only_in_port_checkbox.select()
        self.only_in_port_checkbox.grid(row=2, sticky=tk.W, padx=10, pady=10)

        self.refresh_button = tk.Button(self.options_frame, text = "Search", command=self.run_update)
        self.refresh_button.grid(row=3, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

        self.options_frame.pack(fill=tk.X)

        self.ship_tree_view = ColumnTreeView(self, columns=ShipsView.COLUMNS, 
                                                   on_select=self.controller.display_ship_data,
                                                   id_col=0)

        self.ship_tree_view.pack(fill=tk.BOTH, expand=True, padx=10)


    def run_update(self):
        self.ship_tree_view.clear_all_children()
        self.controller.get_all_ships(self.ship_name_entry.get(), self.only_in_port_var.get(), self.ship_tree_view.insert_to_treeview)
    

        
        