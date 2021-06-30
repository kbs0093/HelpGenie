import cv2
import time




def recordVideo():

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('handSignal.avi',fourcc, 20.0, (640, 480))
    
    # 5 second Record
    t_end = time.time() + 5 

    while(cap.isOpened() & (time.time() < t_end)):
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    

    cap.release()
    out.release()
    cv2.destroyAllWindows()
