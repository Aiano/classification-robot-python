import numpy as np
import cv2 as cv

area_threshold = 5


def divide(input_img: np.ndarray):
    # input_img : a binary img
    # output_contours
    # output_list:
    # [[coordinate...],
    #   [area...],
    #   [aspect ratio...]]
    coordinate = []
    area = []
    ar = []
    output_contours = []
    contours, hierarchy = cv.findContours(input_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) < 1:
        print("Find nothing.")
        return None, None
    for contour in contours:
        tmp_area = cv.contourArea(contour)
        if tmp_area >= area_threshold:
            output_contours.append(contour)
            M = cv.moments(contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            rect = cv.minAreaRect(contour)
            width = rect[1][0]
            height = rect[1][1]

            coordinate.append([cx, cy])
            area.append(tmp_area)
            if width > height:
                ar.append(width / height)
            else:
                ar.append(height / width)

    output_list = [coordinate, area, ar]

    return output_contours, output_list


def draw_division(input_img: np.ndarray, input_contours: list, input_list: list) -> None:
    # input_contours
    # input_list:
    # [[coordinate...],
    #   [area...],
    #   [aspect ratio...]]
    cv.drawContours(input_img, input_contours, -1, (0, 255, 0), 3)
    coordinates, areas, ars = input_list
    if not len(coordinates) == len(areas) == len(ars):
        print("Error occur in function draw_division : length error.")
        exit(1)
    for i in range(len(coordinates)):
        cv.putText(input_img, "Area : " + str(areas[i]), tuple(coordinates[i]), cv.FONT_ITALIC, 0.8, (0, 255, 0), 2)
        cv.putText(input_img, "Ar:" + str(ars[i]), (coordinates[i][0], coordinates[i][1] + 20), cv.FONT_ITALIC, 0.8,
                   (0, 200, 0), 2)
    return
