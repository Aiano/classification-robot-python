import numpy as np
import cv2 as cv


def preprocess(input_img: np.ndarray, background: np.ndarray) -> np.ndarray:
    # Check if input_img is empty.
    if input is None:
        print("Error occur in function preprocess : input_img is empty.")
        exit(1)

    # Convert input_img and background into gray scale
    tmp_input_img_gray = cv.cvtColor(input_img, cv.COLOR_BGR2GRAY)
    tmp_background_gray = cv.cvtColor(background, cv.COLOR_BGR2GRAY)

    # Put Median Blur on above images
    tmp_input_img_gray_blur = cv.medianBlur(tmp_input_img_gray, 3)
    tmp_background_gray_blur = cv.medianBlur(tmp_background_gray, 3)

    # optical elimination
    # There are two methods, we choose subtraction
    # Method subtraction:
    # if we have an "Optical pattern" L and a "Image" I
    # the "result" R = L - I
    tmp_mix = cv.subtract(tmp_background_gray_blur, tmp_input_img_gray_blur)

    # threshold
    _, result = cv.threshold(tmp_mix, 30, 255, cv.THRESH_BINARY)
    return result
