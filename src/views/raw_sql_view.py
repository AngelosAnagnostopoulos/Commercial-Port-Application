import tkinter as tk
from .utilities import ControllerAwareFrame, ColumnTreeView

class RawSQLView(ControllerAwareFrame):

    def __init__(self, controller, master, **cfg):
        super().__init__(controller, master, **cfg)
    
        tk.Label(self, text="MySQL Query").pack(fill=tk.X, padx=10, pady=10, anchor=tk.W)

        self.query_textbox = tk.Text(self, height=3)
        self.query_textbox.pack(fill=tk.X, padx=10, pady=10)

        self.execute_query_button = tk.Button(self, text="Execute SQL", command=self.execute)
        self.execute_query_button.pack(fill=tk.X, anchor=tk.CENTER, padx=10, pady=10)

        self.columns = None
        self.treeview = None

    
    def create_treeview(self, columns):
        self.columns = columns

        if self.treeview:
            self.treeview.destroy()

        self.treeview = ColumnTreeView(self, self.columns, None)
        self.treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def treeview_dispatch(self, data):
        if self.treeview:
            self.treeview.insert_to_treeview(data)

    def execute(self):
        answer = tk.messagebox.askokcancel("Warning", 
                                           "This should be used only for demonstration purposes.\nClick OK to continue.", 
                                            icon=tk.messagebox.WARNING)

        if answer:
            query = self.query_textbox.get("1.0", tk.END).strip()

            self.controller.execute_raw_sql(query, self.treeview_dispatch, self.create_treeview)
            
