import mysql



def my_sql_connector():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="replaceme",  # Update as needed
        database="hospital_db"
    )


