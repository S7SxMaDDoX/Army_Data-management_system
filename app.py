import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import json
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use the resource_path function to access your files
picture1 = resource_path('Picture1.png')
picture2 = resource_path('Picture2.png')
picture3 = resource_path('Picture3.jpg')
picture4 = resource_path('Picture4.jpg')
config = resource_path('config.json')

# Now use these paths in your script where needed


# Load database configuration from the config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Function to create the database and table if they don't exist
def create_table():
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        conn.database = config['database']

        # SQL statement to create the table with dynamic name
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {assessment_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nai_type VARCHAR(250),
            loc VARCHAR(255),
            gr_dsm VARCHAR(255),
            svl_resource VARCHAR(255),
            svl_time_from VARCHAR(255),
            svl_time_to VARCHAR(255),
            svl_tasking_requirements TEXT,
            action_addressee_svl VARCHAR(255),
            svl_coord_instructions TEXT,
            suggested_vectors TEXT,
            assessed_time_frame VARCHAR(255),
            effect_required TEXT,
            action_addressee_tgt VARCHAR(255),
            coord_instructions_tgt TEXT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Inform user or handle success
        print(f"Table '{assessment_name}' created successfully.")

        # After table creation, show the dashboard
        show_dashboard()

    except mysql.connector.Error as error:
        print(f"Error creating table: {error}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def on_next_button_click():
    create_table() 
# Function to show the second page (JOPET)

def show_jopet():
    if username_entry.get() == "pooja" and password_entry.get() == "assessment":
        container.destroy()  # Destroy the container frame to remove images and login form
        jopet_frame.pack(expand=True)
    else:
        messagebox.showwarning("Login Failed", "Invalid username or password.")

# Function to show the dashboard page
def show_dashboard():
    jopet_frame.pack_forget()
    dashboard_frame.pack(expand=True)

# Function to show the new JOPET page with dropdowns
def show_new_jopet():
    dashboard_frame.pack_forget()
    new_jopet_frame.pack(expand=True)

# Function to show the fourth page
def show_more_page():
    svl_info_frame.pack_forget()
    more_page_frame.pack(expand=True)

# Function to go back from the fourth page to the third page
def go_back():
    more_page_frame.pack_forget()
    svl_info_frame.pack(expand=True)

def goo_back():
    new_jopet_frame.pack_forget()
    dashboard_frame.pack(expand=True)

def gooo_back():
    svl_info_frame.pack_forget()
    new_jopet_frame.pack(expand=True)

# Function to show the SVL Information page
def show_svl_info_page():
    new_jopet_frame.pack_forget()
    svl_info_frame.pack(expand=True)

# Function to go back from SVL Information page to More Details page
def go_back_to_more_page():
    svl_info_frame.pack_forget()
    more_page_frame.pack(expand=True)

def go_homepage():
    more_page_frame.pack_forget()
    dashboard_frame.pack(expand=True)

def go_tablepage():
    # Hide dashboard_frame
    dashboard_frame.pack_forget()
    # Pack form_frame_jopet
    form_frame_jopet.pack(fill="both", expand=True)

# Function to submit the form with additional fields
def submit_more_form():
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    # Retrieve form data
    nai_type = nai_type_var.get()
    loc = loc_var.get()
    gr_dsm = gr_dsm_entry.get()
    svl_resource = svl_resource_var.get()
    svl_time_from = svl_time_from_entry.get()
    svl_time_to = svl_time_to_entry.get()
    svl_tasking_requirements = svl_tasking_requirements_entry.get()
    action_addressee_svl = action_addressee_svl_entry.get()
    svl_coord_instructions = svl_coord_instructions_entry.get()
    suggested_vectors = suggested_vectors_entry.get()
    assessed_time_frame = assessed_time_frame_entry.get()
    effect_required = effect_required_entry.get()
    action_addressee_tgt = action_addressee_tgt_entry.get()
    coord_instructions_tgt = coord_instructions_tgt_entry.get()

    # Validation
    if not all([nai_type, loc, gr_dsm, svl_resource]) or nai_type == "Select NAI Type" or loc == "Select LOC" or svl_resource == "Select SVL Resource":
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    # Handle "Add Other" options
    if svl_resource == "Add Other":
        svl_resource = other_svl_resource_entry.get()
    
    if loc == "Add Other":
        loc = other_loc_entry.get()
    
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        
        # Dynamic table name in the INSERT query
        query = f"""
        INSERT INTO {assessment_name} (nai_type, loc, gr_dsm, svl_resource, svl_time_from, svl_time_to, svl_tasking_requirements, action_addressee_svl, svl_coord_instructions, suggested_vectors, assessed_time_frame, effect_required, action_addressee_tgt, coord_instructions_tgt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nai_type, loc, gr_dsm, svl_resource, svl_time_from, svl_time_to, svl_tasking_requirements, action_addressee_svl, svl_coord_instructions, suggested_vectors, assessed_time_frame, effect_required, action_addressee_tgt, coord_instructions_tgt))
        conn.commit()
        
        messagebox.showinfo("Success", "Data submitted successfully.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Function to toggle visibility of 'Other SVL Resource' entry
def toggle_other_svl_resource(*args):
    if svl_resource_var.get() == "Add Other":
        other_svl_resource_label.pack(pady=5)
        other_svl_resource_entry.pack(pady=10)
    else:
        other_svl_resource_label.pack_forget()
        other_svl_resource_entry.pack_forget()

# Function to toggle visibility of 'Other LOC' entry
def toggle_other_loc(*args):
    if loc_var.get() == "Add Other":
        other_loc_label.pack(pady=5)
        other_loc_entry.pack(pady=10)
    else:
        other_loc_label.pack_forget()
        other_loc_entry.pack_forget()

# Function to fetch and show assessment data
def fetch_and_show_data():
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        
        # Dynamic table name in the SELECT query
        cursor.execute(f"SELECT * FROM {assessment_name}")
        rows = cursor.fetchall()
        
        if rows:
            display_data(rows)  # Function to display data (implement according to your UI)
        else:
            messagebox.showinfo("No Data", f"No data available in the table '{assessment_name}'.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Function to display data in a new window
def display_data(rows):
    def on_double_click(event):
        item = tree.selection()[0]
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)

        col_index = int(column.replace('#', '')) - 1
        row_index = tree.index(item)
        
        selected_value = tree.item(item, 'values')[col_index]
        
        entry = tk.Entry(data_window)
        entry.insert(0, selected_value)
        entry.bind("<Return>", lambda e: update_value(entry, row_index, col_index, item))
        entry.place(x=event.x, y=event.y)
        entry.focus_set()

    def update_value(entry, row_index, col_index, item):
        new_value = entry.get()
        entry.destroy()
        
        current_values = list(tree.item(item, 'values'))
        current_values[col_index] = new_value
        tree.item(item, values=current_values)
        
        update_database(row_index, col_index, new_value)
        
    def update_database(row_index, col_index, new_value):
        # Retrieve the assessment name from the entry box
        assessment_name = assessment_entry.get()
        try:
            conn = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            cursor = conn.cursor()
            
            columns = ("id", "nai_type", "loc", "gr_dsm", "svl_resource", "svl_time_from", "svl_time_to", "svl_tasking_requirements", "action_addressee_svl", "svl_coord_instructions", "suggested_vectors", "assessed_time_frame", "effect_required", "action_addressee_tgt", "coord_instructions_tgt")
            row_id = rows[row_index][0]
            column_name = columns[col_index]
            
            update_query = f"UPDATE {assessment_name} SET {column_name} = %s WHERE id = %s"
            cursor.execute(update_query, (new_value, row_id))
            conn.commit()
            
            messagebox.showinfo("Success", "Data updated successfully.")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        
        finally:
            cursor.close()
            conn.close()
    
    # Create a new Toplevel window for displaying data
    data_window = tk.Toplevel(root)
    
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()
    
    # Set the title of the window to the assessment name
    data_window.title(f"Assessment Carried Out By: {assessment_name}")
    data_window.geometry("800x400")
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12), rowheight=25, borderwidth=2, relief="solid" )
    # Define columns for the Treeview
    columns = ("id", "nai_type", "loc", "gr_dsm", "svl_resource", "svl_time_from", "svl_time_to", "svl_tasking_requirements", "action_addressee_svl", "svl_coord_instructions", "suggested_vectors", "assessed_time_frame", "effect_required", "action_addressee_tgt", "coord_instructions_tgt")
    
    # Create Treeview widget
    
    global tree  # Declare tree as global to make it accessible inside nested functions
    tree = ttk.Treeview(data_window, columns=columns, show="headings")
    
    # Set headings for columns
    for col in columns:
        tree.heading(col, text=col)
    
    # Insert data rows into the Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    # Pack the Treeview widget
    tree.pack(expand=True, fill='both')
    
    # Bind double-click event to the Treeview
    tree.bind("<Double-1>", on_double_click)

def fetch():
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        
        # Dynamic table name in the SELECT query and specific columns
        cursor.execute(f"SELECT nai_type,svl_resource, svl_time_from, svl_time_to, svl_tasking_requirements, action_addressee_svl, svl_coord_instructions FROM {assessment_name}")
        rows = cursor.fetchall()
        
        if rows:
            display_sopet_data(rows)  # Function to display data (implement according to your UI)
        else:
            messagebox.showinfo("No Data", f"No data available in the table '{assessment_name}'.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()
        
def display_sopet_data(rows):
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    sopet_window = tk.Toplevel(root)
    sopet_window.title(f"SOPET Data Of : {assessment_name}")  # Set title dynamically
    sopet_window.geometry("800x400")

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12), rowheight=25, borderwidth=2, relief="solid" )
    columns = ("NAI Type", "SVL Resource", "SVL Time From", "SVL Time To", "SVL Tasking Requirements", "Action Addressee (SVL)", "SVL Coord Instructions")
    tree = ttk.Treeview(sopet_window, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
    
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.pack(expand=True, fill='both')

def catch():
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        cursor = conn.cursor()
        
        # Dynamic table name in the SELECT query and specific columns
        cursor.execute(f"SELECT nai_type, suggested_vectors, assessed_time_frame, effect_required, action_addressee_tgt, coord_instructions_tgt FROM {assessment_name}")
        rows = cursor.fetchall()
        
        if rows:
            display_topet_data(rows)  # Function to display data in Treeview
        else:
            messagebox.showinfo("No Data", f"No TOPET data available in the table '{assessment_name}'.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Function to display TOPET data in a Treeview widget
def display_topet_data(rows):
    # Retrieve the assessment name from the entry box
    assessment_name = assessment_entry.get()

    topet_window = tk.Toplevel()
    topet_window.title(f"TOPET Data Of : {assessment_name}")  # Set title dynamically
    topet_window.geometry("800x400")

    # Create a style for the Treeview to configure the appearance
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12), rowheight=25, borderwidth=2, relief="solid" )

    columns = ("NAI Type", "Suggested Vectors", "Assessed Time Frame", "Effect Required", "Action Addressee (TGT)", "Coord Instructions (TGT)")
    tree = ttk.Treeview(topet_window, columns=columns, show="headings", style="Treeview")

    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)

    # Insert data rows into the Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Pack the Treeview widget
    tree.pack(expand=True, fill='both')
# Create the main application window
root = tk.Tk()
root.title(" JT OPERATIONAL PLG & EXECUTION TABLE ")
root.configure(bg='white')

# Set the window to a reasonable size and center it on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Create and place the frames
jopet_frame = tk.Frame(root, bg='white')
dashboard_frame = tk.Frame(root, bg='white')
new_jopet_frame = tk.Frame(root, bg='white')
svl_info_frame = tk.Frame(root, bg='white')
more_page_frame = tk.Frame(root, bg='white')

# Login Frame

container = tk.Frame(root, bg="white", relief=tk.RAISED)
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Update paths to images
image1_path = os.path.join(current_dir, "Picture1.png")
image2_path = os.path.join(current_dir, "Picture2.png")
image3_path = os.path.join(current_dir, "Picture3.jpg")
image4_path = os.path.join(current_dir, "Picture4.jpg")

# Load images using the updated paths
image1 = Image.open(image1_path)
image1 = ImageTk.PhotoImage(image1)
image1_label = tk.Label(container, image=image1, bg="white")
image1_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

image2 = Image.open(image2_path)
image2 = ImageTk.PhotoImage(image2)
image2_label = tk.Label(container, image=image2, bg="white")
image2_label.grid(row=1, column=0, pady=10, padx=10, sticky="n")

image3 = Image.open(image3_path)
image3 = ImageTk.PhotoImage(image3)
image3_label = tk.Label(container, image=image3, bg="white")
image3_label.grid(row=0, column=2, pady=10, padx=10, sticky="n")

image4 = Image.open(image4_path)
image4 = ImageTk.PhotoImage(image4)
image4_label = tk.Label(container, image=image4, bg="white")
image4_label.grid(row=1, column=2, pady=10, padx=10, sticky="n")

form_frame = tk.Frame(container, bg="white")
form_frame.grid(row=0, column=1, rowspan=2, pady=10, padx=10)
title_label = tk.Label(form_frame, text="Login", fg="forest green", font=("Arial", 24, "bold"), bg="white")
title_label.pack(pady=10)

username_label = tk.Label(form_frame, text="Username:", bg="white", font=("Arial", 12) )
username_label.pack()
username_entry = tk.Entry(form_frame,  highlightbackground="green", highlightthickness=2, bd=0, font=("Arial", 14) , width=20)
username_entry.pack(pady=5)

password_label = tk.Label(form_frame, text="Password:", bg="white",font=("Arial", 12))
password_label.pack()
password_entry = tk.Entry(form_frame, highlightbackground="green", highlightthickness=2, bd=0, show='*', font=("Arial", 14) , width=20)
password_entry.pack(pady=5)

login_button = tk.Button(form_frame, text="Login", command=show_jopet, bg="forest green", fg="white", bd=0, padx=20, pady=10)
login_button.pack(pady=10)

# Create the JOPET frame
jopet_frame = tk.Frame(root, bg="white")

# Place images in jopet_frame
image1_label_jopet = tk.Label(jopet_frame, image=image1, bg="white")
image1_label_jopet.grid(row=0, column=0, pady=10, padx=10, sticky="n")

image2_label_jopet = tk.Label(jopet_frame, image=image2, bg="white")
image2_label_jopet.grid(row=1, column=0, pady=10, padx=10, sticky="n")

image3_label_jopet = tk.Label(jopet_frame, image=image3, bg="white")
image3_label_jopet.grid(row=0, column=2, pady=10, padx=10, sticky="n")

image4_label_jopet = tk.Label(jopet_frame, image=image4, bg="white")
image4_label_jopet.grid(row=1, column=2, pady=10, padx=10, sticky="n")

form_frame_jopet = tk.Frame(jopet_frame, bg="white")
form_frame_jopet.grid(row=0, column=1, rowspan=2, pady=10, padx=10)




#page three
tk.Label(form_frame_jopet, text="JT OPERATIONAL PLG & EXECUTION TABLE ", bg='white', fg='green', font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(form_frame_jopet, text="Assessment carried out by", bg='white' , font=("Arial", 16)).pack(pady=5)
assessment_entry = tk.Entry(form_frame_jopet, highlightbackground="green", highlightthickness=2, bd=0 , width=20 , font=("Arial", 16))
assessment_entry.pack(pady=10)
tk.Label(form_frame_jopet, text="Name of Apch:", bg='white', font=("Arial", 16)).pack(pady=5)
apch_entry = tk.Entry(form_frame_jopet, highlightbackground="green", highlightthickness=2, bd=0, font=("Arial", 16), width=20 )
apch_entry.pack(pady=10)
tk.Label(form_frame_jopet, text="Location:", bg='white', font=("Arial", 16)).pack(pady=5)
loc_entry = tk.Entry(form_frame_jopet, highlightbackground="green", highlightthickness=2, bd=0, font=("Arial", 16), width=20 )
loc_entry.pack(pady=10)
tk.Label(form_frame_jopet, text="Level:", bg='white', font=("Arial", 16)).pack(pady=5)
level_var = tk.StringVar()
level_options = ["Select Level", "BN", "COY", "BDE"]
level_menu = ttk.Combobox(form_frame_jopet, textvariable=level_var, values=level_options, font=("Arial", 16), width=20 )
level_menu.pack(pady=10)
level_menu.current(0)
tk.Button(form_frame_jopet, text="Next", command=on_next_button_click, bg='green', fg='white', width=10, height=2).pack(pady=20)

# Start with the container frame visible
container.pack(fill="both", expand=True)



# Dashboard Frame
tk.Label(dashboard_frame, text="JOPET", bg='white', fg='green', font=("Arial", 24, "bold")).pack(pady=2)

tk.Button(dashboard_frame, text="ADD APPROACH", command=show_new_jopet, bg='green', fg='white',width=15, height=2 , font=("Arial", 10, "bold")).pack(pady=20 , padx=30)
tk.Button(dashboard_frame, text="EDIT APPROACH", command=fetch_and_show_data, bg='green', fg='white',width=15, height=2 ,font=("Arial", 10, "bold")).pack(pady=20 , padx=30)
tk.Button(dashboard_frame, text="SOPET TABLE", bg='green', fg='white', command=fetch,width=15, height=2 ,font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=30)
tk.Button(dashboard_frame, text="TOPET TABLE", bg='green', fg='white',command=catch,width=15, height=2,font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=30)
# tk.Button(dashboard_frame, text="  Back  ", command=go_tablepage, bg='green', fg='white',width=15, height=1 ,font=("Arial", 10, "bold")).pack(pady=20 , padx=30)

# New JOPET Frame with dropdowns
tk.Label(new_jopet_frame, text="NEW APPROACH", bg='white', fg='green', font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(new_jopet_frame, text="NAI Type:", bg='white', font=("Arial", 16)).pack(pady=5)
nai_type_var = tk.StringVar()
nai_type_options = ["Select Nai type", 'Stg A', 'Stg A', 'Rear CP', 'Base CP', 'Advance CP', 'Amn / FOL / Lgs Dump', 'Helipads',
    'Attk Heptrs (FARRPs)', 'UAV base', 'AD Sys (SAM Sites)', 'Gun A / Dply Space (Arty)', 
    'PLA EW Dets', 'Debussing Pt', 'Assy As / FAA', 'Rel Pt (RP)', 'OPs', 'Rdr Stns / Radome Stns', 
    'Com Cens', 'Choke Pt / Br', 'Billeting Area / PLA Camp', 'Air',"Add Other"]
nai_type_menu = ttk.Combobox(new_jopet_frame, textvariable=nai_type_var, values=nai_type_options, font=("Arial", 16), width=20)
nai_type_menu.pack(pady=10)
nai_type_menu.current(0)
tk.Label(new_jopet_frame, text="LOC:", bg='white', font=("Arial", 16)).pack(pady=5)
loc_var = tk.StringVar()
loc_options = ["Select LOC ","Yebi", "Tsethang", "D Gonpa", "Kyeo", "Gen", "Niuqu", "Tsona Dz", "Tre", "Gytsum", "Lambu", "Y Jn", "Chiu Tso",
    "Rong", "Nyapa", "Tsona Dz East", "Tsona Dz West", "Y Jn East", "Kechen La", "Nagdoh", "Gongkar Dz", "Serche",
    "Tsona Dz North", "Luogong", "Tre East", "Lambu South", "Y Jn North", "North of Fwd PP", "North of Mera La",
    "NW of Fwd PP", "Tsona Dz High Grnd", "Lambu Spur", "Tsona Dz Open Patch", "Lhasa", "Garpuk", "Gyelung La",
    "Shou Chu Nala Jn", "Y Jn Open Area", "Y Jn Bowl", "Lambu Grove", "Add Other"]
loc_menu = ttk.Combobox(new_jopet_frame, textvariable=loc_var, values=loc_options, font=("Arial", 16), width=20)
loc_menu.pack(pady=10)
loc_menu.current(0)
tk.Label(new_jopet_frame, text="GR DSM:", bg='white', font=("Arial", 16)).pack(pady=5)
gr_dsm_entry = tk.Entry(new_jopet_frame,highlightbackground="green", highlightthickness=2, bd=0, font=("Arial", 16), width=20)
gr_dsm_entry.pack(pady=10)
other_loc_label = tk.Label(new_jopet_frame, text="Other LOC:", bg='white', font=("Arial", 16))
other_loc_entry = tk.Entry(new_jopet_frame,highlightbackground="green", highlightthickness=2, bd=0, font=("Arial", 16), width=20)
tk.Button(new_jopet_frame, text="Back", command=goo_back, bg='green', fg='white',width=10, height=2).pack(side=tk.LEFT,padx=20)
tk.Button(new_jopet_frame, text="Next", command=show_svl_info_page, bg='green', fg='white',width=10, height=2).pack(side=tk.LEFT,padx=20)

# SVL Information Frame
tk.Label(svl_info_frame, text="SVL Information", bg='white', fg='green', font=("Arial", 14, "bold")).pack(pady=20)
tk.Label(svl_info_frame, text="SVL Time From:", bg='white', font=("Arial", 12)).pack(pady=5)
svl_time_from_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))
svl_time_from_entry.pack(pady=10)
tk.Label(svl_info_frame, text="SVL Time To:", bg='white', font=("Arial", 12)).pack(pady=5)
svl_time_to_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))
svl_time_to_entry.pack(pady=10)
tk.Label(svl_info_frame, text="SVL Tasking Requirements:", bg='white', font=("Arial", 12)).pack(pady=5)
svl_tasking_requirements_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))
svl_tasking_requirements_entry.pack(pady=10)
tk.Label(svl_info_frame, text="Action Addressee (SVL):", bg='white', font=("Arial", 12)).pack(pady=5)
action_addressee_svl_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))
action_addressee_svl_entry.pack(pady=10)
tk.Label(svl_info_frame, text="SVL Coordination Instructions:", bg='white', font=("Arial", 12)).pack(pady=5)
svl_coord_instructions_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))
svl_coord_instructions_entry.pack(pady=10)
tk.Label(svl_info_frame, text="SVL Resource:", bg='white', font=("Arial", 12)).pack(pady=5)
svl_resource_var = tk.StringVar()
svl_resource_options = ["Select SVL resources","Satl, RPA, EW (DF)", "Satl, RPA, SF, EW (DF)", "Scouts, LORROS, PR Msns, EW (DF)",
    "Scouts, LORROS, PR Msns", "Satl, RPA, Scouts, PR Msns", "Satl, RPA, Scouts, PR Msns",
    "Satl, RPA, EW (DF)", "Satl, RPA, Scouts, PR Msns, EW (DF), SF",
    "Satl, RPA, Scouts, PR Msns, SF, Scouts", "TBPs, Scouts, Tac RPA, EW (DF)",
    "TBPs, Scouts, Tac RPA, EW (DF) TBPs, Scouts, Tac RPA, EW (DF) OPs, TBPs, Scouts, SF", "Add Other"]
svl_resource_menu = ttk.Combobox(svl_info_frame, textvariable=svl_resource_var, values=svl_resource_options, width=16 , font=("Arial", 12))
svl_resource_menu.pack(pady=10)
svl_resource_menu.current(0)
other_svl_resource_label = tk.Label(svl_info_frame, text="Other SVL Resource:", font=("Arial", 12) ,bg='white')
other_svl_resource_entry = tk.Entry(svl_info_frame,highlightbackground="green", highlightthickness=2, bd=0, width=18 , font=("Arial", 12))

# Place Next and Back buttons in the same row
button_frame = tk.Frame(svl_info_frame, bg='white')
button_frame.pack(pady=20)
tk.Button(button_frame, text="Back", command=gooo_back, bg='green', fg='white' ,width=15).pack(side=tk.LEFT, padx=20)
tk.Button(button_frame, text="Next", command=show_more_page, bg='green', fg='white',width=15).pack(side=tk.LEFT, padx=20)


# More Page Frame with additional fields
tk.Label(more_page_frame, text="More Details", bg='white', fg='green', font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(more_page_frame, text="Assessed Time Frame:", bg='white', font=("Arial", 14)).pack(pady=5)
assessed_time_frame_entry = tk.Entry(more_page_frame,highlightbackground="green", highlightthickness=2, bd=0, width=20 , font=("Arial", 14))
assessed_time_frame_entry.pack(pady=10)
tk.Label(more_page_frame, text="suggested_vectors:", bg='white', font=("Arial", 14)).pack(pady=5)
suggested_vectors_entry = tk.Entry(more_page_frame,highlightbackground="green", highlightthickness=2, bd=0, width=20 , font=("Arial", 14))
suggested_vectors_entry.pack(pady=10)   
tk.Label(more_page_frame, text="Effect Required:", bg='white', font=("Arial", 14)).pack(pady=5)
effect_required_entry = tk.Entry(more_page_frame,highlightbackground="green", highlightthickness=2, bd=0, width=20 , font=("Arial", 14))
effect_required_entry.pack(pady=10)
tk.Label(more_page_frame, text="Action Addressee (TGT):", bg='white', font=("Arial", 14)).pack(pady=5)
action_addressee_tgt_entry = tk.Entry(more_page_frame,highlightbackground="green", highlightthickness=2, bd=0, width=20 , font=("Arial", 14))
action_addressee_tgt_entry.pack(pady=10)
tk.Label(more_page_frame, text="Coordination Instructions (TGT):", bg='white', font=("Arial", 14)).pack(pady=5)
coord_instructions_tgt_entry = tk.Entry(more_page_frame,highlightbackground="green", highlightthickness=2, bd=0 , width=20 , font=("Arial", 14))
coord_instructions_tgt_entry.pack(pady=10)

# Place Next and Back buttons in the same row
button_frame_more = tk.Frame(more_page_frame, bg='white')
button_frame_more.pack(pady=20)
tk.Button(button_frame_more, text="HOME", command=go_homepage, bg='green', fg='white' , width=10, height=1).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame_more, text="Back", command=go_back, bg='green', fg='white', width=10, height=1).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame_more, text="Submit", command=submit_more_form, bg='green', fg='white' ,width=10, height=1).pack(side=tk.LEFT, padx=10)
# Bind dropdown change events
svl_resource_var.trace('w', toggle_other_svl_resource)
loc_var.trace('w', toggle_other_loc)

# Call the function to create the table on startup
create_table()

# Start the application
root.mainloop()
