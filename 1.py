import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()

# Create a table
table = ttk.Treeview(window)

# Define the columns
table["columns"] = ("No", "url", "count")

# Format the columns
table.column("#0", width=0, stretch=tk.NO)
table.column("No", anchor=tk.W, width=30)
table.column("url", anchor=tk.CENTER, width=50)
table.column("count", anchor=tk.W, width=100)

# Create the table headers
table.heading("#0", text="", anchor=tk.W)
table.heading("No", text="No", anchor=tk.W)
table.heading("url", text="url", anchor=tk.CENTER)
table.heading("count", text="count", anchor=tk.W)

# Add rows to the table
table.insert(parent="", index="end", values=("John", 25, "New York"))
table.insert(parent="", index="end", values=("Alice", 30, "London"))
table.insert(parent="", index="end", values=("Bob", 35, "Paris"))

# Pack the table into the window
table.pack()

# Run the main window loop
window.mainloop()
