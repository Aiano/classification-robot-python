from classification.preprocess import *
from classification.division import *
from classification.knn import *

background = None
has_got_background = False
has_added_sample = False

if __name__ == '__main__':
    cap = cv.VideoCapture(2)
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
            has_added_sample = True
            result = preprocess(roi, background)
            contours, feathers = divide(result)
            draw_division(roi, contours, feathers)
            print(feathers)

            cv.imshow("roi", roi)
            cv.waitKey(0)

            label = input("Please input label : ")
            if int(label) != -1:
                add_sample(feathers, int(label))
                print("Add successfully.")

        elif has_added_sample and key == ord('t'):
            train_data()
            save_data("data.xml")
        cv.imshow("roi", roi)
