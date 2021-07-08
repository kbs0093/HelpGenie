import cv2
import time
from PyQt5 import QtGui, QtCore
import threading
import signal
import restApi
import dialogFlow
import geoMaster as GM



#녹화화면 송출은 계속 되고, 파일 단위로 끊는 것은 텍스트로 안내하고, 몇 초간..

class Camera(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal()
        self.file_name = 'sign.avi'
        
    def setSignal(self, class_ob):
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)
        
    def run(self):
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))
        
    def counsel(self):
        self.genieTalk("이 서비스는 청각장애인분들을 위한 화면이에요. 원하시는 서비스를 수어로 입력해주세요.")
        
        while self.is_on:
            time.sleep(4)
            self.recordVideo(12)
            # 영상을 서버 전송
            
            result_data = restApi.uploadVideo(self.file_name, "upload")
            self.customTalk(result_data)
            # 서버로부터 결과값 받기
            # 결과값을 바탕으로 서비스 제공
            keyword = dialogFlow.detect_intent_texts(result_data)
            print("keyword: {}".format(keyword))
            
            
            if (keyword == "가입"): # 테스트 완료
                self.serviceJoin()
            elif (keyword == "조회"): # 테스트 완료
                self.serviceCheck(False)
            elif (keyword == "이번달 조회"): # 테스트 완료
                self.serviceCheck(True)
            elif (keyword == "서비스 조회"): # 잘 안됨 (service1)
                self.serviceService()
            elif (keyword == "변경"): # 테스트 완료
                self.serviceChange()
            elif (keyword == "납부"): # 테스트 완료
                self.servicePay()
            elif (keyword == "대리점"):
                self.serviceOffice()
            else:
                self.genieTalk("죄송해요. 다시 한 번 말씀해주세요.")
                continue
            
            time.sleep(6)
            self.genieTalk("상담을 계속 진행하고 싶으시면 원하시는 서비스를 수어로 입력해주시고, 종료하시고 싶으시면 종료버튼을 눌러주세요.")

    def serviceJoin(self):
        self.genieTalk("가입절차를 시작하겠습니다. 가입정보를 입력해주세요. (숫자 두 번)")
        birth = list()
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        birth.append(result_data)
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        birth.append(result_data)
        self.customTalk(result_data)
        
        self.genieTalk("어떤 요금제를 이용하시겠어요? 수어 번호로 입력해주세요.")
        self.genieTalk("1. 55 요금제")
        self.genieTalk("2. 시즌 초이스 요금제")
        self.genieTalk("3. 슈퍼 플랜 요금제")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        choice_num = result_data
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 가입이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))
    
    def serviceCheck(self, have_this):
        if (not have_this):
            self.genieTalk("몇 월 요금제를 조회하시겠어요? (숫자 두 번)")
            month = list()
            time.sleep(4)
            self.recordVideo(5)
            result_data = restApi.uploadVideo(self.file_name, "num")
            self.customTalk(result_data)
            month.append(result_data)
            self.recordVideo(5)
            result_data = restApi.uploadVideo(self.file_name, "num")
            self.customTalk(result_data)
            month.append(result_data)
            month_result = month[0]+month[1]
            self.genieTalk("고객님께서 {}월 납부하실 금액은 65,000원 입니다.".format(month_result))
        else:
            self.genieTalk("고객님께서 7월 납부하실 금액은 65,000원 입니다.")
        
    def serviceService(self):
        self.genieTalk("고객님이 가입하신 서비스는 다음과 같습니다.")
        self.genieTalk("1. KT Seezn 서비스")
        self.genieTalk("2. 링투유 서비스")
        self.genieTalk("3. 지니 뮤직 서비스")
        
    def serviceChange(self):
        self.genieTalk("변경하실 요금제를 수어 번호로 입력해주세요. (숫자 한 번)")
        self.genieTalk("1. 55 요금제")
        self.genieTalk("2. 시즌 초이스 요금제")
        self.genieTalk("3. 슈퍼 플랜 요금제")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        choice_num = result_data
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 요금제 변경이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))
        
    def servicePay(self):
        self.genieTalk("등록하신 카드 비밀번호 두 자리를 입력해주세요. (숫자 두 번)")
        password = list()
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        password.append(result_data)
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        password.append(result_data)
        
        self.genieTalk("이번 달 납부하실 금액은 65,000원입니다. 등록하신 카드로 결제 완료되었습니다. 감사합니다.")
        
    def serviceOffice(self):
        self.genieTalk("어떤 대리점의 위치를 확인하시겠어요?\n1번 인천 지점\n2번 대전 지점\n3번 광주 지점\n확인하시고 싶은 대리점 위치를 번호로 입력해주세요.")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        office_dict = {'1': 'incheon', '2': 'daejeon', '3': 'kwangju'}
        
        if (result_data not in office_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        GM.openMap(office_dict[result_data])
            
        self.genieTalk("해당 대리점의 위치를 인터넷 창으로 띄워드렸어요.")
        
        
    def genieTalk(self, text: str):
        self.signal_ob.emit("appendTextDeaf", "헬프지니: "+text)
        
    def customTalk(self, text: str):
        self.signal_ob.emit("appendTextDeaf2", "고객님: "+text)
        
    def recordVideo(self, time_sec):
        # change record ui
        self.signal_ob.emit("startRecord", True)
        # record start
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 20)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.file_name, fourcc, 20, (640, 480))

        t_end = time.time() + time_sec

        while (cap.isOpened() and (time.time() < t_end) and self.is_on):
            ret, frame = cap.read()
            
            if ret:
                out.write(frame)
                    
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(400, 500, QtCore.Qt.KeepAspectRatio)
                self.signal_ob.emit("printImage", p)
                del(frame)
                
        cap.release()
        out.release()
        
        # change tori ui
        self.signal_ob.emit("startRecord", False)
