import cv2

def recordVideo(fname):
    
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('test.avi',fourcc, 20.0, (1280,720))

    while(cap.isOpened()):
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
