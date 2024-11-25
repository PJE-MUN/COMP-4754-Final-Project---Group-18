import mysql.connector
import bcrypt

def store_user():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Realmadrid1$",  # Replace with your MySQL password
            database="hospital_db"
        )
        cursor = conn.cursor()

        # User input
        username = input("Enter username: ").strip()
        plain_password = input("Enter password: ").strip()
        role = input("Enter role (Patient, Nurse, Doctor): ").capitalize()

        if role not in ['Patient', 'Nurse', 'Doctor']:
            print("Invalid role! Please enter either 'Patient', 'Nurse', or 'Doctor'.")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        patient_id = None
        if role == 'Patient':
            patient_id = input("Enter patient_id: ").strip()
            if not patient_id.isdigit():
                print("Invalid patient_id. It must be a number.")
                return
            patient_id = int(patient_id)

            # Check if patient_id exists in the patient table
            cursor.execute("SELECT patient_id FROM patient WHERE patient_id = %s", (patient_id,))
            if not cursor.fetchone():
                print(f"Error: patient_id {patient_id} does not exist in the patient table.")
                return

        # Insert into admin table
        if role == 'Patient':
            query = "INSERT INTO admin (username, password, role, patient_id) VALUES (%s, %s, %s, %s)"
            values = (username, hashed_password, role, patient_id)
        else:
            query = "INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)"
            values = (username, hashed_password, role)

        cursor.execute(query, values)
        conn.commit()
        print(f"User '{username}' with role '{role}' stored successfully.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    store_user()
