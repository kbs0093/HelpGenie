import cv2
import time
from PyQt5 import QtGui, QtCore
import threading
import signal
import restApi



#녹화화면 송출은 계속 되고, 파일 단위로 끊는 것은 텍스트로 안내하고, 몇 초간..

class Camera(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal()
        self.file_name = 'handsignal.avi'
        
    def setSignal(self, class_ob):
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)
        
    def run(self):
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))
        
    def counsel(self):
        self.genieTalk("이 서비스는 청각장애인분들을 위한 화면이에요. 원하시는 서비스를 수어로 입력해주세요.")
        
        time.sleep(2)
        self.recordVideo(6)
        # 영상을 서버 전송
        
        restApi.uploadVideo(self.file_name)
        # 서버로부터 결과값 받기
        # 결과값을 바탕으로 서비스 제공
        
        
    def genieTalk(self, text: str):
        self.signal_ob.emit("appendTextDeaf", "헬프지니: "+text)
        
    def recordVideo(self, time_sec):
        # change record ui
        self.signal_ob.emit("startRecord", True)
        # record start
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.file_name,fourcc, 20.0, (640, 480))

        t_end = time.time() + time_sec

        while (cap.isOpened() and (time.time() < t_end)):
            ret, frame = cap.read()
            
            if ret:
                out.write(frame)
                
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(400, 500, QtCore.Qt.KeepAspectRatio)
                self.signal_ob.emit("printImage", p)
                
        cap.release()
        out.release()
        
        # change tori ui
        self.signal_ob.emit("startRecord", False)
