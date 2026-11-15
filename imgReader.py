import cv2
import easyocr
import pandas as pd
import numpy as np


class ImageReader:
    def __init__(self):
        self.counter = 0
        self.replacements = {
            "_": " ",
            ";": ",",
            ":": ",",
            "  ": " ",
            ",": "",
        }
        self.cell_crops = []
        self.reader = easyocr.Reader(["en"], gpu=False)

    def process_img(self, img: np.ndarray):

        # commenting out unused code (self.counter += 1)

        if img is None:
            raise ValueError("Image failed to load in imgReader.py")

        clean_img = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 11))
        dialate = cv2.dilate(thresh, kernal, iterations=1)

        cnts = cv2.findContours(dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        boxes = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if w < 25:
                continue
            boxes.append((x, y, w, h))

        boxes = sorted(boxes, key=lambda b: (b[1] // 15, b[0]))

        for x, y, w, h in boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
            crop = clean_img[y : y + h, x : x + w]
            self.cell_crops.append(crop)

        #  commenting out unused code [ cv2.imwrite(f"temp/index_bbox{self.counter}.png", img) ]

    def img_reader(self):

        all_text = []
        for cropped_img in self.cell_crops:
            results = self.reader.readtext(
                cropped_img, mag_ratio=3, detail=0, paragraph=True
            )
            all_text.append(" ".join(results))  # type: ignore

        self.cell_crops.clear()
        rows = []
        for i in range(0, len(all_text), 2):
            row = all_text[i : i + 2]
            while len(row) < 2:
                row.append("")
            rows.append(row)

        df = pd.DataFrame(rows, columns=["Title", "Artist"])
        df = df.replace(self.replacements, regex=True)
        return df
