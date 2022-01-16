from database_connector import DatabaseConnector, escape_string
from utils import info

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime

from views import *

config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "database" : "projectDB",
        "raise_on_warnings": True
    }


class AppController:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Βαγγέλα αλάνι, δικό σου το λιμάνι")

        self.tab_controller = ttk.Notebook(self.root)

        self.ships_in_view = self.new_aware_frame(ShipsView)
        self.employees_view = self.new_aware_frame(EmployeesView)
        self.ship_view = self.new_aware_frame(ShipDetailsView)
        self.add_ship_view = self.new_aware_frame(AddShipView)
        self.cargo_view = self.new_aware_frame(CargoView)
        self.movements_view = self.new_aware_frame(MovementView)
        self.raw_sql_view = self.new_aware_frame(RawSQLView)

        self.tab_controller.add(self.ships_in_view, text='Ships')
        self.tab_controller.add(self.employees_view, text='Employees')
        self.tab_controller.add(self.ship_view, text='Ship View')
        self.tab_controller.add(self.add_ship_view, text="Add Ship")
        self.tab_controller.add(self.cargo_view, text="Cargo")
        self.tab_controller.add(self.movements_view, text="Movements")
        self.tab_controller.add(self.raw_sql_view, text="Raw SQL")

        self.tab_controller.pack(fill=tk.BOTH, expand=True)


        self.connector = DatabaseConnector(config, default_error_handler=self.display_error_messagebox)
        self.connector.start_executor()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.root.mainloop()


    def display_error_messagebox(self):
        tk.messagebox.showerror(title="Error", message="SQL Error!", parent=self.root)
    

    def new_aware_frame(self, aware_type, **cfg_options):
        return aware_type(self, self.root, **cfg_options)


    def display_ship_data(self, shipid):
        self.tab_controller.select(2)
        self.ship_view.display_ship_data(shipid)

    def get_ship_data(self, shipid, data_dispatcher):
        
        COLUMNS = (
                "S_Name",
                "ShipID",
                "Flag"  ,
                "Constructed",
                "Length_",
                "GT",
                "DWT",
                "PrevPort",
            )

        FIELDS = ", ".join(COLUMNS)

        query = f"SELECT {FIELDS} FROM Ship WHERE ShipID = {shipid}"

        self.connector.query_database(query, data_dispatcher)
        

    def get_all_ships(self, name_search, only_in_port, data_dispatcher):
        view = "ShipsInPort" if only_in_port else "AllShipsView"

        query = f"SELECT * FROM {view}"

        if name_search:
            name_search = escape_string(name_search)
            query += f" WHERE S_Name LIKE '%{name_search}%';"

        self.connector.query_database(query, data_dispatcher)

    def get_cargo(self, data_dispatcher):
        query = "SELECT * FROM CargoInfo"
        
        self.connector.query_database(query, data_dispatcher)
    
    def get_arrivals(self, data_dispatcher):
        query = "SELECT * FROM ArrivingSoon"

        self.connector.query_database(query, data_dispatcher)


    def get_departures(self, data_dispatcher):
        query = "SELECT * FROM DepartingSoon"

        self.connector.query_database(query, data_dispatcher)


    def add_ship(self, data):
        query = "INSERT INTO Ship (S_Name, Flag, Length_, GT, DWT, Constructed) VALUES ({})"

        if not all(map(str.isdigit, data[2:5])):
            self.display_error_messagebox()
            return

        escape_and_quote = lambda s : f"'{escape_string(s)}'"

        sanitizers = [escape_and_quote, escape_and_quote, str, str, str, lambda date : f"DATE '{datetime.date.strftime(date, '%Y-%m-%d')}'"]

        sanitized_data = [sanitizer(field_data) for sanitizer, field_data in zip(sanitizers, data)]

        query = query.format(', '.join(sanitized_data))
        self.connector.query_database(query)

    def get_employees(self, data_dispatcher):
        query = "SELECT * FROM EmployeeInfo"

        self.connector.query_database(query, dispatcher=data_dispatcher)

    def execute_raw_sql(self, query, data_dispatcher, column_dispatcher):
        self.connector.query_database(query, dispatcher=data_dispatcher, column_dispatcher=column_dispatcher)


    def on_close(self):
        self.connector.close_connector()
        self.root.destroy()

if __name__ == "__main__":
    AppController()



