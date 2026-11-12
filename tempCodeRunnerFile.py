import cv2
import easyocr  # noqa: F401
import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401
import pyautogui  # noqa: F401
from PIL import Image  # noqa: F401

import imgReader as IR


def main():
    img = cv2.imread("temp/TestImg.png")
    results = IR.process_img(img)
    print(IR.img_reader(results))


if __name__ == "__main__":
    main()
