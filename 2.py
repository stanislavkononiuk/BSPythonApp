import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests

rows=[]
def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        all_links = []
        for link in links:
            href = link.get('href')
            if href:
                all_links.append(href)
        return all_links
    except Exception as e:
        print("Error:", e)
def get_txt_file():
    global data, curr_lines, rows
    try:
        text_file_path = filedialog.askopenfilename(initialdir="./",
                                                    title="Select a File",
                                                    filetypes=(("Text File", "*.txt*"),))
        with open(text_file_path, 'r') as f:
            txt = f.readlines()
            i = 1
            for row_data in txt:
                links = get_all_links(row_data)
                if links!=None:
                    table.insert("", index="end", values=(i, row_data,len(links), links))
                    rows.append(row_data+str(len(links))+str(links))
                else:
                    table.insert("", index="end", values=(i, row_data,'0', ''))
                    rows.append(row_data+'0'+'')
                i = i + 1
            label_txt.config(text=text_file_path)

    except Exception as e:
        print("Error:", e)
def save_txt_file():
    global conn, rows, curr_lines
    try:
        file_path = filedialog.asksaveasfilename(initialdir="./",
                                                title="Save Result",
                                                filetypes=(("Result", "*.txt"),))
        save_txt.config(text=file_path)
        if file_path:
            with open(file_path, "w") as file:
                for row in rows:
                    file.write(row+'\n')

    except Exception as e:
        print("Error:", e)


# Create the main window
window = tk.Tk()

# Create a canvas
canvas = tk.Canvas(window)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame inside the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

top_frame=tk.Frame(frame,width=1400, height=800)
top_frame.grid(row=0,column=0,padx=10,pady=5)

btm_frame=tk.Frame(frame,width=200, height=400)
btm_frame.grid(row=1,column=0,padx=10,pady=5)
# Create a table
table = ttk.Treeview(top_frame)

# Define the columns
table["columns"] = ("No", "url", "count", "sub urls")

# Format the columns
table.column("#0", width=0, stretch=tk.NO)
table.column("No", anchor=tk.W, width=30)
table.column("url", anchor=tk.W, width=250)
table.column("count", anchor=tk.W, width=50)
table.column("sub urls", anchor=tk.W, width=200)

# Create the table headers
table.heading("#0", text="", anchor=tk.W)
table.heading("No", text="No", anchor=tk.W)
table.heading("url", text="url", anchor=tk.W)
table.heading("count", text="count", anchor=tk.CENTER)
table.heading("sub urls", text="sub urls", anchor=tk.W)

# Pack the table into the frame
table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create x-scrollbar
x_scrollbar = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=table.xview)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
table.configure(xscrollcommand=x_scrollbar.set)
# Create y-scrollbar
y_scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=table.yview)
y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
table.configure(yscrollcommand=y_scrollbar.set)

# Create label and button widgets
label_txt = tk.Label(btm_frame, text="Click the button to browse the Text File")
label_txt.grid(row=1,column=1)
txt_button = tk.Button(btm_frame, text="Get Text File", command=get_txt_file)
label_txt.grid(row=1,column=2)

# Pack the label and button widgets
label_txt.pack(side=tk.BOTTOM, pady=5)
txt_button.pack(side=tk.BOTTOM, pady=5)

# Create label and button widgets
save_txt = tk.Label(window, text="Click the button to save the Text File")
save_button = tk.Button(window, text="Save", command=save_txt_file)

# Pack the label and button widgets
save_txt.pack(side=tk.BOTTOM, pady=5)
save_button.pack(side=tk.BOTTOM, pady=5)


# Configure the canvas scrolling
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Run the main window loop
window.mainloop()
