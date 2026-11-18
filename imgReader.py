import cv2
import easyocr
import numpy as np
import pandas as pd


class ImageReader:
    def __init__(self):
        self.counter = 0
        self.replacements = {
            "_": " ",
            ";": ",",
            ":": ",",
            ",": "",
            r"\b[Ff]eat\.?\b": "",
            r"\b[Ff]t\.?\b": "",
            r"\s+": " ",
        }
        self.cell_crops = []
        self.reader = easyocr.Reader(["en"], gpu=False)

    def process_img(self, img):

        if img is None:
            raise ValueError("Image failed to load in imgReader.py")

        clean_img = img.copy()
        img_h, img_w = img.shape[:2]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        blur = cv2.GaussianBlur(enhanced, (3, 3), 0)
        cv2.imwrite(f"temp/index_blur{self.counter}.png", blur)

        otsu_val, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        adjusted_thresh = max(15, otsu_val - 22)
        thresh = cv2.threshold(blur, adjusted_thresh, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite(f"temp/index_thresh{self.counter}.png", thresh)

        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 12))
        dialate = cv2.dilate(thresh, kernal, iterations=1)
        cv2.imwrite(f"temp/index_dialate{self.counter}.png", dialate)

        cnts = cv2.findContours(dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        boxes = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if w < 20:
                continue
            boxes.append((x, y, w, h))

        boxes = sorted(boxes, key=lambda b: (b[1] // 15, b[0]))

        pad = 4
        scale_factor = 3
        for x, y, w, h in boxes:
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img_w, x + w + pad)
            y2 = min(img_h, y + h + pad)

            cv2.rectangle(img, (x1, y1), (x2, y2), (36, 255, 12), 2)
            crop = clean_img[y1:y2, x1:x2]
            crop = cv2.bitwise_not(crop)
            crop = cv2.resize(
                crop,
                None,
                fx=scale_factor,
                fy=scale_factor,
                interpolation=cv2.INTER_LANCZOS4,
            )
            self.cell_crops.append(crop)

        cv2.imwrite(f"temp/index_bbox{self.counter}.png", img)

    def img_reader(self):

        all_text = []
        for cropped_img in self.cell_crops:
            results = self.reader.readtext(
                cropped_img,
                mag_ratio=3,
                detail=0,
                low_text=0.3,
                text_threshold=0.5,
                adjust_contrast=0.7,
                paragraph=True,
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
