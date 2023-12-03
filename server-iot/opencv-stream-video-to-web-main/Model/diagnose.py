import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class DiagnoseRepository:
    def add_diagnose_data(self, Link_image, Diagnose, Time):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.diagnose(Link_image, Diagnose, Time ) VALUES (%s, %s,%s)', (Link_image, Diagnose, Time))
                conn.commit()
    def get_diagnose_data(self):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM diagnose order by time desc;"
                cursor.execute(query)
                data = cursor.fetchall()
        return data
