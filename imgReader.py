import pyautogui
import easyocr
import numpy as np
from PIL import Image
import pandas as pd

import cv2
from cv2.typing import MatLike

replacements = {
    "_": " ",
    ";": ",",
    ":": ",",
}

def process_img(img: MatLike):

    if img is None:
        raise ValueError("Image failed to load in imgReader.py")

    clean_img = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/index_gray.png", gray)

    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    cv2.imwrite("temp/index_blur.png", blur)

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite("temp/index_thresh.png", thresh)

    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dialate = cv2.dilate(thresh, kernal, iterations=1)
    cv2.imwrite("temp/index_dilate.png", dialate)

    cnts = cv2.findContours(dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    
    boxes = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w < 25:
            continue
        boxes.append((x, y, w, h))

    boxes = sorted(boxes, key=lambda b: (b[1] // 15, b[0]))

    cell_crops = []
    for x, y, w, h in boxes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
        crop = clean_img[y : y + h, x : x + w]
        cell_crops.append(crop)

    cv2.imwrite("temp/index_bbox.png", img)
   
    return cell_crops


def img_reader(cell_crops:list[MatLike]):
    reader = easyocr.Reader(["en"], gpu=False)
    
    all_text = []
    for cropped_img in cell_crops:
        results = reader.readtext(cropped_img, mag_ratio=3, detail=0)
        all_text.append(" ".join(results))

    rows = []
    for i in range(0, len(all_text), 2):
        row = all_text[i : i + 2]
        while len(row) < 2:
            row.append("")
        rows.append(row)

    df = pd.DataFrame(rows, columns=["Title", "Artist"])
    df = df.replace(replacements, regex=True)
    return df