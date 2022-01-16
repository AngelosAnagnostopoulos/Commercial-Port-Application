from json.encoder import ESCAPE_ASCII
import tkinter as tk
from tkcalendar import DateEntry
import datetime
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

    ROWS_PER_TABLE = 5
    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.search_frame = tk.Frame(self)
        self.search_frame.grid_columnconfigure(list(range(2)), weight=1)
        self.search_frame.grid_columnconfigure(2, weight=2)

        tk.Label(self.search_frame, text="From").grid(sticky=tk.W, padx=10)

        self.from_dateentry = DateEntry(self.search_frame)
        self.from_dateentry.set_date(datetime.date.today() - datetime.timedelta(days=1))
        self.from_dateentry.grid(row=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.search_frame, text="To").grid(row=0, column=1, sticky=tk.W, padx=10)

        self.to_dateentry = DateEntry(self.search_frame)
        self.to_dateentry.set_date(datetime.date.today() + datetime.timedelta(days=7))
        self.to_dateentry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.update)
        self.search_button.grid(row=1, column=2, sticky=tk.NSEW, padx=10, pady=5)

        self.search_frame.pack(anchor=tk.CENTER, fill=tk.X, padx=10, pady=5)

        tk.Label(self, text="Arrivals").pack(anchor=tk.CENTER, pady=10)

        self.arrivals_treeview = ColumnTreeView(self, columns=MovementView.ARRIVALS_COLUMNS,
                                                      id_col=0,
                                                      height=MovementView.ROWS_PER_TABLE)

        self.arrivals_treeview.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=10, pady=5)

        tk.Label(self, text="Departures").pack(anchor=tk.CENTER, pady=10)

        self.departures_treeview = ColumnTreeView(self, columns=MovementView.DEPARTURES_COLUMNS, 
                                                        id_col=0,
                                                        height=MovementView.ROWS_PER_TABLE)

        self.departures_treeview.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER, padx=10, pady=5)


    def update(self):
        self.arrivals_treeview.clear_all_children()
        self.departures_treeview.clear_all_children()

        from_date = self.from_dateentry.get_date()
        to_date   = self.to_dateentry.get_date()

        self.controller.get_arrivals(from_date, to_date, self.arrivals_treeview.insert_to_treeview)
        self.controller.get_departures(from_date, to_date, self.departures_treeview.insert_to_treeview)
