from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt


class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Eastern Health Records")
        self.root.geometry("1540x800+0+0")
        self.root.resizable(False, False)

        # Load and set the background image
        try:
            self.set_background_image()
        except Exception as e:
            print(f"Error loading background image: {e}")
            messagebox.showerror("Error", "Background image not found. Please check the image path.")
            return

        # Call the role selection window
        self.role_selection_window()

    def set_background_image(self):
        # Load the image
        bg_image = Image.open("background.jpeg")  # Replace with your image path
        bg_image = bg_image.resize((1540, 800))  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Add the image to a label
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def role_selection_window(self):
        # Frame for role selection
        self.role_frame = Frame(self.root, bg="white", bd=10, relief=RIDGE)
        self.role_frame.place(x=400, y=150, width=700, height=400)

        # Title
        title = Label(self.role_frame, text="Welcome to Eastern Health Records", font=("Arial", 20, "bold"), bg="white", fg="black")
        title.pack(side=TOP, pady=20)

        # Sub-title
        subtitle = Label(self.role_frame, text="Who are you?", font=("Arial", 16), bg="white", fg="black")
        subtitle.pack(side=TOP, pady=10)

        # Label and dropdown for role selection
        lbl_role = Label(self.role_frame, text="Role:", font=("Arial", 14), bg="white", fg="black")
        lbl_role.pack(pady=10)

        self.role_var = StringVar()
        self.role_combobox = ttk.Combobox(self.role_frame, textvariable=self.role_var, state="readonly", font=("Arial", 14))
        self.role_combobox['values'] = ("Select Role", "Patient", "Nurse", "Doctor")
        self.role_combobox.current(0)  # Set default value
        self.role_combobox.pack(pady=10)

        # Button to proceed
        btn_proceed = Button(self.role_frame, text="Proceed", font=("Arial", 14, "bold"), bg="blue", fg="white",
                             command=self.proceed_based_on_role)
        btn_proceed.pack(pady=20)

    def proceed_based_on_role(self):
        selected_role = self.role_var.get()

        if selected_role == "Select Role":
            messagebox.showerror("Error", "Please select a valid role.")
        elif selected_role in ("Patient", "Nurse", "Doctor"):
            self.role_frame.destroy()  # Remove role selection window
            self.login_window(selected_role)  # Call login window with the selected role

    def login_window(self, role):
        # Frame for login window
        self.login_frame = Frame(self.root, bg="white", bd=10, relief=RIDGE)
        self.login_frame.place(x=400, y=200, width=600, height=400)

        title = Label(self.login_frame, text=f"{role} Login", font=("Arial", 20, "bold"), bg="white", fg="black")
        title.pack(side=TOP, pady=20)

        lbl_username = Label(self.login_frame, text="Username:", font=("Arial", 14), bg="white", fg="black")
        lbl_username.place(x=50, y=100)
        self.entry_username = Entry(self.login_frame, font=("Arial", 14), bg="lightgray")
        self.entry_username.place(x=200, y=100, width=300)

        lbl_password = Label(self.login_frame, text="Password:", font=("Arial", 14), bg="white", fg="black")
        lbl_password.place(x=50, y=160)
        self.entry_password = Entry(self.login_frame, font=("Arial", 14), bg="lightgray", show="*")
        self.entry_password.place(x=200, y=160, width=300)

        btn_login = Button(self.login_frame, text="Login", font=("Arial", 14, "bold"), bg="blue", fg="white",
                           command=lambda: self.check_credentials(role))
        btn_login.place(x=200, y=250, width=100)

        btn_exit = Button(self.login_frame, text="Exit", font=("Arial", 14, "bold"), bg="red", fg="white",
                          command=self.root.destroy)
        btn_exit.place(x=350, y=250, width=100)

    def check_credentials(self, role):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Memorial092000*",  # Update as needed
                database="hospital_db"
            )
            cursor = conn.cursor()

            # Validate username, password, and role from the admin table
            query = "SELECT password FROM admin WHERE username=%s AND role=%s"
            cursor.execute(query, (username, role))
            result = cursor.fetchone()
            conn.close()

            if result:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    messagebox.showinfo("Login Success", f"Welcome, {role}!")

                    # Destroy the login frame
                    self.login_frame.destroy()

                    # Redirect to the appropriate dashboard based on the role
                    if role == "Patient":
                        self.patient_dashboard(username)
                    elif role == "Nurse":
                        self.nurse_dashboard(username)
                    elif role == "Doctor":
                        self.doctor_dashboard(username)
                else:
                    messagebox.showerror("Invalid Login", "Invalid Username or Password.")
            else:
                messagebox.showerror("Invalid Login", "Invalid Username or Password.")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Database Error", f"Error: {err}")


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
                user="root",
                password="Memorial092000*",  # Update as needed
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
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Memorial092000*",  # Update as needed
                database="hospital_db"
            )
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

    def nurse_dashboard(self, username):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        lbl_title = Label(self.root, text="Nurse Dashboard", font=("Arial", 24, "bold"), bg="dark green", fg="white")
        lbl_title.pack(side=TOP, fill=X)

        # Frame for nurse details
        details_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
        details_frame.place(x=50, y=100, width=1400, height=300)

        lbl_details = Label(details_frame, text="Personal Information", font=("Arial", 18, "bold"), bg="white", fg="black")
        lbl_details.pack(side=TOP, pady=10)

        # Query nurse details
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Memorial092000*",  # Update as needed
                database="hospital_db"
            )
            cursor = conn.cursor()

            # Corrected Query to fetch nurse information
            query = """
                SELECT n.fname, n.lname, n.phone, n.email
                FROM nurse n
                INNER JOIN admin a ON a.nurse_id = n.nurse_id
                WHERE a.username = %s
            """
            cursor.execute(query, (username,))
            nurse_info = cursor.fetchone()
            conn.close()

            if nurse_info:
                # Display nurse details
                details_text = f"""
                Name: {nurse_info[0]} {nurse_info[1]}
                Phone: {nurse_info[2]}
                Email: {nurse_info[3]}
                """
                lbl_nurse_info = Label(details_frame, text=details_text, font=("Arial", 14), bg="white", fg="black", justify=LEFT)
                lbl_nurse_info.pack(pady=10, anchor="w")
            else:
                lbl_error = Label(details_frame, text="No nurse details found.", font=("Arial", 14), bg="white", fg="red")
                lbl_error.pack(pady=10)

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Database Error", f"Error: {err}")

        # Buttons for CRUD operations
        btn_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
        btn_frame.place(x=250, y=450, width=1000, height=100)  # Slightly shifted to center

        # Center and enlarge buttons
        Button(btn_frame, text="New Record", font=("Arial", 16, "bold"), bg="blue", fg="white", width=15, command=self.create_appointment_nurse).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="View Records", font=("Arial", 16, "bold"), bg="green", fg="white", width=15, command=self.view_appointments_nurse).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="Update Record", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15, command=self.update_appointment_nurse).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="Delete Records", font=("Arial", 16, "bold"), bg="red", fg="white", width=15, command=self.delete_appointment_nurse).pack(side=LEFT, padx=20, pady=10)


    def doctor_dashboard(self, username):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        lbl_title = Label(self.root, text="Doctor Dashboard", font=("Arial", 24, "bold"), bg="red", fg="white")
        lbl_title.pack(side=TOP, fill=X)

        # Frame for doctor details
        details_frame = Frame(self.root, bg="white", bd=5, relief=RIDGE)
        details_frame.place(x=50, y=100, width=1400, height=300)

        lbl_details = Label(details_frame, text="Doctor Information", font=("Arial", 18, "bold"), bg="white", fg="black")
        lbl_details.pack(side=TOP, pady=10)

        # Query doctor details
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Memorial092000*",  # Update as needed
                database="hospital_db"
            )
            cursor = conn.cursor()

            # Corrected Query to fetch doctor information
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
                # Display doctor details
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
        btn_frame.place(x=250, y=450, width=1000, height=100)  # Slightly shifted to center

        # Center and enlarge buttons
        Button(btn_frame, text="New Record", font=("Arial", 16, "bold"), bg="blue", fg="white", width=15, command=self.doctor_create_dashboard).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="View Records", font=("Arial", 16, "bold"), bg="green", fg="white", width=15, command=self.view_appointments_doctor).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="Update Records", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15, command=self.update_appointment_nurse).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="Delete Records", font=("Arial", 16, "bold"), bg="red", fg="white", width=15, command=self.delete_appointment_nurse).pack(side=LEFT, padx=20, pady=10)

    def doctor_create_dashboard(self):
        # Popup window for creating a dashboard
        create_win = Toplevel(self.root)
        create_win.title("Create Appointment")
        create_win.geometry("800x600")
        
        # Buttons for CRUD operations
        btn_frame = Frame(create_win, bg="white", bd=5, relief=RIDGE)
        btn_frame.place(x=150, y=250, width=500, height=100)  # Slightly shifted to center

        def create_prescription():
            # Clear the root window
            for widget in create_win.winfo_children():
                widget.destroy()

            # Frame for input fields
            frame = Frame(create_win, padx=20, pady=20)
            frame.pack(fill="both", expand=True)

            # Drug ID
            Label(frame, text="Drug ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            drug_id_entry = Entry(frame, font=("Arial", 12), width=40)
            drug_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Doctor ID
            Label(frame, text="Doctor ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
            doctor_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Patient ID
            Label(frame, text="Patient ID:", font=("Arial", 12), anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
            patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
            patient_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

            # Dosage
            Label(frame, text="Dosage:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            dosage_entry = Entry(frame, font=("Arial", 12), width=40)
            dosage_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Date
            Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            date_entry = Entry(frame, font=("Arial", 12), width=40)
            date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            # Duration (Larger Text Area)
            Label(frame, text="Duration:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
            duration_entry = Text(frame, font=("Arial", 12), width=40, height=5, wrap="word")
            duration_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            # Save Appointment Button
            def save_prescription():
                # Fetch user input
                drug_id = drug_id_entry.get().strip()
                doctor_id = doctor_id_entry.get().strip()
                patient_id = patient_id_entry.get().strip()
                dosage = dosage_entry.get().strip()
                date = date_entry.get().strip()
                duration = duration_entry.get().strip()

                # Save to database
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Memorial092000*",  # Update as needed
                        database="hospital_db"
                    )
                    cursor = conn.cursor()

                    # Insert query
                    query = """
                        INSERT INTO appointment (appointment_id, date, time, reason, doctor_id, patient_id, priority, nurse_id)
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

                # Add Save Button
                Button(frame, text="Save Prescription", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_prescription).grid(
                    row=8, column=1, padx=(50, 10), pady=20, sticky="e"
                )

        def create_procedure():
            # Clear the root window
            for widget in create_win.winfo_children():
                widget.destroy()

            # Frame for input fields
            frame = Frame(create_win, padx=20, pady=20)
            frame.pack(fill="both", expand=True)

            # Procedure ID
            Label(frame, text="Procedure ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            procedure_id_entry = Entry(frame, font=("Arial", 12), width=40)
            procedure_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Appointment ID
            Label(frame, text="Appointment ID:", font=("Arial", 12), anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
            appointment_id_entry = Entry(frame, font=("Arial", 12), width=40)
            appointment_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

            # Doctor ID
            Label(frame, text="Doctor ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
            doctor_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Patient ID
            Label(frame, text="Patient ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
            patient_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Date
            Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            date_entry = Entry(frame, font=("Arial", 12), width=40)
            date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            # Notes (Larger Text Area)
            Label(frame, text="Notes:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
            notes_entry = Text(frame, font=("Arial", 12), width=40, height=5, wrap="word")
            notes_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            # Save Appointment Button
            def save_procedure():
                # Fetch user input
                procedure_id = procedure_id_entry.get().strip()
                appointment_id = appointment_id_entry.get().strip()
                doctor_id = doctor_id_entry.get().strip()
                patient_id = patient_id_entry.get().strip()
                date = date_entry.get().strip()
                notes = notes_entry.get("1.0", "end").strip()

                # Save to database
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Memorial092000*",  # Update as needed
                        database="hospital_db"
                    )
                    cursor = conn.cursor()

                    # Insert query
                    query = """
                        INSERT INTO appointment (appointment_id, date, time, reason, doctor_id, patient_id, priority, nurse_id)
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

            # Add Save Button
            Button(frame, text="Save Procedure", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_procedure).grid(
                row=8, column=1, padx=(50, 10), pady=20, sticky="e"
            )

        # Center and enlarge buttons        
        Button(btn_frame, text="New Prescription", font=("Arial", 16, "bold"), bg="orange", fg="white", width=15, command=create_prescription).pack(side=LEFT, padx=20, pady=10)
        Button(btn_frame, text="New Procedures", font=("Arial", 16, "bold"), bg="red", fg="white", width=15, command=create_procedure).pack(side=LEFT, padx=20, pady=10)

    def view_appointments_doctor(self):
        # Popup window for viewing details
        view_win = Toplevel(self.root)
        view_win.title("View Records")
        view_win.geometry("1000x600")

        # Frame for Patient ID Input
        input_frame = Frame(view_win, padx=10, pady=10)
        input_frame.pack(fill="x", side="top")

        Label(input_frame, text="Enter Patient ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(input_frame, font=("Arial", 12), width=20)
        patient_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Notebook (Tabbed View) - Initially Empty
        notebook = ttk.Notebook(view_win)
        notebook.pack(fill="both", expand=True)

        # Tabs Placeholder
        tabs = {
            "Patient Information": None,
            "Prescriptions": None,
            "Appointments": None,
            "Procedures": None
        }

        # Function to fetch and display patient details
        def fetch_patient_details():
            patient_id = patient_id_entry.get().strip()
            if not patient_id:
                messagebox.showerror("Error", "Please enter a valid Patient Name.")
                return

            # Remove existing tabs (if any)
            for tab_name, tab_frame in tabs.items():
                if tab_frame:
                    notebook.forget(tab_frame)

            # Create tabs for Patient Data, Prescription Record, Appointment Details, and Procedures
            for tab_name in tabs.keys():
                tabs[tab_name] = ttk.Frame(notebook)
                notebook.add(tabs[tab_name], text=tab_name)

            # Helper function to populate a tab with a Treeview
            def populate_tab(tab_frame, columns, query, params=()):
                # Frame for Treeview
                tree_frame = Frame(tab_frame, padx=10, pady=10)
                tree_frame.pack(fill="both", expand=True)

                # Treeview for displaying data
                tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
                tree.pack(fill="both", expand=True)

                # Define column headings
                for col in columns:
                    tree.heading(col, text=col.capitalize())
                    tree.column(col, width=120, anchor="center")

                # Fetch data from database
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Memorial092000*",  # Update as needed
                        database="hospital_db"
                    )
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    conn.close()

                    # Insert rows into Treeview
                    for row in rows:
                        tree.insert("", "end", values=row)
                except mysql.connector.Error as err:
                    print(f"Database Error: {err}")
                    messagebox.showerror("Database Error", f"Error: {err}")

            # Populate Patient Tab
            patient_columns = ["patient_id", "fname", "lname", "dob", "phone", "email", "postal_code"]
            patient_query = """
                SELECT patient_id, fname, lname, dob, phone, email, postal_code
                FROM patient
                WHERE patient_id = %s
            """
            populate_tab(tabs["Patient Information"], patient_columns, patient_query, params=(patient_id,))

            # Populate Prescriptions Tab
            prescription_columns = ["prescription_id", "drug_name", "dosage", "prescription duration", "date"]
            prescription_query = """
                SELECT pr.drug_id, dr.name, pr.doses, pr.duration, pr.start_date
                FROM prescription pr, drugs dr
                WHERE dr.drug_id=pr.drug_id AND patient_id = %s
            """
            populate_tab(tabs["Prescriptions"], prescription_columns, prescription_query, params=(patient_id,))

            # Populate Appointments Tab
            appointment_columns = ["appointment_id", "date", "time", "reason", "doctor_id", "priority", "nurse_id"]
            appointment_query = """
                SELECT appointment_id, date, time, reason, doctor_id, priority, nurse_id
                FROM appointment
                WHERE patient_id = %s
            """
            populate_tab(tabs["Appointments"], appointment_columns, appointment_query, params=(patient_id,))

            # Populate Procedures Tab
            procedure_columns = ["procedure_id", "procedure_name", "date", "doctor_id", "notes"]
            procedure_query = """
                SELECT pr.procedure_id, op.name, pr.date, pr.doctor_id, pr.notes
                FROM procedure pr
                INNER JOIN operations op
                ON pr.procedure_id=op.procedure_id
                WHERE patient_id = %s
            """
            populate_tab(tabs["Procedures"], procedure_columns, procedure_query, params=(patient_id,))

        # Fetch Button
        Button(input_frame, text="Fetch Details", font=("Arial", 12, "bold"), bg="blue", fg="white", command=fetch_patient_details).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

    def create_appointment_nurse(self):
        # Popup window for creating an appointment
        create_win = Toplevel(self.root)
        create_win.title("Create Appointment")
        create_win.geometry("800x600")  # Increased size to accommodate content

        # Frame for input fields
        frame = Frame(create_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Appointment ID
        Label(frame, text="Appointment ID (Leave blank for auto-increment):", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        appointment_id_entry = Entry(frame, font=("Arial", 12), width=40)
        appointment_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Date
        Label(frame, text="Date (YYYY-MM-DD):", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        date_entry = Entry(frame, font=("Arial", 12), width=40)
        date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Time (Dropdown for 12-hour format)
        Label(frame, text="Time:", font=("Arial", 12), anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        time_var = StringVar(value="Select Time")
        time_options = [
            "12:00 AM", "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
            "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM"
        ]
        time_menu = OptionMenu(frame, time_var, *time_options)
        time_menu.config(font=("Arial", 12), width=35, highlightthickness=1)
        time_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Reason (Larger Text Area)
        Label(frame, text="Reason:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        reason_entry = Text(frame, font=("Arial", 12), width=40, height=5, wrap="word")
        reason_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Doctor ID
        Label(frame, text="Doctor ID:", font=("Arial", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        doctor_id_entry = Entry(frame, font=("Arial", 12), width=40)
        doctor_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Patient ID
        Label(frame, text="Patient ID:", font=("Arial", 12), anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(frame, font=("Arial", 12), width=40)
        patient_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Priority
        Label(frame, text="Priority (Low, Medium, High):", font=("Arial", 12), anchor="w").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        priority_entry = Entry(frame, font=("Arial", 12), width=40)
        priority_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Nurse ID (Manual Input)
        Label(frame, text="Nurse ID:", font=("Arial", 12), anchor="w").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        nurse_id_entry = Entry(frame, font=("Arial", 12), width=40)
        nurse_id_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Save Appointment Button
        def save_appointment():
            # Fetch user input
            appointment_id = appointment_id_entry.get().strip()
            date = date_entry.get().strip()
            time = time_var.get().strip()
            reason = reason_entry.get("1.0", "end").strip()
            doctor_id = doctor_id_entry.get().strip()
            patient_id = patient_id_entry.get().strip()
            priority = priority_entry.get().strip()
            nurse_id = nurse_id_entry.get().strip()

            # Validation for time selection
            if time == "Select Time":
                messagebox.showerror("Error", "Please select a valid time.")
                return

            # Save to database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Memorial092000*",  # Update as needed
                    database="hospital_db"
                )
                cursor = conn.cursor()

                # Insert query
                query = """
                    INSERT INTO appointment (appointment_id, date, time, reason, doctor_id, patient_id, priority, nurse_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (appointment_id or None, date, time, reason, doctor_id, patient_id, priority, nurse_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Appointment created successfully!")
                create_win.destroy()

            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        # Add Save Button
        Button(frame, text="Save Appointment", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_appointment).grid(
            row=8, column=1, padx=(50, 10), pady=20, sticky="e"
        )
    
    def view_appointments_nurse(self):
        # Popup window for viewing details
        view_win = Toplevel(self.root)
        view_win.title("View Records")
        view_win.geometry("1000x600")

        # Frame for Patient ID Input
        input_frame = Frame(view_win, padx=10, pady=10)
        input_frame.pack(fill="x", side="top")

        Label(input_frame, text="Enter Patient ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        patient_id_entry = Entry(input_frame, font=("Arial", 12), width=20)
        patient_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Notebook (Tabbed View) - Initially Empty
        notebook = ttk.Notebook(view_win)
        notebook.pack(fill="both", expand=True)

        # Tabs Placeholder
        tabs = {
            "Prescriptions": None,
            "Appointments": None,
            "Procedures": None
        }

        # Function to fetch and display patient details
        def fetch_patient_details():
            patient_id = patient_id_entry.get().strip()
            if not patient_id:
                messagebox.showerror("Error", "Please enter a valid Patient ID.")
                return

            # Remove existing tabs (if any)
            for tab_name, tab_frame in tabs.items():
                if tab_frame:
                    notebook.forget(tab_frame)

            # Create tabs for Prescription Record, Appointment Details, and Procedures
            for tab_name in tabs.keys():
                tabs[tab_name] = ttk.Frame(notebook)
                notebook.add(tabs[tab_name], text=tab_name)

            # Helper function to populate a tab with a Treeview
            def populate_tab(tab_frame, columns, query, params=()):
                # Frame for Treeview
                tree_frame = Frame(tab_frame, padx=10, pady=10)
                tree_frame.pack(fill="both", expand=True)

                # Treeview for displaying data
                tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
                tree.pack(fill="both", expand=True)

                # Define column headings
                for col in columns:
                    tree.heading(col, text=col.capitalize())
                    tree.column(col, width=120, anchor="center")

                # Fetch data from database
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Memorial092000*",  # Update as needed
                        database="hospital_db"
                    )
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    conn.close()

                    # Insert rows into Treeview
                    for row in rows:
                        tree.insert("", "end", values=row)
                except mysql.connector.Error as err:
                    print(f"Database Error: {err}")
                    messagebox.showerror("Database Error", f"Error: {err}")

            # Populate Prescriptions Tab
            prescription_columns = ["prescription_id", "drug_name", "dosage", "prescription duration", "date"]
            prescription_query = """
                SELECT pr.drug_id, dr.name, pr.doses, pr.duration, pr.start_date
                FROM prescription pr, drugs dr
                WHERE dr.drug_id=pr.drug_id AND patient_id = %s
            """
            populate_tab(tabs["Prescriptions"], prescription_columns, prescription_query, params=(patient_id,))

            # Populate Appointments Tab
            appointment_columns = ["appointment_id", "date", "time", "reason", "doctor_id", "priority", "nurse_id"]
            appointment_query = """
                SELECT appointment_id, date, time, reason, doctor_id, priority, nurse_id
                FROM appointment
                WHERE patient_id = %s
            """
            populate_tab(tabs["Appointments"], appointment_columns, appointment_query, params=(patient_id,))

            # Populate Procedures Tab
            procedure_columns = ["procedure_id", "procedure_name", "date", "doctor_id", "notes"]
            procedure_query = """
                SELECT proc.procedure_id, op.name, proc.date, proc.doctor_id, proc.notes
                FROM procedure proc
                INNER JOIN operations op ON op.procedure_id=proc.procedure_id
                WHERE patient_id = %s
            """
            populate_tab(tabs["Procedures"], procedure_columns, procedure_query, params=(patient_id,))

        # Fetch Button
        Button(input_frame, text="Fetch Details", font=("Arial", 12, "bold"), bg="blue", fg="white", command=fetch_patient_details).grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

    def update_appointment_nurse(self):
        # Popup window for updating an appointment
        update_win = Toplevel(self.root)
        update_win.title("Update Appointment")
        update_win.geometry("800x600")

        # Frame for input fields
        frame = Frame(update_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Appointment ID to fetch
        Label(frame, text="Enter Appointment ID to Update:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        appointment_id_entry = Entry(frame, font=("Arial", 12), width=40)
        appointment_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Fields for updating
        fields = [
            "Date (YYYY-MM-DD):",
            "Time (e.g., 2:00 PM):",
            "Reason:",
            "Doctor ID:",
            "Patient ID:",
            "Priority (Low/Medium/High):",
            "Nurse ID:"
        ]
        entries = {}

        for i, field in enumerate(fields, start=1):
            Label(frame, text=field, font=("Arial", 12), anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if "Reason" in field:  # Larger text box for Reason
                entry = Text(frame, font=("Arial", 12), width=40, height=4, wrap="word")
            else:
                entry = Entry(frame, font=("Arial", 12), width=40)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[field] = entry

        # Function to fetch current details of the appointment
        def fetch_appointment():
            appointment_id = appointment_id_entry.get().strip()
            if not appointment_id:
                messagebox.showerror("Error", "Appointment ID is required to fetch details.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Memorial092000*",  # Update as needed
                    database="hospital_db"
                )
                cursor = conn.cursor()
                query = """
                    SELECT date, time, reason, doctor_id, patient_id, priority, nurse_id
                    FROM appointment
                    WHERE appointment_id = %s
                """
                cursor.execute(query, (appointment_id,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    # Populate fields with current data
                    fields_data = ["Date (YYYY-MM-DD):", "Time (e.g., 2:00 PM):", "Reason:", "Doctor ID:", "Patient ID:", "Priority (Low/Medium/High):", "Nurse ID:"]
                    for field, value in zip(fields_data, result):
                        if "Reason" in field:
                            entries[field].delete("1.0", "end")
                            entries[field].insert("1.0", value)
                        else:
                            entries[field].delete(0, "end")
                            entries[field].insert(0, value)
                else:
                    messagebox.showerror("Error", "No appointment found with the provided Appointment ID.")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        # Function to save updated details
        def save_updates():
            appointment_id = appointment_id_entry.get().strip()
            if not appointment_id:
                messagebox.showerror("Error", "Appointment ID is required to save updates.")
                return

            new_values = []
            for field in fields:
                if "Reason" in field:
                    new_values.append(entries[field].get("1.0", "end").strip())  # Multi-line text box
                else:
                    new_values.append(entries[field].get().strip())

            if not all(new_values):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Memorial092000*",  # Update as needed
                    database="hospital_db"
                )
                cursor = conn.cursor()
                query = """
                    UPDATE appointment
                    SET date = %s, time = %s, reason = %s, doctor_id = %s, patient_id = %s, priority = %s, nurse_id = %s
                    WHERE appointment_id = %s
                """
                cursor.execute(query, (*new_values, appointment_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Appointment updated successfully!")
                update_win.destroy()
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        # Fetch Button
        Button(frame, text="Fetch Details", font=("Arial", 12, "bold"), bg="blue", fg="white", command=fetch_appointment).grid(
            row=len(fields) + 1, column=0, padx=10, pady=20, sticky="w"
        )

        # Save Button
        Button(frame, text="Save Updates", font=("Arial", 12, "bold"), bg="green", fg="white", command=save_updates).grid(
            row=len(fields) + 1, column=1, padx=10, pady=20, sticky="e"
        )
    
    def delete_appointment_nurse(self):
        # Popup window for deleting an appointment
        delete_win = Toplevel(self.root)
        delete_win.title("Delete Appointment")
        delete_win.geometry("500x250")  # Increased size for better layout
        delete_win.resizable(False, False)  # Disable resizing of the window

        # Frame for input fields
        frame = Frame(delete_win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Appointment ID Input
        Label(frame, text="Enter Appointment ID:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        appointment_id_entry = Entry(frame, font=("Arial", 12), width=30)
        appointment_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Delete Button below the text field
        Button(frame, text="Delete Appointment", font=("Arial", 12, "bold"), bg="red", fg="white", command=lambda: confirm_delete(appointment_id_entry.get())).grid(
            row=1, column=0, columnspan=2, pady=20, sticky="n"
        )

        # Function to handle delete operation
        def confirm_delete(appointment_id):
            appointment_id = appointment_id.strip()
            if not appointment_id:
                messagebox.showerror("Error", "Appointment ID is required to delete an appointment.")
                return

            # Confirmation dialog
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete appointment ID {appointment_id}?")
            if not confirm:
                return

            try:
                # Connect to database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Memorial092000*",  # Update as needed
                    database="hospital_db"
                )
                cursor = conn.cursor()

                # Delete query
                query = "DELETE FROM appointment WHERE appointment_id = %s"
                cursor.execute(query, (appointment_id,))
                conn.commit()
                conn.close()

                # Success message
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Appointment ID {appointment_id} deleted successfully!")
                    delete_win.destroy()
                else:
                    messagebox.showerror("Error", f"No appointment found with ID {appointment_id}.")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
                messagebox.showerror("Database Error", f"Error: {err}")

        





if __name__ == "__main__":
    root = Tk()
    ob = Hospital(root)
    root.mainloop()
