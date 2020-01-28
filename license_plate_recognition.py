import time
import multiprocessing as mp
from hyperlpr import *
import cv2

faceCascade = cv2.CascadeClassifier('./myhaar.xml')
pointTime = 0

def image_put(q, user, pwd, ip, channel=1):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s//Streaming/Channels/%d" % (user, pwd, ip, channel))

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)


def image_get(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow(window_name, gray)

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for (x,y,w,h) in faces:
            print(faces)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
            LPR(time.time(),frame)
        time.sleep(0.1)

        cv2.waitKey(1)

def LPR(requestTime,frame):
    global pointTime
    # print(requestTime,pointTime,requestTime - pointTime)
    if(requestTime - pointTime >1.5):
        result = HyperLPR_plate_recognition(frame)
        im_url = r'E:/workspace/LPR/IMG/check/%s.jpg'%time.strftime("%H-%M-%S", time.localtime())
        print(im_url)
        cv2.imwrite(im_url,frame)
        if(len(result)>0):
            print(result)
            im_url = r'E:/workspace/LPR/IMG/success/R-%s.jpg'%(result[0][0]+"-"+str(result[0][1])[:5])
            print("success==",im_url)
            cv2.imwrite(im_url,frame)
            pointTime = requestTime

def run_single_camera():
    user_name, user_pwd, camera_ip = "admin", "admin123456", "192.168.1.1:554"

    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)),
                 mp.Process(target=image_get, args=(queue, camera_ip))]

    [process.start() for process in processes]
    [process.join() for process in processes]


if __name__ == '__main__':
    run_single_camera()