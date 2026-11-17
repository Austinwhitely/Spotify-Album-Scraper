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
    initial_offset = 350
    AutoSS = AS.AutoScreenshotter(initial_scroll_amount=initial_offset, url=url)
    IMAGE_READER = IR.ImageReader()

    img = cv2.imread(r"temp\screenshot_1.png")
    IMAGE_READER.process_img(img)
    print(IMAGE_READER.img_reader())

    "AS.screenshot()"


# AutoSS.open_web(True)


if __name__ == "__main__":
    main()
