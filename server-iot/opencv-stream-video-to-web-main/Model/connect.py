import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="tr1nhtu@n",
            database="iot"
        )
        if connection.is_connected():
            print("Kết nối thành công!")
            return connection
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối: {err}")
        return None
