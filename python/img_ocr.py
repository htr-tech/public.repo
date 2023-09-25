import cv2
import sys
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

def detect_text(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data_obj = pytesseract.image_to_data(img, config=tessdata_dir_config)

    text_detected = False
    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:
                text_detected = True
                break

    if not text_detected:
        data_obj = pytesseract.image_to_data(img, config=tessdata_dir_config + ' --psm 10')
    
    output = ""
    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:
                txt = data[11]
                output += txt + ' '
                # x, y, w, h = int(data[6]), int(data[7]), int(data[8]), int(data[9])
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.putText(img, txt, (x-9,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # cv2.imshow("popup", img)
    # cv2.waitKey(0)
    return output

print(detect_text('luck.png'))