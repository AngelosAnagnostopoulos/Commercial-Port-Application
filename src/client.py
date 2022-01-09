import mysql.connector
from mysql.connector import errorcode
from utils import dbutils, schema, info

import tkinter as tk
from tkinter import ttk

import asyncio


config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "database" : "projectDB",
        "raise_on_warnings": True
    }


class ShipsInView(tk.Frame):

    COLUMNS = ("Ship ID", "Ship Name", "Pier", "Position")

    DUMMY_DATA = (
        ('1', 'A', 'A', '1'),
        ('2', 'B', 'A', '2')
    )

    def __init__(self, master):
        super().__init__(master)

        self.ship_view_table = ttk.Treeview(self, columns=ShipsInView.COLUMNS)

        self.ship_view_table.heading("#0", text="")
    
        # fix ghost col
        self.ship_view_table.column("#0", width=1, stretch=False)

        for column in ShipsInView.COLUMNS:
            self.ship_view_table.heading(column, text=column)
            self.ship_view_table.column(column, width=1, anchor=tk.CENTER)

        for entry in ShipsInView.DUMMY_DATA:
            self.ship_view_table.insert(parent='', index=tk.END, iid=entry[0], values=entry)

        self.ship_view_table.pack(fill=tk.BOTH, expand=True, padx=10)
        
    def update(self):

        # delete all items in view
        for item in self.ship_view_table:
            self.ship_view_table.delete(item)

        # fetch data

        

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
        self.root.mainloop()


if __name__ == "__main__":
    App()



