import tkinter as tk
from tkinter import ttk

class ColumnTreeView(ttk.Treeview):

    def __init__(self, master, columns, updater=None, on_select=None, id_col=None, **cfg):
        super().__init__(master, columns=columns, **cfg)

        self.columns = columns
        self.__updater = updater
        self.__on_select = on_select
        self.__id_col = id_col
        self.heading("#0", text="")
    
        # fix ghost col
        self.column("#0", width=1, stretch=False)

        for column in self.columns:
            self.heading(column, text=column)
            self.column(column, width=1, anchor=tk.CENTER)

        if self.__on_select:
            self.bind("<Double-1>", self.__on_click)

        if self.__updater:
            self.bind("<FocusIn>", lambda e : self.update())

    def __on_click(self, event):
        selected_item = self.selection()

        if selected_item is None or len(selected_item) != 1:
            return

        selected_item = selected_item[0]

        self.__on_select(selected_item)

    def update(self):
        # delete all items in view

        for item in self.get_children():
            self.delete(item)

        self.__updater(self.insert_to_treeview)

    def insert_to_treeview(self, data):
        if self.__id_col is not None:
            self.insert(parent='', index=tk.END, iid=str(data[self.__id_col]), values=data)
        
        else:
            self.insert(parent='', index=tk.END, values=data)
    


class ControllerAwareFrame(tk.Frame):

    def __init__(self, controller, master, **cfg):
        super().__init__(master, **cfg)
        self.controller = controller

class ShipsInView(ControllerAwareFrame):
    
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

        self.ship_tree_view = ColumnTreeView(self, columns=ShipsInView.COLUMNS, 
                                                   on_select=self.controller.display_ship_data,
                                                   id_col=0)

        self.ship_tree_view.pack(fill=tk.BOTH, expand=True, padx=10)


    def run_update(self):
        self.controller.get_all_ships(self.ship_name_entry.get(), self.only_in_port_var.get(), self.ship_tree_view.insert_to_treeview)
        

class GridLabeledField:

    def __init__(self, master, field_name, row, column, vertical=False):
       self.__label = tk.Label(master, text=field_name)
       self.__data = tk.Label(master, text="")

       self.__label.grid(row=row, column=column, sticky=tk.W)
       
       data_row, data_col = row, column + 1
       if vertical:
           data_row, data_col = row + 1, column

       self.__data.grid(row=data_row, column=data_col, sticky=tk.W, padx=10)

    def update_data(self, data):
        if data is None:
            data = ''
        
        self.__data.config(text=data)
