import cv2 as cv
import serial
import time

x = 1
y = 1
w = 0
h = 0
is_fist = False
now_x = 0
now_y = 12
count = 0
string2 = "0@o\n"
is_down = True


def control():
    global x, y, w, h, is_fist, now_y, now_x, count, string2,is_down
    cap = cv.VideoCapture(2)
    if cap is None:
        print("Cant open the camera.")
        exit(1)

    # serial
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    if not ser.isOpen():
        print("Cant open serial")
        exit(1)

    # serial

    frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH) / 3
    frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) / 3
    cap.set(cv.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, frame_height)
    w = frame_width
    h = frame_height
    fps = cap.get(cv.CAP_PROP_FPS)
    # delay = int(1000 / fps)
    print("Frame : ", frame_width, "x", frame_height)
    print("FPS : ", fps)

    cv.namedWindow("Frame", cv.WINDOW_KEEPRATIO)

    fist_cascade = cv.CascadeClassifier("fist.xml")
    palm_cascade = cv.CascadeClassifier("palm.xml")

    while True:
        ret, frame = cap.read()
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        palm_rects = palm_cascade.detectMultiScale(gray_frame, scaleFactor=1.03, minNeighbors=2)
        fist_rects = fist_cascade.detectMultiScale(gray_frame, scaleFactor=1.03, minNeighbors=2)
        if len(palm_rects) > 0:
            (x, y, w, h) = palm_rects[0]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, "Palm", (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
            is_fist = False
        elif len(fist_rects) > 0:
            (x, y, w, h) = fist_rects[0]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, "Fist", (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
            is_fist = True

        tarX = int(((x + w / 2) / frame_width * 20 - 8))
        tarY = int(16 - (y + h / 2) / frame_height * 18 + 10)
        print("tarX : ", tarX, "\ttarY : ", tarY, "\tis_fist : ", is_fist)

        count += 1
        if count == 8:
            if is_fist:
                tarY += 1
            string = "%" + str(tarX) + "@" + str(tarY) + "@" + string2
            if is_fist:
                string2 = "3@c\n"
                if is_down:
                    string = "%" + str(tarX) + "@" + str(tarY) + "@" + "0@c\n"
                    time.sleep(0.6)
                    is_down = False
            else:
                string2 = "0@o\n"
                is_down = True
            ser.write(string.encode("utf-8"))
            count = 0

        cv.imshow("Frame", frame)

        key = cv.waitKey(50)
        if key == 27:
            break

    cv.destroyAllWindows()
