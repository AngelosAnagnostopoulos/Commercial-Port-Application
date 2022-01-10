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
        




class App:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Βαγγέλα αλάνι, δικό σου το λιμάνι")

        self.tab_controller = ttk.Notebook(self.root)

        self.ships_in_frame = ShipsInView(self.root)
        self.employees = tk.Frame(self.root)
        self.employees.config(bg='red')

        self.tab_controller.add(self.ships_in_frame, text='Ships')
        self.tab_controller.add(self.employees, text='Employees')

        self.tab_controller.pack(fill=tk.BOTH, expand=True)
        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.root.mainloop()

    def on_close(self):
        connector.close_connector()
        self.root.destroy()

if __name__ == "__main__":
    App()



