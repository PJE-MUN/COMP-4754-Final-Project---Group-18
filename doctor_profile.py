from tkinter import *
from tkinter import ttk, messagebox
import mysql
import gen_sql_connection


def doctor_dashboard(self, username):
    for widget in self.root.winfo_children():
        widget.destroy()

    lbl_title = Label(self.root, text="Doctor Dashboard", font=("Arial", 24, "bold"), bg="red", fg="white")
    lbl_title.pack(side=TOP, fill=X)

    details_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
    details_frame.place(x=50, y=100, width=1400, height=300)

    lbl_details = Label(details_frame, text="Doctor Information", font=("Arial", 18, "bold"), bg="white", fg="black")
    lbl_details.pack(side=TOP, pady=10)

    try:
        conn = gen_sql_connection.my_sql_connector()
        cursor = conn.cursor()

        query = """
        SELECT d.fname, d.lname, d.specialty, d.email, d.phone
        FROM doctor d
        INNER JOIN admin a ON a.doctor_id = d.doctor_id
        WHERE a.username = %s
        """
        cursor.execute(query, (username,))
        doctor_info = cursor.fetchone()
        conn.close()

        if doctor_info:
            details_text = f"""
            Name: {doctor_info[0]} {doctor_info[1]}
            Specialty: {doctor_info[2]}
            Email: {doctor_info[3]}
            Phone: {doctor_info[4]}
            """
            lbl_doctor_info = Label(details_frame, text=details_text, font=("Arial", 14), bg="white", fg="black", justify=LEFT)
            lbl_doctor_info.pack(pady=10, anchor="w")
        else:
            lbl_error = Label(details_frame, text="No doctor details found.", font=("Arial", 14), bg="white", fg="red")
            lbl_error.pack(pady=10)

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")

    # Buttons for CRUD operations
    btn_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
    btn_frame.place(x=250, y=450, width=1000, height=100)

    Button(btn_frame, text="Create Prescription & Procedure", font=("Arial", 12, "bold"), bg="blue", fg="white", wraplength=200, width=20, command=lambda: doctor_create_dashboard(self)).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="View Patient Detail", font=("Arial", 12, "bold"), bg="green", fg="white", width=20, command=lambda: view_patient_doctor(self)).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="Update Patient Detail", font=("Arial", 12, "bold"), bg="orange", fg="white", width=20, command=lambda: doctor_update_dashboard(self)).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="Delete Patient Record", font=("Arial", 12, "bold"), bg="red", fg="white", width=20, command=lambda: doctor_delete_dashboard(self)).pack(side=LEFT, padx=20, pady=10)


def doctor_create_dashboard(self):
    create_win = Toplevel(self.root)
    create_win.title("Create Prescription & Procedure")
    create_win.geometry("800x600")

    # Buttons for CRUD operations
    btn_frame = Frame(create_win, bg="white", bd=5, relief=RIDGE)
    btn_frame.place(x=150, y=250, width=500, height=100)

    def create_prescription():
        for widget in create_win.winfo_children():
            widget.destroy()

        frame = Frame(create_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Drug ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        drug_id_entry = Entry(frame, font=("Arial", 12), width=40)
        drug_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Doctor ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
        doctor_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Patient ID:", font=("Arial", 12), anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
        patient_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Dosage:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        dosage_entry = Entry(frame, font=("Arial", 12), width=40)
        dosage_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        date_entry = Entry(frame, font=("Arial", 12), width=40)
        date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Duration:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        duration_entry = Text(frame, font=("Arial", 12), width=40, height=5, wrap="word")
        duration_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        def save_prescription():
            drug_id = drug_id_entry.get().strip()
            doctor_id = doctor_id_entry.get().strip()
            patient_id = patient_id_entry.get().strip()
            dosage = dosage_entry.get().strip()
            date = date_entry.get().strip()
            duration = duration_entry.get().strip()

            try:
                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()

                query = """
                    INSERT INTO prescription (drug_id, doctor_id, patient_id, doses, start_date, duration)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (drug_id, doctor_id, patient_id, dosage, date, duration))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Prescription created successfully!")
                create_win.destroy()

            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

            Button(frame, text="Save Prescription", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_prescription).grid(
                row=8, column=1, padx=(50, 10), pady=20, sticky="e"
            )

    def create_procedure():
        for widget in create_win.winfo_children():
            widget.destroy()

        frame = Frame(create_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Procedure ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        procedure_id_entry = Entry(frame, font=("Arial", 12), width=40)
        procedure_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Appointment ID:", font=("Arial", 12), anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        appointment_id_entry = Entry(frame, font=("Arial", 12), width=40)
        appointment_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Doctor ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
        doctor_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Patient ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
        patient_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        date_entry = Entry(frame, font=("Arial", 12), width=40)
        date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        Label(frame, text="Notes:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        notes_entry = Text(frame, font=("Arial", 12), width=40, height=5, wrap="word")
        notes_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        def save_procedure():
            procedure_id = procedure_id_entry.get().strip()
            appointment_id = appointment_id_entry.get().strip()
            doctor_id = doctor_id_entry.get().strip()
            patient_id = patient_id_entry.get().strip()
            date = date_entry.get().strip()
            notes = notes_entry.get("1.0", "end").strip()

            try:
                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()

                query = """
                    INSERT INTO procedures (procedure_id, appointment_id, doctor_id, patient_id, procedure_date, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (procedure_id, appointment_id, doctor_id, patient_id, date, notes))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Procedure created successfully!")
                create_win.destroy()

            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        Button(frame, text="Save Procedure", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_procedure).grid(
            row=8, column=1, padx=(50, 10), pady=20, sticky="e"
        )
      
    Button(btn_frame, text="Create Prescription", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15, command=create_prescription).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="Create Procedure", font=("Arial", 16, "bold"), bg="red", fg="white", width=15, command=create_procedure).pack(side=LEFT, padx=20, pady=10)

def view_patient_doctor(self):
    view_win = Toplevel(self.root)
    view_win.title("View Patient Detail")
    view_win.geometry("1000x600")

    input_frame = Frame(view_win, padx=10, pady=10)
    input_frame.pack(fill="x", side="top")

    Label(input_frame, text="Enter Patient ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    patient_id_entry = Entry(input_frame, font=("Arial", 12), width=20)
    patient_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    notebook = ttk.Notebook(view_win)
    notebook.pack(fill="both", expand=True)

    tabs = {
        "Patient Information": None,
        "Prescriptions": None,
        "Appointments": None,
        "Procedures": None
    }

    def fetch_patient_details():
        patient_id = patient_id_entry.get().strip()
        if not patient_id:
            messagebox.showerror("Error", "Please enter a valid Patient Name.")
            return

        for tab_name, tab_frame in tabs.items():
            if tab_frame:
                notebook.forget(tab_frame)

        for tab_name in tabs.keys():
            tabs[tab_name] = ttk.Frame(notebook)
            notebook.add(tabs[tab_name], text=tab_name)

        def populate_tab(tab_frame, columns, query, params=()):
            tree_frame = Frame(tab_frame, padx=10, pady=10)
            tree_frame.pack(fill="both", expand=True)

            tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
            tree.pack(fill="both", expand=True)

            for col in columns:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=120, anchor="center")

            try:
                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                conn.close()

                for row in rows:
                    tree.insert("", "end", values=row)
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        patient_columns = ["patient_id", "fname", "lname", "dob", "phone", "email", "postal_code"]
        patient_query = """
            SELECT patient_id, fname, lname, dob, phone, email, postal_code
                FROM patient
                WHERE patient_id = %s
        """
        populate_tab(tabs["Patient Information"], patient_columns, patient_query, params=(patient_id,))

        prescription_columns = ["prescription_id", "drug_name", "dosage", "prescription duration", "date"]
        prescription_query = """
            SELECT pr.drug_id, dr.name, pr.doses, pr.duration, pr.start_date
                FROM prescription pr, drugs dr
                WHERE dr.drug_id=pr.drug_id AND patient_id = %s
        """
        populate_tab(tabs["Prescriptions"], prescription_columns, prescription_query, params=(patient_id,))

        appointment_columns = ["appointment_id", "date", "time", "reason", "doctor_id", "priority", "nurse_id"]
        appointment_query = """
            SELECT appointment_id, date, time, reason, doctor_id, priority, nurse_id
                FROM appointment
                WHERE patient_id = %s
        """
        populate_tab(tabs["Appointments"], appointment_columns, appointment_query, params=(patient_id,))

        procedure_columns = ["procedure_id", "procedure_name", "date", "doctor_id", "notes"]
        procedure_query = """
            SELECT pr.procedure_id, op.name, pr.procedure_date, pr.doctor_id, pr.notes
                FROM procedures pr, operations op
                WHERE pr.procedure_id=op.procedure_id AND patient_id = %s
        """
        populate_tab(tabs["Procedures"], procedure_columns, procedure_query, params=(patient_id,))

    Button(input_frame, text="Fetch Details", font=("Arial", 12, "bold"), bg="blue", fg="white", command=fetch_patient_details).grid(
        row=0, column=2, padx=10, pady=5, sticky="w"
    )


def doctor_update_dashboard(self):
    update_win = Toplevel(self.root)
    update_win.title("Update Prescription & Procedure")
    update_win.geometry("800x600")

    btn_frame = Frame(update_win, bg="white", bd=5, relief=RIDGE)
    btn_frame.place(x=150, y=250, width=550, height=100)

    def update_prescription():
        frame = Frame(update_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        labels = {
            "drug_id": Label(frame, text="Enter Drug (Prescription) ID to Update:"),
            "doctor_id": Label(frame, text="Doctor ID:"),
            "patient_id": Label(frame, text="Patient ID:"),
            "doses": Label(frame, text="Doses (Number Only):"),
            "start_date": Label(frame, text="Start Date (YYYY-MM-DD):"),
            "duration": Label(frame, text="Duration (milligrams in __ weeks):")
        }

        labels["drug_id"].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        drug_id_entry = Entry(frame, font=("Arial", 12), width=40)
        drug_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        labels["doctor_id"].grid(row=1, column=0, padx=10, pady=5, sticky="w")
        doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
        doctor_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        labels["patient_id"].grid(row=2, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
        patient_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        labels["doses"].grid(row=3, column=0, padx=10, pady=5, sticky="w")
        doses_entry = Entry(frame, font=("Arial", 12), width=40)
        doses_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        labels["start_date"].grid(row=4, column=0, padx=10, pady=5, sticky="w")
        start_date_entry = Entry(frame, font=("Arial", 12), width=40)
        start_date_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        labels["duration"].grid(row=5, column=0, padx=10, pady=5, sticky="w")
        duration_entry = Entry(frame, font=("Arial", 12), width=40)
        duration_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        def update():
            try:
                drug_id = drug_id_entry.get().strip()
                doctor_id = doctor_id_entry.get().strip()
                patient_id = patient_id_entry.get().strip()
                doses = doses_entry.get().strip()
                start_date = start_date_entry.get().strip()
                duration = duration_entry.get().strip()

                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()
                cursor.callproc("UpdatePrescription", (int(drug_id), int(doctor_id), int(patient_id), int(doses), start_date, duration))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Prescription updated successfully!")
                update_win.destroy()
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        Button(frame, text="Update", font=("Arial", 12, "bold"), bg="blue", fg="white", command=update).grid(
            row=len(labels) + 1, column=0, padx=10, pady=20, sticky="w"
        )
    
    def update_procedure():
        frame = Frame(update_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        labels = {
            "procedure_id": Label(frame, text="Enter Procedure ID to Update:"),
            "appointment_id": Label(frame, text="Appointment ID:"),
            "doctor_id": Label(frame, text="Doctor ID:"),
            "patient_id": Label(frame, text="Patient ID:"),
            "procedure_date": Label(frame, text="Date (YYYY-MM-DD):"),
            "notes": Label(frame, text="Notes:")
        }

        labels["procedure_id"].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        procedure_id_entry = Entry(frame, font=("Arial", 12), width=40)
        procedure_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        labels["appointment_id"].grid(row=1, column=0, padx=10, pady=5, sticky="w")
        appointment_id_entry = Entry(frame, font=("Arial", 12), width=40)
        appointment_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        labels["doctor_id"].grid(row=2, column=0, padx=10, pady=5, sticky="w")
        doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
        doctor_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        labels["patient_id"].grid(row=3, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
        patient_id_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        labels["procedure_date"].grid(row=4, column=0, padx=10, pady=5, sticky="w")
        date_entry = Entry(frame, font=("Arial", 12), width=40)
        date_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        labels["notes"].grid(row=5, column=0, padx=10, pady=5, sticky="w")
        notes_entry = Entry(frame, font=("Arial", 12), width=40)
        notes_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        def update():
            try:
                procedure_id = procedure_id_entry.get().strip()
                appointment_id = appointment_id_entry.get().strip()
                doctor_id = doctor_id_entry.get().strip()
                patient_id = patient_id_entry.get().strip()
                date = date_entry.get().strip()
                notes = notes_entry.get().strip()

                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()
                cursor.callproc("UpdateProcedure", (int(procedure_id), int(appointment_id), int(doctor_id), int(patient_id), date, notes))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Procedure updated successfully!")
                update_win.destroy()
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        # Update Button
        Button(frame, text="Update", font=("Arial", 12, "bold"), bg="blue", fg="white", command=update).grid(
            row=len(labels) + 1, column=0, padx=10, pady=20, sticky="w"
        )
      
    Button(btn_frame, text="Update Prescription", font=("Arial", 16, "bold"), bg="orange", fg="white", width=18, command=update_prescription).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="Update Procedure", font=("Arial", 16, "bold"), bg="red", fg="white", width=18, command=update_procedure).pack(side=LEFT, padx=20, pady=10)


def doctor_delete_dashboard(self):
    delete_win = Toplevel(self.root)
    delete_win.title("Delete Prescription & Procedure")
    delete_win.geometry("800x250")  # Increased size for better layout
    delete_win.resizable(False, False)  # Disable resizing of the window

    btn_frame = Frame(delete_win, bg="white", bd=5, relief=RIDGE)
    btn_frame.place(x=150, y=75, width=500, height=100)  # Slightly shifted to center
    
    def delete_prescription():
        frame = Frame(delete_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Enter Prescription ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        drug_id_entry = Entry(frame, font=("Arial", 12), width=30)
        drug_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Button(frame, text="Delete Prescription", font=("Arial", 12, "bold"), bg="red", fg="white", command=lambda: confirm_delete(drug_id_entry.get())).grid(
            row=1, column=0, columnspan=2, pady=20, sticky="n"
        )

        def confirm_delete(drug_id):
            drug_id = drug_id.strip()
            if not drug_id:
                messagebox.showerror("Error", "Prescription ID is required to delete a Prescription.")
                return

            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Prescription ID {drug_id}?")
            if not confirm:
                return

            try:
                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()

                cursor.execute(f"SELECT delete_prescription({drug_id})")
                result = cursor.fetchone()[0]
                conn.commit()
                conn.close()

                messagebox.showinfo("Result", f"{result}")
                
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")


    def delete_procedure():
        frame = Frame(delete_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Enter Procedure ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        procedure_id_entry = Entry(frame, font=("Arial", 12), width=30)
        procedure_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Button(frame, text="Delete Procedure", font=("Arial", 12, "bold"), bg="red", fg="white", command=lambda: confirm_delete(procedure_id_entry.get())).grid(
            row=1, column=0, columnspan=2, pady=20, sticky="n"
        )

        # Function to handle delete operation
        def confirm_delete(procedure_id):
            procedure_id = procedure_id.strip()
            if not procedure_id:
                messagebox.showerror("Error", "Procedure ID is required to delete a procedure.")
                return

            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete procedure ID {procedure_id}?")
            if not confirm:
                return

            try:
                conn = gen_sql_connection.my_sql_connector()
                cursor = conn.cursor()

                cursor.execute(f"SELECT delete_prescription({procedure_id})")
                result = cursor.fetchone()[0]
                conn.commit()
                conn.close()

                messagebox.showinfo("Result", f"{result}")
                
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")
      
    Button(btn_frame, text="Delete Prescription", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15, command=delete_prescription).pack(side=LEFT, padx=20, pady=10)
    Button(btn_frame, text="Delete Procedure", font=("Arial", 16, "bold"), bg="red", fg="white", width=15, command=delete_procedure).pack(side=LEFT, padx=20, pady=10)