import cv2
import time


def recordVideo():

    start = time.time()    
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('handSignal.avi',fourcc, 20.0, (640, 480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if start >= 5:
            print('5초 경과 - 녹화 중지')
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
