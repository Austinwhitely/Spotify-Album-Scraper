import pyautogui
import easyocr
import numpy as np
from PIL import Image
import pandas as pd

import cv2
from cv2.typing import MatLike


def process_img(img: MatLike):

    if img is None:
        raise ValueError("Image failed to load in imgReader.py")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/index_gray.png", gray)

    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    cv2.imwrite("temp/index_blur.png", blur)

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite("temp/index_thresh.png", thresh)

    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

    dialate = cv2.dilate(thresh, kernal, iterations=1)
    cv2.imwrite("temp/index_kernal.png", dialate)

    proccessedImg = cv2.imread("temp/index_kernal.png")
    return proccessedImg


def img_reader(img: MatLike):

    reader = easyocr.Reader(["en"], gpu=False)
    screen_image = np.array(img)
    results = reader.readtext(screen_image, mag_ratio=2)
    all_text = [text for (bbox, text, prob) in results]

    rows = []
    for i in range(0, len(all_text), 2):
        row = all_text[i : i + 2]
        while len(row) < 2:
            row.append("")
        rows.append(row)

    df = pd.DataFrame(rows, columns=["Title", "Artist"])
    return df
