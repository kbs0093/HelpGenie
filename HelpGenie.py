import VoiceToText
import MicrophoneStream as MS
import TextToVoice
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws
import cv2
import GenieButton
import CameraStream as CS
import VideoPlay as VP

import userInterface as ui
import sys
import threading
import time

KWSID = ['오늘', '지니야', '친구야', '자기야', 'help지니']
RATE = 16000
CHUNK = 512


'''
class DataDeliv():
    function_dict = dict()
    
    def __init__(self, obj):
        if (obj.__class__.__name__ == "TimeMeasure"):
            DataDeliv.function_dict["exit"] = obj.exit
            
    def emit(self, function_name, *parameter):
        eval("DataDeliv.function_dict['{}'](*parameter)".format(function_name))
        
class TimeMeasure(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_on = True
	
    def run(self):
        count_time = 0
        
        while self.is_on:
            if (count_time == 5 and self.is_on):
                print("5초 경과 시각장애인 UI 전환")
                break
            time.sleep(1)
            count_time += 1
            print(count_time)
    
    def exit(self):
        print("TimeMeasure thread exit")
        self.is_on = False
'''

def detect():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        for content in audio_generator:

                rc = ktkws.detect(content)
                rms = audioop.rms(content,2)
                #print('audio rms = %d' % (rms))

                if (rc == 1):
                        MS.play_file("./Data/sample_sound.wav")
                        return 200
                
def initHelpGenie(key_word = '오늘'):
    rc = ktkws.init("./Data/kwsmodel.pack")

    print ('init rc = %d' % (rc))
    rc = ktkws.start()
    print ('start rc = %d' % (rc))
    print ('\n호출어를 불러보세요~\n')
    ktkws.set_keyword(KWSID.index(key_word))
    rc = detect()
    print ('detect rc = %d' % (rc))
    print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
    ktkws.stop()
    return rc
    
def btn_test(key_word = 'help지니'):
    global btn_status
    rc = ktkws.init("../data/kwsmodel.pack")
    print ('init rc = %d' % (rc))
    rc = ktkws.start()
    print ('start rc = %d' % (rc))
    print ('\n버튼을 눌러보세요~\n')
    ktkws.set_keyword(KWSID.index(key_word))
    rc = GenieButton.btn_detect()
    print ('detect rc = %d' % (rc))
    print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
    ktkws.stop()
    return rc
    


def initService():
    # 타임 스레드 생성 및 시그널 초기화
    '''
    time_th = TimeMeasure()
    data_deliv = DataDeliv(time_th)
    ui.data_deliv = data_deliv
    '''
    
    # UI 출력
    app = ui.QtWidgets.QApplication([""])
    window = ui.MainWindow()
    window.show()
    #time_th.start()
    sys.exit(app.exec_())
    
    
    # 안내 음성 재생
    '''
    voice_text = '음성 테스트 데이터입니다.'
    output_file = "output.wav"
    TextToVoice.getText2VoiceStream(voice_text, output_file)
    MS.play_file(output_file)
    
    '''
    
    
    
    #fileName = 'handSignal.avi'
    
    #VP.VideoPlay(fileName)
    

def main():
    # 버튼 클릭 (UI 버튼 클릭시 실행 함수)

    #button = btn_test()
    
    #if button == 200 :
    #    CS.recordVideo()

    
    initService()
    
    #VP.VideoPlay(fileName)


    # 결과 값 출력

    


if __name__ == '__main__':
    main()
