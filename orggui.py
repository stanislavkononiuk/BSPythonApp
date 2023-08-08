from tkinter import *
from tkinter import filedialog
from tkinter import filedialog as fd
import sqlite3
  
# Function for opening the
# file explorer window
conn,data,curr_lines,curr_rows = None,None,None,None
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

def Add_Rows():
    global conn,data,curr_lines,curr_rows
    try:
        if conn and data:
            stmt = "INSERT OR IGNORE INTO data (text) VALUES (?)"
            conn.executemany(stmt, data)
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
    except Exception as e:
            label_error.config(text = e)
                                                                                                  
# Create the root window
window = Tk()
  
# Set window title
window.title('Add in DB')

# Set window size
window.geometry("600x200")
  
#Set window background color
window.config(background = "white")
  
      
db_button = Button(window,text = "Get Database",command = get_db_file)
txt_button = Button(window,text = "Get Text File",command = get_txt_file)
Add = Button(window, text='Add Rows', width=25, command=Add_Rows)
create_db = Button(window, text='Create new db', width=25, command=create_empty_df)

label_db=Label(window, text="Click the button to browse the Database file")
label_db.grid(column = 1, row = 2)
label_txt=Label(window, text="Click the button to browse the Text File")
label_txt.grid(column = 1, row = 3)

label_db_lines=Label(window, text="Rows : None")
label_db_lines.grid(column = 3, row = 2)
label_txt_lines=Label(window, text="Lines : None")
label_txt_lines.grid(column = 3, row = 3)


db_creation=Label(window, text="Not Required, Not created")
db_creation.grid(column = 2, row = 1)

db_button.grid(column = 2, row = 2)
txt_button.grid(column = 2, row = 3)
Add.grid(column = 1, row = 4)
create_db.grid(column = 1, row = 1)

label_status=Label(window, text="Status : None")
label_status.grid(column = 1, row = 5)

label_duplicates=Label(window, text="Duplicate Rows : None")
label_duplicates.grid(column = 1, row = 6)

label_error=Label(window, text="Error : None")
label_error.grid(column = 1, row = 8)

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