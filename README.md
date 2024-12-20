# DatabaseProject4754

This is a Python-based GUI application that provides a medical database which will serve as an aid in the operating efficiency of the hospital. Doctors can create, read, update and delete procedures and prescriptions. Nurses can create, read, update and delete appointments. The nurses and doctors can also view patient details. The patients can read only the appointments they have been booked for.

# Installation

1.	Clone the Repository:
git clone https://github.com/PJE-MUN/COMP-4754-Final-Project---Group-18.git
cd python-gui-project

2.	Install Required Packages:
pip install mysql-connector-python
pip install bcrypt
pip install pillow

3.	Set Up the Database Connection:
Check the gen_sql_connection.py file to update your host connection to the mysql database:
db = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

4.	Run the Project:
Using the terminal: python hospital.py

5.	Log in credentials:
Patient – Username: patient1, Password: 1234
Nurse - Username: nurse1, Password: nurse1
Doctor - Username: doctor1, Password: doctor1

Dependencies
•	Python 3.7+
•	MySQL Server
•	Python Packages:
    o	tkinter (comes pre-installed with Python on most systems)
    o	PIL (Pillow, for handling image-related tasks)
    o	mysql-connector-python (for database connectivity)
    o	bcrypt (for password hashing)
