import mysql.connector
from Model.connect import create_connection
from datetime import datetime

class LightRepository:
    def add_light_data(self, intensity, time_now):
        conn = create_connection()
        if conn:
            with conn:
                cursor = conn.cursor()
                # Thêm dữ liệu vào bảng light
                result=cursor.execute('INSERT INTO iot.lightsensor(Light_Intensity, Time) VALUES (%s, %s)', (intensity, time_now))
                conn.commit()
    def get_light_data_by_id(self, light_id):
        try:
            conn = create_connection()
            if conn:
                with conn:
                    cursor = conn.cursor(dictionary=True)

                    # Thực hiện truy vấn để lấy dữ liệu từ ID trong bảng light
                    cursor.execute('SELECT * FROM lightsensor WHERE deviceID = %s', (light_id,))
                    light_data = cursor.fetchone()

                    return light_data
        except Exception as e:
            print(f"Error: {e}")
            return None
