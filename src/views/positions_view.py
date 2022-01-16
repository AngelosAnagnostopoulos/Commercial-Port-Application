from re import S
import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class PositionsView(ControllerAwareFrame):

    COLUMNS = (
        "Position Number",
        "Pier Number",
        "Ship ID",
        "Ship Name"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.__only_empty_invtar = tk.IntVar()
        self.only_empty_checkbox = tk.Checkbutton(self, text="Only show empty", 
                                                        variable=self.__only_empty_invtar,
                                                        command=self.update)
        self.only_empty_checkbox.deselect()
        self.only_empty_checkbox.pack(anchor=tk.W, padx=10, pady=10)

        self.positions_treeview = ColumnTreeView(self, 
                                                 columns=PositionsView.COLUMNS,
                                                 updater=self.get_position_data,
                                                 on_select=self.on_position_selected,
                                                 id_col=0,
                                                 text_on_null="EMPTY")

        self.positions_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def on_position_selected(self, position):
        print("position selected from view:", position)
        self.controller.position_selected(position)

    def show_empty(self):
        self.__only_empty_invtar.set(1)
        self.update()

    def update(self):
        self.get_position_data(self.positions_treeview.insert_to_treeview)

    def get_position_data(self, ins):
        self.positions_treeview.clear_all_children()
        self.controller.get_positions(self.__only_empty_invtar.get(), ins)