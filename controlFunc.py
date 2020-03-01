import cv2 as cv
from connect import *

x = 1
y = 1
w = 0
h = 0
is_fist = False
change_to_fist = False


def control():
    global x, y, w, h, is_fist, change_to_fist

    init_serial()

    cap = cv.VideoCapture(2)
    if cap is None:
        print("Cant open the camera.")
        exit(1)

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
            change_to_fist = False
        elif len(fist_rects) > 0:
            (x, y, w, h) = fist_rects[0]
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, "Fist", (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
            is_fist = True

        tarX = ((x + w / 2) / frame_width * 20 - 8)
        tarY = 16 - (y + h / 2) / frame_height * 18 + 10
        print("tarX : ", tarX, "\ttarY : ", tarY, "\tis_fist : ", is_fist)

        catch_height = 1
        if is_fist:
            if not change_to_fist:
                write_serial(tarX, tarY + 1, catch_height, 0.1, is_fist)
                change_to_fist = True
            catch_height = 3
        write_serial(tarX, tarY, catch_height, 0.1, is_fist)

        cv.imshow("Frame", frame)

        key = cv.waitKey(23)
        if key == 27:
            cv.destroyAllWindows()
            break
