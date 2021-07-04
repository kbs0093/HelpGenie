import cv2
import time
from PyQt5 import QtGui, QtCore
import threading
import signal



#녹화화면 송출은 계속 되고, 파일 단위로 끊는 것은 텍스트로 안내하고, 몇 초간..

class Camera(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)
        
    def setSignal(self, class_ob):
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)
        
    def run(self):
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))
        
    def counsel(self):
        print("counsel start")
        pass
        
    def genieTalk(self, text: str):
        # To do
        self.signal_ob.emit("appendTextDeaf", "헬프지니: "+text)
        self.strToVoice(text)
        
    def recordVideo(self):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('handSignal.avi',fourcc, 20.0, (800, 600))

        # 5 second Record
        t_end = time.time() + 10
        
        print(cap.isOpened() and (time.time() < t_end))

        while (True):
            ret, frame = cap.read()
            
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(400, 500, QtCore.Qt.KeepAspectRatio)
                self.signal_ob.emit("printImage", p)
                
                out.write(frame)
            
                
        cap.release()
        out.release()
        # change tori
        self.signal_ob.emit("reapint")
