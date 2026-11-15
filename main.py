import cv2
import easyocr  # noqa: F401
import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401
import pyautogui  # noqa: F401
from PIL import Image  # noqa: F401

import autoScreenshot as AS
import imgReader as IR


def main():
    url = "https://open.spotify.com/playlist/54EvyvoDP1AZBgfgh5bVP1"
    """
    img = cv2.imread("temp/TestImg.png")
    results = IR.process_img(img)  # type: ignore
    print(IR.img_reader(results))
    """

    "AS.screenshot()"
    AutoSS = AS.AutoScreenshotter(url=url)
    AutoSS.open_web(True)


if __name__ == "__main__":
    main()
