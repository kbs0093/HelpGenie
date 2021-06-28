import cv2 

url = 'rtsp://helpgenie:k5336309@192.168.25.23:554/stream1'
cap = cv2.VideoCapture(url)
   
def playVideo():
	
    while True :
        ret, frame = cap.read()
        cv2.imshow("video", frame)
        cv2.waitKey(1)
 
