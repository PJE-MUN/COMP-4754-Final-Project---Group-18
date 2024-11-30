from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt
import gen_sql_connection
import doctor_profile
import nurse_profile
import patient_profile


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
            conn = gen_sql_connection.my_sql_connector()
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
                        patient_profile.patient_dashboard(self, username)
                    elif role == "Nurse":
                        nurse_profile.nurse_dashboard(self, username)
                    elif role == "Doctor":
                        doctor_profile.doctor_dashboard(self, username)
                else:
                    messagebox.showerror("Invalid Login", "Invalid Username or Password.")
            else:
                messagebox.showerror("Invalid Login", "Invalid Username or Password.")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Database Error", f"Error: {err}")



if __name__ == "__main__":
    root = Tk()
    ob = Hospital(root)
    root.mainloop()
