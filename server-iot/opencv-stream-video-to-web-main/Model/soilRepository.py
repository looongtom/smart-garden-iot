import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class SoilRepository:
    def add_soil_data(self, SoilHumidity, time_now):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.soilhumiditysensor(SoilHumidity, Time) VALUES (%s, %s)', (SoilHumidity, time_now))
                conn.commit()