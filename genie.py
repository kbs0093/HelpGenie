import TextToVoice
import VoiceToText
import dialogFlow
import MicrophoneStream as MS
import threading
import time
import sys

import signal

class GenieVoice(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal()
        #self.return_val = None # function return pointer
        #print("genie instance created: {}".format(self))
        
    def setSignal(self, class_ob): #시그널을 쓰지않는 객체의일 수도 있기때문에 정의
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)
        
    def run(self): #스레드 객체는 한번만 실행할 수 있고, 여러 가지 분리된 기능을 구현하기 위해 이렇게 작성
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))
		
    def strToVoice(self, voice_text: str):
        output_file = "output.wav"
        TextToVoice.getText2VoiceStream(voice_text, output_file)
        MS.play_file(output_file)
        
    def voiceToStr(self): #음성 받아서 핵심 키워드 추출
        return VoiceToText.getVoice2Text()
        
    def genieTalk(self, text: str):
        self.signal_ob.emit("appendTextBlind", "헬프지니: "+text)
        self.strToVoice(text)
        
    def voiceCounsel(self):
        self.genieTalk("안녕하세요. 원하시는 서비스를 말씀해주세요.")
        
        while self.is_on:
            voice_text = self.voiceToStr()
            self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
            keyword = dialogFlow.detect_intent_texts(voice_text)
            print("keyword: {}".format(keyword))
            
            if (keyword == "조회"):
                self.genieTalk("고객님이 이번 달 납부하실 요금은 총 육만 오천원 입니다.")
            elif (keyword == "변경"):
                self.genieTalk("변경하시고 싶은 요금제를 말씀해주세요.")
            elif (keyword == "해지"):
                self.genieTalk("정말로 가입정보를 해지하시겠습니까?")
            elif (keyword == "가입"):
                self.genieTalk("가입정보를 말씀해주세요.")
            elif (keyword == "종료"):
                self.genieTalk("서비스를 종료합니다. 좋은 하루 되세요.")
                self.is_one = False
                break
            else:
                self.genieTalk("죄송해요. 다시 한번 말씀해주세요.")
                continue
            
            time.sleep(2)    
            self.genieTalk("상담을 계속 진행하고 싶으시면 원하시는 서비스를 말씀해주세요.")
            
            
