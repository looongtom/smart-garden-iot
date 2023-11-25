from datetime import datetime
import os
import cv2 

cam_port = 0
cam = cv2.VideoCapture(cv2.CAP_DSHOW) 
  
# reading the input using the camera 
result, image = cam.read() 
  
# If image will detected without any error,  
# show result 
if result: 
    currentDateAndTime = datetime.now()
    currentDateAndTime=currentDateAndTime.strftime("%d_%b_%y_%H_%M_%S")
    imageName = "image_"+str(currentDateAndTime)+".png"
    file_path = os.path.join('./server-iot/opencv-stream-video-to-web-main/upload/capture/', imageName)

    print(file_path)
    # showing result, it take frame name and image  
    # output 
    imshow(file_path, image) 
  
    # saving image in local storage 
    imwrite(file_path, image) 
# D:\IOT\smart-garden-iot\server-iot\opencv-stream-video-to-web-main\upload
  
# If captured image is corrupted, moving to else part 
else: 
    print("No image detected. Please! try again") 
