import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class HistoryRepository:
    def add_history_data(self, Time,Temperature, Humidity ,Light, Soil, pump_state, light_state):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.history(Time,Temperature, Humidity ,Light, Soil, pump_state, light_state ) VALUES (%s, %s,%s, %s,%s, %s,%s)', (Time,Temperature, Humidity ,Light, Soil, pump_state, light_state))
                conn.commit()
    def get_history_data(self):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM history order by time desc;"
                cursor.execute(query)
                data = cursor.fetchall()
        return data
