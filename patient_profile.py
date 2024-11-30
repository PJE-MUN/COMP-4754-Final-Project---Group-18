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
        conn = gen_sql_connection.my_sql_connector()
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
            lbl_patient_info = Label(details_frame, text=details_text, font=("Arial", 14), bg="white", fg="black", justify=LEFT)
            lbl_patient_info.pack(pady=10, anchor="w")
        else:
            lbl_error = Label(details_frame, text="No patient details found.", font=("Arial", 14), bg="white", fg="red")
            lbl_error.pack(pady=10)

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")


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