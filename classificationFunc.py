from classification.preprocess import *
from classification.division import *
from classification.knn import *
from connect import *
import time

background = None
has_got_background = False


def classification():
    global background, has_got_background
    init_serial()
    cap = cv.VideoCapture(2)
    load_data("data.xml")
    while True:
        ret, frame = cap.read()
        key = cv.waitKey(20)
        # 480x640x3
        roi = frame[123:334, 273:485]
        if key == 27:
            break
        elif key == ord('b'):
            has_got_background = True
            background = roi.copy()
            print(roi.shape)
            cv.imshow("background", background)
            cv.waitKey(0)
            cv.destroyWindow("background")
        elif has_got_background and key == ord('p'):
            result = preprocess(roi, background)
            contours, feathers = divide(result)
            draw_division(roi, contours, feathers)

            x = int((feathers[0][0][0] - 108) / 212 * 12)
            y = int(feathers[0][0][1] / 212 * 12 + 12)
            print("x", x, "y:", y)
            prediction = predict(feathers)
            target_class = prediction[0][0]
            print("target_class:", target_class)

            data = "#" + str(x) + "@" + str(y) + "@3@o"
            write_serial(data)
            print(data)

            time.sleep(2.5)

            data = "#" + str(x) + "@" + str(y) + "@0@c"
            write_serial(data)
            print(data)

            time.sleep(2.5)

            data = "#" + str(x) + "@" + str(y) + "@3@"
            write_serial(data)
            print(data)

            cv.imshow("roi", roi)
            cv.waitKey(0)

            data = "#8" + "@" + str(12 + target_class * 2) + "@1@o"
            write_serial(data)
            print(data)

            time.sleep(2.5)

            write_serial("*")

        cv.imshow("roi", roi)
    cv.destroyAllWindows()
