from database_connector import DatabaseConnector, escape_string
from utils import info

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime

config = {
        "user":info.USER,
        "host":info.HOST,
        "password":info.PASSWORD,
        "port" : info.PORT,
        "database" : "projectDB",
        "raise_on_warnings": True
    }


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

        self.ship_view_table = ttk.Treeview(self, columns=ShipsInView.COLUMNS)

        self.ship_view_table.heading("#0", text="")
    
        # fix ghost col
        self.ship_view_table.column("#0", width=1, stretch=False)

        for column in ShipsInView.COLUMNS:
            self.ship_view_table.heading(column, text=column)
            self.ship_view_table.column(column, width=1, anchor=tk.CENTER)

        
        self.ship_view_table.bind("<Double-1>", self.on_click)

        self.ship_view_table.pack(fill=tk.BOTH, expand=True, padx=10)

    def on_click(self, event):
        selected_item = self.ship_view_table.selection()

        if selected_item is None or len(selected_item) != 1:
            return

        selected_item = selected_item[0]

        self.controller.display_ship_data(selected_item)
        
    
    def __insert_data_to_treeview(self, data):
        self.ship_view_table.insert(parent='', index=tk.END, iid=str(data[0]), values=data)


    def run_update(self):
        # delete all items in view
        
        for item in self.ship_view_table.get_children():
            self.ship_view_table.delete(item)

        self.controller.get_all_ships(self.ship_name_entry.get(), self.only_in_port_var.get(), self.__insert_data_to_treeview)
        

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
        self.__data.config(text=data)

class ShipView(ControllerAwareFrame):
    
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
    
        self.data_display_labels = [GridLabeledField(self, field_data, row=place_row, column=0) for place_row, field_data in enumerate(ShipView.COLUMNS, start=1)]
        
        self.refresh_button = tk.Button(self, text="Referesh", command=self.fetch_ship_data)
        self.refresh_button.grid(row=len(ShipView.COLUMNS) + 2, column=0, columnspan=2)

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


class AddShipView(ControllerAwareFrame):

    COLUMNS = (
        "Ship Name",
        "Flag",
        "Length",
        "GT",
        "DWT"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        tk.Label(self, text="Add Ship").grid(columnspan=2, sticky=tk.NSEW, pady=10)

        self.entries = []

        current_row = 1
        for col_name in AddShipView.COLUMNS:
            tk.Label(self, text=col_name).grid(row=current_row, sticky=tk.W, padx=10, pady=10)
            
            entry = tk.Entry(self)
            entry.grid(row=current_row, column=1, sticky=tk.NSEW, padx=10, pady=10)

            self.entries.append(entry)

            current_row += 1

        tk.Label(self, text="Construction date").grid(row=current_row, sticky=tk.W, padx=10, pady=10)
        
        self.date_entry = DateEntry(self)
        self.date_entry.grid(row=current_row, column=1, sticky=tk.W, padx=10, pady=10)

        current_row += 1

        self.add_button = tk.Button(self, text="Add", command=self.add_ship)
        self.add_button.grid(row=current_row, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        
    def add_ship(self):
        data = [e.get() for e in self.entries]
        data.append(self.date_entry.get_date())
    
        self.controller.add_ship(data)


        

class MovementView(ControllerAwareFrame):


    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)



class EmployeeView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)


class AppController:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Βαγγέλα αλάνι, δικό σου το λιμάνι")

        self.tab_controller = ttk.Notebook(self.root)

        self.ships_in_frame = self.new_aware_frame(ShipsInView)
        self.employees = tk.Frame(self.root)
        self.employees.config(bg='red')

        self.ship_view = self.new_aware_frame(ShipView)
        self.add_ship_view = self.new_aware_frame(AddShipView)

        self.tab_controller.add(self.ships_in_frame, text='Ships')
        self.tab_controller.add(self.employees, text='Employees')
        self.tab_controller.add(self.ship_view, text='Ship View')
        self.tab_controller.add(self.add_ship_view, text="Add Ship")

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

        QUERY = f"SELECT {FIELDS} FROM Ship WHERE ShipID = {{}}"
        
        query = QUERY.format(shipid)
        
        self.connector.query_database(query, data_dispatcher)
        

    def get_all_ships(self, name_search, only_in_port, data_dispatcher):
        view = "ShipsInPort" if only_in_port else "AllShipsView"

        query = f"SELECT * FROM {view}"

        if name_search:
            name_search = escape_string(name_search)
            query += f" WHERE S_Name LIKE '%{name_search}%';"

        self.connector.query_database(query, data_dispatcher)

        

    def add_ship(self, data):
        query = "INSERT INTO Ship (S_Name, Flag, Length_, GT, DWT, Constructed) VALUES ({})"
        
        print(data[-1])

        if not all(map(str.isdigit, data[2:5])):
            self.display_error_messagebox()
            return

        escape_and_quote = lambda s : f"'{escape_string(s)}'"

        sanitizers = [escape_and_quote, escape_and_quote, str, str, str, lambda date : f"DATE '{datetime.date.strftime(date, '%Y-%m-%d')}'"]

        sanitized_data = [sanitizer(field_data) for sanitizer, field_data in zip(sanitizers, data)]

        query = query.format(', '.join(sanitized_data))
        self.connector.query_database(query)



    def on_close(self):
        self.connector.close_connector()
        self.root.destroy()

if __name__ == "__main__":
    AppController()



