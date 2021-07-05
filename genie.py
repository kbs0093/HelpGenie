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
        
    def genieTalk(self, text: str, is_voice = True):
        self.signal_ob.emit("appendTextBlind", "헬프지니: "+text)
        if isVoice:
            self.strToVoice(text)
        
    def voiceCounsel(self):
        self.genieTalk("이 서비스는 시각장애인분들을 위한 거에요. 원하시는 서비스를 말씀해주세요.")
        
        while self.is_on:
            voice_text = self.voiceToStr()
            self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
            keyword = dialogFlow.detect_intent_texts(voice_text)
            print("keyword: {}".format(keyword))
            
            if (keyword == "가입"):
                self.serviceJoin()
            elif (keyword == "조회"):
                self.serviceCheck(False)
            elif (keyword == "이번달 조회"): # 학습
                self.serviceCheck(True)
            elif (keyword == "서비스 조회"): # 학습
                self.serviceService()
            elif (keyword == "변경"):
                self.serviceChange()
            elif (keyword == "납부"): # 학습
                self.servicePay()
            elif (keyword == "종료"):
                self.genieTalk("서비스를 종료합니다. 좋은 하루 되세요.")
                self.is_one = False
                break
            else:
                self.genieTalk("죄송해요. 다시 한번 말씀해주세요.")
                continue
            
            time.sleep(2)    
            self.genieTalk("상담을 계속 진행하고 싶으시면 원하시는 서비스를 말씀해주세요.")
 
    def serviceJoin(self):
        self.genieTalk("가입절차를 시작하겠습니다. 생년월일을 말씀해주세요.")
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
        
        self.genieTalk("가입하실 수 있는 요금제를 말씀 드릴게요. 가입하고 싶은 요금제를 번호로 말씀해주세요.")
        self.genieTalk("1. 55 요금제\n2. 시즌 초이스 요금제\n3. 슈퍼 플랜 요금", False)
 
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
        
        choice_num = voice_text[0] # 1번 -> 1
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 가입이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))
    
    def serviceCheck(self, have_this):
        if (not have_this):
            self.genieTalk("몇 월 요금제를 조회하시겠어요?") # ex) 1월, 2월, 3월
            voice_text = self.voiceToStr()
            self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
            
            result_data = voice_text[0] # 1월 ->1
            self.genieTalk("고객님께서 {}월 납부하실 금액은 65,000원 입니다.".format(result_data))
        else:
            self.genieTalk("고객님께서 7월 납부하실 금액은 65,000원 입니다.")
        
    def serviceService(self):
        self.genieTalk("고객님이 가입하신 서비스는 다음과 같습니다.")
        self.genieTalk("1. 지니 뮤직\n2. 시콜 투 유\n3. KT Seezn", False)
        
    def serviceChange(self):
        self.genieTalk("변경하실 요금제를 번호로 말씀해주세요.")
        self.genieTalk("1. 55 요금제\n2. 시즌 초이스 요금제\n3. 슈퍼 플랜 요금", False)
        
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
        result_data = voice_text[0] # 1번 -> 1
        choice_num = result_data
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 요금제 변경이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))
        
    def servicePay(self):
        self.genieTalk("등록하신 카드 비밀번호 두 자리를 말씀해주세요.")
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
        
        self.genieTalk("이번 달 납부하실 금액은 65,000원입니다. 등록하신 카드로 결제 완료되었습니다. 감사합니다.")
    
    
            
            
