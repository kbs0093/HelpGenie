import TextToVoice
import VoiceToText
import MicrophoneStream as MS
import threading
import time
import sys

class GenieVoice(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        
        #self.return_val = None # function return pointer
        #print("genie instance created: {}".format(self))
        
    def run(self):
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))
		
    def strToVoice(self, voice_text: str):
        output_file = "output.wav"
        TextToVoice.getText2VoiceStream(voice_text, output_file)
        MS.play_file(output_file)
        
    def voiceToStr(self):
        return VoiceToText.getVoice2Text()
        
        
    def voiceCounsel(self):
        self.strToVoice("안녕하세요. 원하시는 서비스를 말씀해주세요.")
        while self.is_on:
            voice_text = self.voiceToStr()
            print(voice_text)
            
            if (voice_text == "조회"):
                self.strToVoice("고객님이 이번 달 납부하실 요금은 총 육만 오천원 입니다.")
            elif (voice_text == "변경"):
                self.strToVoice("변경하시고 싶은 요금제를 말씀해주세요.")
            elif (voice_text == "해지"):
                self.strToVoice("정말로 가입정보를 해지하시겠습니까?")
            elif (voice_text == "가입"):
                self.strToVoice("가입정보를 말씀해주세요.")
            elif (voice_text == "종료"):
                self.strToVoice("서비스를 종료합니다. 좋은 하루 되세요.")
                self.is_one = False
                break
            else:
                self.strToVoice("죄송해요. 다시 한번 말씀해주세요.")
                continue
                
            self.strToVoice("상담을 계속 진행하고 싶으시면 원하시는 서비스를 말씀해주세요.")
            
            time.sleep(1)
