import TextToVoice
import MicrophoneStream as MS
import threading

# singleton
class GenieVoice(threading.Thread):
    __instance = None
    
    @classmethod
    def instance(cls, function_name:str , *parameter):
        if (not cls.__instance):
            cls.__instance = cls(function_name, *parameter)
        return cls.__instance
        
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        print("genie instance created")
        print(self.function_name)
        print(self.parameter)
        
    def run(self):
        print("genie started")
        eval("self.{}(*self.parameter)".format(self.function_name))
		 
		
    def strToVoice(self, voice_text: str):
        output_file = "output.wav"
        TextToVoice.getText2VoiceStream(voice_text, output_file)
        MS.play_file(output_file)
