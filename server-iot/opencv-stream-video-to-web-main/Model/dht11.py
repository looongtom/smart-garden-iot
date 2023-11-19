import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class DHT11Repository:
    def add_dht11_data(self, Temperature, Humidity, time_now):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.temperaturehumidity(Temperature, Humidity, Time) VALUES (%s, %s, %s)', (Temperature, Humidity, time_now))
                conn.commit()