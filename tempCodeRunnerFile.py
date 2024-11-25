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
                    password="Realmadrid1$",  # Update as needed
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

