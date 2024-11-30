from tkinter import *
from tkinter import ttk, messagebox
import mysql
import gen_sql_connection


def patient_dashboard(self, username):
    # Clear the root window
    for widget in self.root.winfo_children():
        widget.destroy()

    # Title
    lbl_title = Label(self.root, text="Patient Dashboard", font=("Arial", 24, "bold"), bg="darkblue", fg="white")
    lbl_title.pack(side=TOP, fill=X)

    # Frame for patient details
    details_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
    details_frame.place(x=50, y=100, width=1400, height=300)

    lbl_details = Label(details_frame, text="Patient Details", font=("Arial", 18, "bold"), bg="white", fg="black")
    lbl_details.pack(side=TOP, pady=10)

    # Query patient details
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="replaceme",
            password="password",  # Update as needed
            database="hospital_db"
        )
        cursor = conn.cursor()

        # Query to fetch patient information
        query = """
            SELECT p.fname, p.lname, p.dob, p.phone, p.email, p.postal_code
            FROM patient p
            INNER JOIN admin a ON a.patient_id = p.patient_id
            WHERE a.username = %s
        """
        cursor.execute(query, (username,))
        patient_info = cursor.fetchone()
        conn.close()

        if patient_info:
            # Display patient details
            details_text = f"""
            Name: {patient_info[0]} {patient_info[1]}
            Date of Birth: {patient_info[2]}
            Phone: {patient_info[3]}
            Email: {patient_info[4]}
            Postal Code: {patient_info[5]}
            """
            lbl_patient_info = Label(details_frame, text=details_text, font=("Arial", 14), bg="white", fg="black",
                                     justify=LEFT)
            lbl_patient_info.pack(pady=10, anchor="w")
        else:
            lbl_error = Label(details_frame, text="No patient details found.", font=("Arial", 14), bg="white", fg="red")
            lbl_error.pack(pady=10)
        btn_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
        btn_frame.place(x=250, y=450, width=1000, height=100)  # Slightly shifted to center

        Button(btn_frame, text="View Appointments", font=("Arial", 16, "bold"), bg="blue", fg="white", width=15,
               command=lambda: self.view_appointments_patient(username)).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="View Prescriptions", font=("Arial", 16, "bold"), bg="green", fg="white", width=15,
               command=lambda: self.view_prescriptions_patient(username)).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="View Procedures", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15,
               command=lambda: self.view_procedures_patient(username)).pack(side=LEFT, padx=20, pady=10)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")


def view_appointments_patient(self, username):
    view_win = Toplevel(self.root)
    view_win.title("View Appointment Records")
    view_win.geometry("1000x600")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="replaceme",
            password="password",  # Update as needed
            database="hospital_db"
        )
        cursor = conn.cursor(buffered=False)
        cursor.callproc('view_appts', (username,))
        for result in cursor.stored_results():
            appts = result.fetchall()
        conn.close()
        notebook = ttk.Notebook(view_win)
        notebook.pack(fill="both", expand=True)
        # Tabs Placeholder
        tabs = {"Appointments": None}
        appointment_columns = ['Date', 'Time', 'Reason', 'Priority', 'Doctor', 'Nurse']

        for tab_name, tab_frame in tabs.items():
            if tab_frame:
                notebook.forget(tab_frame)
        for tab_name in tabs.keys():
            tabs[tab_name] = ttk.Frame(notebook)
            notebook.add(tabs[tab_name], text=tab_name)
        # Frame for Treeview
        tree_frame = Frame(tabs["Appointments"], padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True)

        # Treeview for displaying data
        tree = ttk.Treeview(tree_frame, columns=appointment_columns, show="headings")
        tree.pack(fill="both", expand=True)

        # Define column headings
        for col in appointment_columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120, anchor="center")

            # Insert rows into Treeview
        for row in appts:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")

    # Notebook (Tabbed View) - Initially Empty
    notebook = ttk.Notebook(view_win)
    notebook.pack(fill="both", expand=True)


def view_prescriptions_patient(self, username):
    view_win = Toplevel(self.root)
    view_win.title("View Prescription Records")
    view_win.geometry("1000x600")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="replaceme",
            password="password",  # Update as needed
            database="hospital_db"
        )
        cursor = conn.cursor(buffered=False)
        cursor.callproc('view_prescriptions', (username,))
        for result in cursor.stored_results():
            prescriptions = result.fetchall()
        conn.close()
        notebook = ttk.Notebook(view_win)
        notebook.pack(fill="both", expand=True)
        # Tabs Placeholder
        tabs = {"Prescriptions": None}
        prescription_columns = ['Date', 'Duration', 'Doses', 'Drug Name', 'Doctor']

        for tab_name, tab_frame in tabs.items():
            if tab_frame:
                notebook.forget(tab_frame)
        for tab_name in tabs.keys():
            tabs[tab_name] = ttk.Frame(notebook)
            notebook.add(tabs[tab_name], text=tab_name)
        # Frame for Treeview
        tree_frame = Frame(tabs["Prescriptions"], padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True)

        # Treeview for displaying data
        tree = ttk.Treeview(tree_frame, columns=prescription_columns, show="headings")
        tree.pack(fill="both", expand=True)

        # Define column headings
        for col in prescription_columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120, anchor="center")

            # Insert rows into Treeview
        for row in prescriptions:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")

    # Notebook (Tabbed View) - Initially Empty
    notebook = ttk.Notebook(view_win)
    notebook.pack(fill="both", expand=True)


def view_procedures_patient(self, username):
    view_win = Toplevel(self.root)
    view_win.title("View Procedure Records")
    view_win.geometry("1000x600")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="replaceme",
            password="password",  # Update as needed
            database="hospital_db"
        )
        cursor = conn.cursor(buffered=False)
        cursor.callproc('view_procs', (username,))
        for result in cursor.stored_results():
            procs = result.fetchall()
        conn.close()
        notebook = ttk.Notebook(view_win)
        notebook.pack(fill="both", expand=True)
        # Tabs Placeholder
        tabs = {"Procedures": None}
        proc_columns = ['Operation', 'Date', 'Doctor']

        for tab_name, tab_frame in tabs.items():
            if tab_frame:
                notebook.forget(tab_frame)
        for tab_name in tabs.keys():
            tabs[tab_name] = ttk.Frame(notebook)
            notebook.add(tabs[tab_name], text=tab_name)
        # Frame for Treeview
        tree_frame = Frame(tabs["Procedures"], padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True)

        # Treeview for displaying data
        tree = ttk.Treeview(tree_frame, columns=proc_columns, show="headings")
        tree.pack(fill="both", expand=True)

        # Define column headings
        for col in proc_columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120, anchor="center")

            # Insert rows into Treeview
        for row in procs:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")

    # Notebook (Tabbed View) - Initially Empty
    notebook = ttk.Notebook(view_win)
    notebook.pack(fill="both", expand=True)

def display_patient_data(self, username, data_type):
    try:
        conn = gen_sql_connection.my_sql_connector()
        cursor = conn.cursor()

        # Query based on the data type
        if data_type == "appointments":
            query = "SELECT appointment_date, doctor_name, notes FROM appointments WHERE patient_username=%s"
        elif data_type == "prescriptions":
            query = "SELECT medication_name, dosage, instructions FROM prescriptions WHERE patient_username=%s"
        elif data_type == "operations":
            query = "SELECT operation_date, operation_type, surgeon FROM operations WHERE patient_username=%s"
        else:
            messagebox.showerror("Error", "Invalid data type selected!")
            return

        cursor.execute(query, (username,))
        rows = cursor.fetchall()
        conn.close()

        # Clear existing data in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Add new data to the Treeview
        if rows:
            for i, col in enumerate(cursor.column_names, start=1):
                self.tree.heading(f"col{i}", text=col)
            for row in rows:
                self.tree.insert("", END, values=row)
        else:
            messagebox.showinfo("Info", "No records found.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")