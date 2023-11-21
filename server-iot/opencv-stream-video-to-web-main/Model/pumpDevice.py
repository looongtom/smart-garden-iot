import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class PumpDeviceRepository:
    def add_pumpdevice_data(self, State, time_now):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.waterpump (State, Time) VALUES (%s, %s)', (State, time_now))
                conn.commit()