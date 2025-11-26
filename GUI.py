# Author: Thisanga Perera
# IIT ID: 20242008
# UoW ID: 2151959
#Submission date:20.04.2025
# Coursework: Stage 04



import json # Import the JSON module to handle JSON data
import tkinter as tk # Import tkinter for creating the GUI
from tkinter import ttk # For modern themed GUI widgets


# Task class to represent a single task
class Task:
    def __init__(self, name, description, priority, due_date):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    # Convert task object to dictionary for saving
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }

# TaskManager class handles task loading, filtering, and sorting
class TaskManager:
    def __init__(self, json_file='tasks.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks_from_json()

    
    # Load tasks from a JSON file
    def load_tasks_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                task_dicts = json.load(file)
                self.tasks = [Task(**task) for task in task_dicts]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    # Filter tasks by name, priority, and due date
    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered_tasks = self.tasks
        if name_filter:
            filtered_tasks = [task for task in filtered_tasks if name_filter.lower() in task.name.lower()]
        if priority_filter and priority_filter != "all":
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority_filter]
        if due_date_filter:
            filtered_tasks = [task for task in filtered_tasks if due_date_filter in task.due_date]
            
        return filtered_tasks

    
    # Sort tasks by specified field
    def sort_tasks(self, sort_key='name'):
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        if sort_key == 'priority':
            self.tasks.sort(key=lambda x: priority_order.get(x.priority, 4))
        else:
            self.tasks.sort(key=lambda x: getattr(x, sort_key))


# GUI class for the Task Manager
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.task_manager = TaskManager()
        self.sort_order = {}  # Store sort order for each column
        self.setup_gui() # Set up the interface

     # Set up all the GUI widgets
    def setup_gui(self):
        # Header section
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(side="top", fill="x")

        ttk.Label(header_frame, text="Personal Task Manager", font='arial 20 bold').pack(pady=(10, 5))

        # Search and Filter Section
        filter_frame = ttk.LabelFrame(self.root, text="Search and Filter", padding=10)
        filter_frame.pack(padx=10, pady=10, fill="x")

        # Name filter
        ttk.Label(filter_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.name_filter_var).grid(row=0, column=1, padx=5, pady=5)

        # Priority filter
        ttk.Label(filter_frame, text="Priority:").grid(row=0, column=2, padx=5, pady=5)
        self.priority_filter_var = tk.StringVar()
        priority_options = ["all", "high", "medium", "low"]
        ttk.Combobox(filter_frame, textvariable=self.priority_filter_var, values=priority_options, state="readonly").grid(row=0, column=3, padx=5, pady=5)
        self.priority_filter_var.set("all")

        # Due date filter
        ttk.Label(filter_frame, text="Due Date:").grid(row=0, column=4, padx=5, pady=5)
        self.due_date_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.due_date_filter_var).grid(row=0, column=5, padx=5, pady=5)

        # Filter button
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=0, column=6, padx=5, pady=5)

        # Task Display Table
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview widget to show tasks in table format
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Description", "Priority", "Due Date"), show="headings")
        
        # Table headings (clickable for sorting)
        self.tree.heading("Name", text="Name", command=lambda: self.sort_tasks("name"))
        self.tree.heading("Description", text="Description", command=lambda: self.sort_tasks("description"))
        self.tree.heading("Priority", text="Priority", command=lambda: self.sort_tasks("priority"))
        self.tree.heading("Due Date", text="Due Date", command=lambda: self.sort_tasks("due_date"))
        
        # Set column widths
        self.tree.column("Name", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Priority", width=100)
        self.tree.column("Due Date", width=100)
        
        # Show the task table in the window and let it resize with the window
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Adjust layout sizing
        self.root.columnconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Load tasks into the table
        self.populate_tree()

    
    # Load and display filtered tasks in the table
    def populate_tree(self):
        # Clear current rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filtered tasks and add to table
        tasks = self.task_manager.get_filtered_tasks(
            self.name_filter_var.get(),
            self.priority_filter_var.get(),
            self.due_date_filter_var.get()
        )

        
        for task in tasks:
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date))

    # Apply filters and refresh the table
    def apply_filter(self):
        self.populate_tree()

    # Sort table when header clicked
    def sort_tasks(self, sort_key):
        
        # Toggle sorting order
        self.sort_order[sort_key] = not self.sort_order.get(sort_key, False)
        self.task_manager.sort_tasks(sort_key)
        
        # Reverse if needed to toggle ascending/descending
        if self.sort_order[sort_key]:
            self.task_manager.tasks.reverse()
        
         # Refresh the table
        self.populate_tree()


# Start the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()