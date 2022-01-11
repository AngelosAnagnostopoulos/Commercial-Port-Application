from database_connector import DatabaseConnector
from utils import info

import tkinter as tk
from tkinter import ttk

config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "database" : "projectDB",
        "raise_on_warnings": True
    }


connector = DatabaseConnector(config)
connector.start_executor()

def default_error_popup():
    tk.messagebox.showerror(title="Error", message="SQL Error!")

class ShipsInView(tk.Frame):

    QUERY = "SELECT ShipID, S_Name, PierID, PosID FROM Ship NATURAL JOIN Position_ NATURAL JOIN Pier WHERE PosID IS NOT NULL ORDER BY ShipID;"
    
    COLUMNS = ("Ship ID", "Ship Name", "Pier", "Position")

    DUMMY_DATA = (
        ('1', 'A', 'A', '1'),
        ('2', 'B', 'A', '2')
    )

    def __init__(self, master):
        super().__init__(master)

        self.refresh_button = tk.Button(self, text = "Refresh", command=self.run_update)
        self.refresh_button.pack(fill=tk.X)

        self.ship_view_table = ttk.Treeview(self, columns=ShipsInView.COLUMNS)

        self.ship_view_table.heading("#0", text="")
    
        # fix ghost col
        self.ship_view_table.column("#0", width=1, stretch=False)

        for column in ShipsInView.COLUMNS:
            self.ship_view_table.heading(column, text=column)
            self.ship_view_table.column(column, width=1, anchor=tk.CENTER)

        for entry in ShipsInView.DUMMY_DATA:
            self.ship_view_table.insert(parent='', index=tk.END, iid=str(entry[0]), values=entry)

        self.ship_view_table.pack(fill=tk.BOTH, expand=True, padx=10)

    def __insert_data_to_treeview(self, data):
        self.ship_view_table.insert(parent='', index=tk.END, iid=str(data[0]), values=data)


    def run_update(self):
        # delete all items in view
        
        for item in self.ship_view_table.get_children():
            self.ship_view_table.delete(item)

        connector.query_database(ShipsInView.QUERY, self.__insert_data_to_treeview)
        

class GridLabeledField:

    def __init__(self, master, field_name, row, column, vertical=False):
       self.__label = tk.Label(master, text=field_name)
       self.__data = tk.Label(master, text="placeholder")

       self.__label.grid(row=row, column=column, sticky=tk.W)
       
       data_row, data_col = row, column + 1
       if vertical:
           data_row, data_col = row + 1, column

       self.__data.grid(row=data_row, column=data_col, sticky=tk.W, padx=10)

    def update_data(self, data):
        self.__data.config(text=data)

class ShipView(tk.Frame):
    
    COLUMNS = (
            ("Ship Name", "S_Name"),
            ("Ship ID"  , "ShipID"),
            ("Flag"     , "Flag"  ),
            ("Coonstructuion Year", "Constructed"),
            ("Ship Length"        , "Length_"),
            ("GT", "GT"),
            ("DWT", "DWT"),
            ("Previous Port", "PrevPort")
        )

    FIELDS = ", ".join(map(lambda x : x[1], COLUMNS))

    QUERY = f"SELECT {FIELDS} FROM Ship WHERE ShipID = {{}}"

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.title_label = tk.Label(self, text="Ship Details")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
        self.data_display_labels = [GridLabeledField(self, field_data[0], row=place_row, column=0) for place_row, field_data in enumerate(ShipView.COLUMNS, start=1)]
        
        self.refresh_button = tk.Button(self, text="Referesh", command=self.fetch_ship_data)
        self.refresh_button.grid(row=len(ShipView.COLUMNS) + 2, column=0, columnspan=2)

        self.current_ship_id = 5

    def display_ship_data(self, shipid):
        self.current_ship_id = shipid
        self.fetch_ship_data()

    def __display_data(self, data):
        for grid_field, data_chunk in zip(self.data_display_labels, data):
            grid_field.update_data(data_chunk)

    def fetch_ship_data(self):
        
        if self.current_ship_id:
            query = ShipView.QUERY.format(self.current_ship_id)
            connector.query_database(query, self.__display_data, onerror=default_error_popup)


class EmployeeView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)


class App:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Βαγγέλα αλάνι, δικό σου το λιμάνι")

        self.tab_controller = ttk.Notebook(self.root)

        self.ships_in_frame = ShipsInView(self.root)
        self.employees = tk.Frame(self.root)
        self.employees.config(bg='red')

        self.ship_view = ShipView(self.root)

        self.tab_controller.add(self.ships_in_frame, text='Ships')
        self.tab_controller.add(self.employees, text='Employees')
        self.tab_controller.add(self.ship_view, text='Ship View')

        self.tab_controller.pack(fill=tk.BOTH, expand=True)
        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.root.mainloop()

    def on_close(self):
        connector.close_connector()
        self.root.destroy()

if __name__ == "__main__":
    App()



