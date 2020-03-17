from classification.preprocess import *
from classification.division import *
from classification.knn import *
from connect import *

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

            x = (feathers[0][0][0] - 108) / 212 * 12
            y = feathers[0][0][1] / 212 * 12 + 12
            print("x", x, "y:", y)
            prediction = predict(feathers)
            target_class = prediction[0][0]
            print("target_class:", target_class)

            cv.imshow("roi", roi)
            cv.waitKey(0)

            write_serial(x, y, 3, 2.5, False)
            print("X : ", x, "\tY : ", y, "\tZ:", 3, "\tDelay Seconds : ", 2.5, "\tCatch Condition : ", False)

            write_serial(x, y, 0, 1, False)
            print("X : ", x, "\tY : ", y, "\tZ:", 0, "\tDelay Seconds : ", 1, "\tCatch Condition : ", False)

            write_serial(x, y, 0, 1, True)
            print("X : ", x, "\tY : ", y, "\tZ:", 0, "\tDelay Seconds : ", 1, "\tCatch Condition : ", True)

            write_serial(x, y, 3, 1, True)
            print("X : ", x, "\tY : ", y, "\tZ:", 3, "\tDelay Seconds : ", 1, "\tCatch Condition : ", True)

            write_serial(8, 12 + target_class * 2, 1, 2.5, True)
            print("X : ", 8, "\tY : ", 12 + target_class * 2, "\tZ:", 1, "\tDelay Seconds : ", 2.5,
                  "\tCatch Condition : ", True)

            write_serial(8, 12 + target_class * 2, 1, 1, False)
            print("X : ", 8, "\tY : ", 12 + target_class * 2, "\tZ:", 1, "\tDelay Seconds : ", 1,
                  "\tCatch Condition : ", False)

        cv.imshow("roi", roi)
    cv.destroyAllWindows()
