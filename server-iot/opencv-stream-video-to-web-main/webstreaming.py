# import the necessary packages
from pyimagesearch.motion_detection.singlemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import time
import cv2

import paho.mqtt.client as mqtt
import json

import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

from Model.lightRepository import LightRepository
from Model.soilRepository import SoilRepository
from Model.dht11 import DHT11Repository
from Model.lightDevice import LightDeviceRepository
from Model.pumpDevice import PumpDeviceRepository
from Model.history import HistoryRepository
from Model.diagnose import DiagnoseRepository

from datetime import datetime

from flask import request, flash, session

from Model.connect import create_connection


# MQTT broker information
from cloudinary.uploader import upload
import cloudinary
import requests

from PIL import Image
from io import BytesIO

cloudinary.config(
    cloud_name="dsjuckdxu",
    api_key="973371356842627",
    api_secret="zJ5bMJgfkw3XBdyBocwO8Kgs1us"
)

# MQTT broker information
mqtt_broker = "192.168.1.8"

mqtt_port = 1883
mqtt_topic = "iot"
relay_topic = "relay/control"
relay_topic2 = "relay2/control"
auto_topic = "auto/control"

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
app.secret_key = b'\x9b\xfa\xa8\x85\xf2\xce\x1e\x13\x0b\xd8\x84\xac\x04\xed\x9e\xe9\xd8\x7e\x2b\x90\x6b\xfa\x2d'
# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)
# =========================================================================================================
from flask import Flask, request,render_template, redirect, url_for,jsonify

received_data = {}  # Create a global variable to store received data

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    global received_data
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    # Update data dictionary with received JSON
    received_data = (payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

# Start MQTT loop in a separate thread
client.loop_start()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    return render_template('overview.html', data=(received_data))
    # return render_template('index.html', data=jsonify(received_data))

@app.route('/camera')
def camera():
    if 'username' not in session:
        return redirect('/login')
    return render_template('camera.html')

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect('/login')
    history_repo = HistoryRepository()
    data = history_repo.get_history_data()
    return render_template('history1.html', data=data)
    
@app.route('/diagnose')
def diagnose():
    if 'username' not in session:
        return redirect('/login')
    history_repo = DiagnoseRepository()
    data = history_repo.get_diagnose_data()
    return render_template('diagnose.html', data=data)   

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    conn = create_connection()
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        cursor = conn.cursor()
        cursor.execute('SELECT password FROM account WHERE username = %s', (username,))
        result = cursor.fetchone()
        if result and result[0] == current_password:
            if new_password == confirm_password:
                cursor.execute('UPDATE account SET password = %s WHERE username = %s', (new_password, username))
                conn.commit()
                cursor.close()

                flash('Mật khẩu đã được cập nhật thành công!', 'success')
                return redirect('/')
            else:
                flash('Xác nhận mật khẩu không khớp!', 'error')
        else:
            flash('Mật khẩu hiện tại không chính xác!', 'error')
            cursor.close()

    return render_template('profile.html', username=username)


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if 'username' not in session:
        return redirect('/login')
    conn = create_connection()
    if 'username' not in session:
        return redirect('/login')

    # Kiểm tra vai trò của người dùng
    username = session['username']
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM account WHERE username = %s', (username,))
    user_role = cursor.fetchone()
    cursor.close()

    if user_role and user_role[0] == 1:
        if request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']

            cursor = conn.cursor()
            cursor.execute('INSERT INTO account (username, password, role) VALUES (%s, %s, %s)', (new_username, new_password, 0))
            conn.commit()
            cursor.close()

            # flash('Người dùng đã được tạo thành công!', 'success')
            return redirect('/')

        return render_template('create.html')
    else:
        # flash('Bạn không có quyền truy cập vào trang này.', 'error')
        return redirect('/')
    
@app.route('/login', methods = ['get', 'post'])
def login():
    conn = create_connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM account WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[1] == password:
            session['username'] = username
            # flash('Đăng nhập thành công!', 'success')
            return redirect('/')
        # else:
            # flash('Tên người dùng hoặc mật khẩu không đúng.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/received_data')
def get_data():
    if 'username' not in session:
        return redirect('/login')
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data = json.loads(received_data)
    # Lưu cường độ ánh sáng
    cuong_do_anh_sang = (json_data).get("cuong_do_anh_sang")
    light_repo = LightRepository()
    light_repo.add_light_data(intensity=cuong_do_anh_sang, time_now=time_now)
    
    # Lưu độ ẩm đất
    do_am_dat= (json_data).get("do_am_dat")
    soil_repo = SoilRepository()
    soil_repo.add_soil_data(SoilHumidity=do_am_dat, time_now=time_now)
    
    # Lưu nhiệt độ, độ ẩm phòng
    nhiet_do_phong =  (json_data).get("nhiet_do")
    do_am_phong =  (json_data).get("do_am")
    dht11_repo= DHT11Repository()
    dht11_repo.add_dht11_data(Temperature=nhiet_do_phong,Humidity= do_am_phong, time_now=time_now)
    
    # Lưu tạng thái máy bơm
    pump_status =  (json_data).get("pump_status")
    pumpdevice_repo = PumpDeviceRepository()
    pumpdevice_repo.add_pumpdevice_data(State= pump_status, time_now= time_now)
    
    # lưu trạng thái đèn
    light_status =  (json_data).get("light_status")
    lightdevice_repo = LightDeviceRepository()
    lightdevice_repo.add_lightdevice_data(State= light_status, time_now= time_now)
    
    # Lưu vào bảng history
    history_repo = HistoryRepository()
    history_repo.add_history_data(Time=time_now, Temperature= nhiet_do_phong, Humidity=do_am_phong, Light= cuong_do_anh_sang, Soil=do_am_dat, pump_state= pump_status, light_state= light_status )
    return jsonify(received_data)
# ===========================================================================================================
@app.route('/turn_on_relay1', methods=['POST'])
def turn_on_relay1():
	# Extract data from the request
    data = request.json

    # Process the data (in this example, assuming data includes 'relay' key)
    relay_number = data.get('relay')

    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(relay_topic, "ON")

    print(f"Turning on relay {relay_number}")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'Relay {relay_number} turned on'}
    
    return jsonify(response_data)

@app.route('/turn_on_relay2', methods=['POST'])
def turn_on_relay2():
	# Extract data from the request
    data = request.json

    # Process the data (in this example, assuming data includes 'relay' key)
    relay_number = data.get('relay')

    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(relay_topic2, "ON")

    print(f"Turning on relay {relay_number}")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'Relay {relay_number} turned on'}
    
    return jsonify(response_data)

@app.route('/turn_off_relay1', methods=['POST'])
def turn_off_relay1():
	# Extract data from the request
    data = request.json

    # Process the data (in this example, assuming data includes 'relay' key)
    relay_number = data.get('relay')

    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(relay_topic, "OFF")

    print(f"Turning off relay {relay_number}")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'Relay {relay_number} turned off'}
    
    #Lưu trạng thái máy bơm
    pumpdevice_repo = PumpDeviceRepository()
    pumpdevice_repo.add_pumpdevice_data(State= 'OFF', time_now= time_now)
    
    return jsonify(response_data)

@app.route('/turn_off_relay2', methods=['POST'])
def turn_off_relay2():
	# Extract data from the request
    data = request.json

    # Process the data (in this example, assuming data includes 'relay' key)
    relay_number = data.get('relay')

    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(relay_topic2, "OFF")

    print(f"Turning off relay {relay_number}")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'Relay {relay_number} turned off'}
    
    return jsonify(response_data)

@app.route('/turn_on_auto', methods=['POST'])
def turn_on_auto():
    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(auto_topic, "ON")

    print(f"Turning on auto mode")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'auto mode turned on'}

    return jsonify(response_data)

@app.route('/turn_off_auto', methods=['POST'])
def turn_off_auto():
    # Perform actions based on the relay_number (you may turn on the relay here)
    # Replace the following line with your actual relay control logic
    client.publish(auto_topic, "OFF")

    print(f"Turning off auto mode")
    # Dummy response for demonstration purposes
    response_data = {'status': 'success', 'message': f'auto mode turned off'}

    return jsonify(response_data)
# ==============================================================================================
filepath = 'model.h5'
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")

def pred_tomato_dieas(tomato_plant):
  time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  image_url = cloudinary.utils.cloudinary_url(tomato_plant)[0] #Đọc image từ cloudinary
  response = requests.get(image_url)
  image_content = response.content

  test_image = load_img(BytesIO(image_content), target_size = (128, 128)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  diagnose_repo = DiagnoseRepository()
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Apple - Bệnh ghẻ (Apple Scab Disease)", Time=time_now )
        return "Apple - Bệnh ghẻ (Apple Scab Disease)", 'Apple_Scab_Disease.html'
  elif pred==1:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Apple - Bệnh thối đen (Apple Black Rot)", Time=time_now )
        return "Apple - Bệnh thối đen (Apple Black Rot)", 'Apple_Black_Rot.html'
  elif pred==2:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Apple - Bệnh gỉ sắt táo (Cedar Apple Rust)", Time=time_now )
        return "Apple - Bệnh gỉ sắt táo (Cedar Apple Rust)", 'Common_Rust.html'
  elif pred==3:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Apple - Không có bệnh", Time=time_now )
        return "Apple - Không có bệnh", 'Apple_Healthy.html'
  elif pred==4:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Không phải hình ảnh lá cây", Time=time_now )
        return "Không phải hình ảnh lá cây", 'No_Leaves.html'
  elif pred==5:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Đốm lá Cercospora/Đốm lá xám (Cercospora Leaf Spot/Gray Leaf Spot)", Time=time_now )
        return "Đốm lá Cercospora/Đốm lá xám (Cercospora Leaf Spot/Gray Leaf Spot)", 'Cercospora_Leaf_Spot.html'
  elif pred==6:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Corn - Bệnh gỉ sắt (Common Rust)", Time=time_now )
        return "Corn - Bệnh gỉ sắt (Common Rust)", 'Common_Rust.html'
  elif pred==7:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Corn - Bệnh bạc lá (Northern Leaf Blight)", Time=time_now )
        return "Corn - Bệnh bạc lá (Northern Leaf Blight)", 'Northern_Leaf_Blight.html'
  elif pred==8:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Corn - Không có bệnh", Time=time_now )
        return "Corn - Không có bệnh", 'Corn_Healthy.html'
  elif pred==9:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Grape - Bệnh đốm lá (Black Rot)", Time=time_now )
        return "Grape - Bệnh đốm lá (Black Rot)", 'Grape_Black_Rot.html'
  elif pred==10:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Grape - Bệnh sở đen (Esca (Black Measles))", Time=time_now )
        return "Grape - Bệnh sở đen (Esca (Black Measles))", 'Esca.html'
  elif pred==11:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Grape - Bệnh bạc lá (Leaf Blight (Isariopsis Leaf Spot))", Time=time_now )
        return "Grape - Bệnh bạc lá (Leaf Blight (Isariopsis Leaf Spot))", 'Leaf_Blight.html'
  elif pred==12:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Grape - Không có bệnh", Time=time_now )
        return "Grape - Không có bệnh", 'Grape_Healthy.html'        
  elif pred==13:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Potato - Bệnh bạc lá sớm (Early Blight)", Time=time_now )
        return "Potato - Bệnh bạc lá sớm (Early Blight)", 'Early_Blight_Disease.html'
  elif pred==14:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Potato - Bệnh mốc sương (Late Blight)", Time=time_now )
        return "Potato - Bệnh mốc sương (Late Blight)", 'Late_Blight_Disease.html'
  elif pred==15:
        diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Potato - Không có bệnh", Time=time_now )
        return "Potato - Không có bênh", 'Potato_Healthy.html'
  elif pred==16:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh đốm vi khuẩn (Bacteria Spot Disease)", Time=time_now )
      return "Tomato - Bệnh đốm vi khuẩn (Bacteria Spot Disease)", 'Bacterial_Spot_Disease.html'
       
  elif pred==17:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh bạc lá sớm (Early Blight Disease)", Time=time_now )
      return "Tomato - Bệnh bạc lá sớm (Early Blight Disease)", 'Early_Blight_Disease.html'
        
  elif pred==18:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Khoẻ mạnh", Time=time_now )
      return "Tomato - Khoẻ mạnh", 'Tomato_Healthy.html'
        
  elif pred==19:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh mốc sương (Late Blight Disease)", Time=time_now )
      return "Tomato - Bệnh mốc sương (Late Blight Disease)", 'Late_Blight_Disease.html'
       
  elif pred==20:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh mốc lá (Leaf Mold Disease)", Time=time_now )
      return "Tomato - Bệnh mốc lá (Leaf Mold Disease)", 'Leaf_Mold_Disease.html'
        
  elif pred==21:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh đốm lá Septoria (Septoria Leaf Spot Disease)", Time=time_now )
      return "Tomato - Bệnh đốm lá Septoria (Septoria Leaf Spot Disease)", 'Septoria_Leaf_Spot_Disease.html'
        
  elif pred==22:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh đốm mục chấm (Target Spot Disease)", Time=time_now )
      return "Tomato - Bệnh đốm mục chấm (Target Spot Disease)", 'Target_Spot_Disease.html'
        
  elif pred==23:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh virus vàng lá xoăn (Yellow Leaf Curl Virus Disease)", Time=time_now )
      return "Tomato - Bệnh virus vàng lá xoăn (Yellow Leaf Curl Virus Disease)", 'Yellow_Leaf_Curl_Virus_Disease.html'
  elif pred==24:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh khảm virus (Tomato Mosaic Virus Disease)", Time=time_now )
      return "Tomato - Bệnh khảm virus (Tomato Mosaic Virus Disease)", 'Mosaic_Virus.html'
        
  elif pred==25:
      diagnose_repo.add_diagnose_data(Link_image= tomato_plant, Diagnose= "Tomato - Bệnh nhện đỏ hai đốm (Two Spotted Spider Mite Disease)", Time=time_now )
      return "Tomato - Bệnh nhện đỏ hai đốm (Two Spotted Spider Mite Disease)", 'Two_Spotted_Spider_Mite_Disease.html'


@app.route("/predict", methods = ['GET','POST'])
def predict():
     if 'username' not in session:
        return redirect('/login')
     if request.method == 'POST':
        file = request.files['image'] # fet input

        result = upload(file)
        public_url = result['secure_url']
        print(public_url)

        # filename = file.filename        
        # print("@@ Input posted = ", filename)
        
        # file_path = os.path.join('./upload/', filename)
        # file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_tomato_dieas(tomato_plant=public_url)
              
        return render_template(output_page, pred_output = pred, user_image = public_url)
# ==========================================================================================================
@app.route("/view-camera")
def view_camera():
	# return the rendered template
    if 'username' not in session:
     return redirect('/login')
	
    return render_template("index.html")

def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock
	# initialize the motion detector and the total number of frames
	# read thus far
	md = SingleMotionDetector(accumWeight=0.1)
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=600)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (20, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		if total > frameCount:
			# detect motion in the image
			motion = md.detect(gray)
			# check to see if motion was found in the frame
			if motion is not None:
				# unpack the tuple and draw the box surrounding the
				# "motion area" on the output frame
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
					(0, 0, 255), 2)
		
		# update the background model and increment the total number
		# of frames read thus far
		md.update(gray)
		total += 1
		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--ip", type=str, required=True,
	# 	help="ip address of the device")
	# ap.add_argument("-o", "--port", type=int, required=True,
	# 	help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# start the flask app
	# app.run(host=args["ip"], port=args["port"], debug=True,
	app.run(host="0.0.0.0", port=5000, debug=True,
		threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()
