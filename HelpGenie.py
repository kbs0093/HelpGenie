import VoiceToText
import MicrophoneStream as MS
import TextToVoice
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws
import MicrophoneStream as MS
import cv2
import GenieButton
import CameraStream as CS

KWSID = ['오늘', '지니야', '친구야', '자기야', 'help지니']
RATE = 16000
CHUNK = 512

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

def main():


    # 5초 후 음성 인식 시작

    # returnValue = initHelpGenie()
    
    # if returnValue == 200:
    #     text = VoiceToText.getVoice2Text()


    # 버튼 클릭 (UI 버튼 클릭시 실행 함수)

    button = btn_test()
    
    if button == 200 :
        CS.recordVideo()



    # 결과 값 출력

    result = '음성 테스트 데이터입니다 여기를 바꿔주세요'
    print(result)





        
        

if __name__ == '__main__':
    main()
