import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class EmployeesView(ControllerAwareFrame):

    COLUMNS = (
        "First Name",
        "Last Name",
        "Salary",
        "Shift Starts",
        "Shift Finishes"
    )

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)

        self.employee_view = ColumnTreeView(self, columns=EmployeesView.COLUMNS, 
                                                  updater=self.controller.get_employees)
        
        self.employee_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
