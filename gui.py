from tkinter import *
from tkinter import filedialog
from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
from urllib.parse import urlparse
import os
import sqlite3
import time
  
# Function for opening the
# file explorer window
conn,curr_lines,curr_rows = None,None,None
data=[]
filecounts=0

db_name = 'text_data'
def create_empty_df():
    global db_name
    try:
        the_folder = fd.askdirectory(title = "Select a Folder where DB file needs to be created")
        conn = sqlite3.connect(the_folder+f'/{db_name}.db')
        db_creation.config(text=f"created")
        conn.close()
    except Exception as e:
            label_error.config(text = e)

def get_db_file():
    global conn,curr_rows,curr_lines
    try:
        db_path = filedialog.askopenfilename(initialdir = "./",
                                            title = "Select a File",
                                            filetypes = (("SQL file","*.db*"),))
        
        if len(db_path) > 0:
            conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS data (text VARCHAR(255)  ,PRIMARY KEY (text))")
        cursor = conn.execute("SELECT count(*) from data;")
        rows = None
        for row in cursor:
            rows = row[0]
        curr_rows = rows
        label_db.config(text = db_path)
        label_db_lines.config(text=f"Rows : {str(rows)}")
        if curr_lines:
            label_status.config(text = f"Adding {abs(curr_lines)} Rows")
    except Exception as e:
            label_error.config(text = e)

def get_txt_file():
    global data,curr_lines,curr_rows
    try:
        text_file_path = filedialog.askopenfilename(initialdir = "./",
                                            title = "Select a File",
                                            filetypes = (("Text File","*.txt*"),))
        with open(text_file_path,'r') as f:
            txt = f.readlines()
        
        txt = [x.replace('\n','') for x in txt]
        curr_lines = len(txt)
        data = [x for x in zip(*[iter(txt)])]
        label_txt.config(text = text_file_path)
        label_txt_lines.config(text = f"Lines : {str(curr_lines)}")
        if curr_rows:
            label_status.config(text = f"Adding {abs(curr_lines)} Rows")
    except Exception as e:
            label_error.config(text = e)
def process_txt_file(text_file_path):
    global data,curr_lines,curr_rows
    try:
        # text_file_path = filedialog.askopenfilename(initialdir = "./",
        #                                     title = "Select a File",
        #                                     filetypes = (("Text File","*.txt*"),))
        with open(text_file_path,'r') as f:
            txt = f.readlines()
        
        txt = [x.replace('\n','') for x in txt]
        curr_lines = len(txt)
        data.append([x for x in zip(*[iter(txt)])])
        # data.extend([x for x in zip(*[iter(txt)])])
        # label_txt.config(text = text_file_path)
        # label_txt_lines.config(text = f"Lines : {str(curr_lines)}")
        # if curr_rows:
        #     label_status.config(text = f"Adding {abs(curr_lines)} Rows")
    except Exception as e:
            label_error.config(text = e)
def get_dir():
    global conn,data,curr_lines,curr_rows,filecounts
    try:
        folder_path = filedialog.askdirectory(initialdir = "./",
                                            title = "Select a directory")
        print("Selected folder:", folder_path)
        label_dir.config(text = folder_path)
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                filecounts = filecounts + 1
                try:
                    process_txt_file(file_path)
                    # print(file_path," is processed")
                    # with open(file_path, "r") as file:
                    #     contents = file.read()
                    #     print("File:", filename)
                    #     print(contents)
                    #     print("--------------------")
                except FileNotFoundError:
                    print("File not found.")
                except IOError:
                    print("Error reading the file.")
        # print("counts :", filecounts)
        label_filecounts.config(text=f"Text file counts : {str(filecounts)}")
        # print('data:',data)
    except Exception as e:
        label_error.config(text = e)
def Add_Rows():
    global conn,data,curr_lines,curr_rows    
    i=0
    try:
        for item in data:
            i=i+1
            if conn and item:
                stmt = "INSERT OR IGNORE INTO data (text) VALUES (?)"
                conn.executemany(stmt, item)
                
                # print('In add:',item)                
                conn.commit()
                
                cursor = conn.execute("SELECT count(*) from data;")
                rows = None
                for row in cursor:
                    rows = row[0]
                
                
                label_status.config(text = f"Added {abs(rows-curr_rows)} Rows")
                label_db_lines.config(text=f"Rows : {str(rows)}")
                label_duplicates.config(text=f"Duplicate Rows : {abs(curr_lines-(rows-curr_rows))}")
                curr_rows = rows
                
            else:
                label_status.config(text = 'no conn or txt')
            time.sleep(2)
            progress_bar["value"] += 100/filecounts
            label_processed.config(text=f"Processed : {str(i)}")
            # print("aaaaaaa",progress_bar["value"])
            window.update() 
    except Exception as e:
            label_error.config(text = e)
                                                                                                  
def save_dns_file():
    global conn,curr_rows,curr_lines
    try:
        file_path = filedialog.asksaveasfilename(initialdir = "./",
                                            title = "Export DNS",
                                            filetypes = (("DNS","*.txt"),))  
        label_dns.config(text = file_path)
        if file_path and conn:
            # Open the selected file in write mode
            urls=conn.execute("SELECT * from data;")
            rows=urls.fetchall()       
            # for row in rows:
            #     print("row:",row[0].replace("('",""))     
            with open(file_path, "w") as file:
                for row in rows:
                    parsed_url = urlparse(row[0])
                    domain = parsed_url.netloc
                    file.write(domain+'\n')
        label_expstatus.config(text=f"Exported : Success")
    except Exception as e:
            label_error.config(text = e)
            label_expstatus.config(text=f"Exported : Failed")
# Create the root window
window = Tk()
  
# Set window title
window.title('Add in DB')

# Set window size
window.geometry("800x200")
  
#Set window background color
window.config(background = "white")
  
      
db_button = Button(window,text = "Get Database",command = get_db_file)
# txt_button = Button(window,text = "Get Text File",command = get_txt_file)
dir_button = Button(window,text = "Select Folder",command = get_dir)
Add = Button(window, text='Add Rows', width=25, command=Add_Rows)
create_db = Button(window, text='Create new db', width=25, command=create_empty_df)

label_db=Label(window, text="Click the button to browse the Database file")
label_db.grid(column = 1, row = 2)
# label_txt=Label(window, text="Click the button to browse the Text File")
# label_txt.grid(column = 1, row = 3)

label_db_lines=Label(window, text="Rows : None")
label_db_lines.grid(column = 3, row = 2)
label_processed=Label(window, text="Processed : None")
label_processed.grid(column = 3, row = 4)


db_creation=Label(window, text="Not Required, Not created")
db_creation.grid(column = 2, row = 1)

db_button.grid(column = 2, row = 2)
# txt_button.grid(column = 2, row = 3)
dir_button.grid(column = 2, row = 3)
label_dir=Label(window, text="Click the button to select folder")
label_dir.grid(column = 1, row = 3)
label_filecounts=Label(window, text="Text file counts : None")
label_filecounts.grid(column = 3, row = 3,padx=30)


progress_bar = ttk.Progressbar( orient="horizontal", length=150, mode="determinate")
progress_bar.grid(row=4, column=1)
Add.grid(column = 2, row = 4)
create_db.grid(column = 1, row = 1)


exp_button = Button(window,text = "Export Domains",command = save_dns_file)
exp_button.grid(column = 2, row = 5)
label_dns=Label(window, text="Click the button to export DNS to file")
label_dns.grid(column = 1, row = 5)
label_expstatus=Label(window, text="Exported : None")
label_expstatus.grid(column = 3, row = 5)



label_status=Label(window, text="Status : None")
label_status.grid(column = 1, row = 6)

label_duplicates=Label(window, text="Duplicate Rows : None")
label_duplicates.grid(column = 1, row = 7)

label_error=Label(window, text="Error : None")
label_error.grid(column = 1, row = 9)

# Let the window wait for any events
def on_closing():
    global conn
    try:
        conn.close()
    except:
        pass
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()