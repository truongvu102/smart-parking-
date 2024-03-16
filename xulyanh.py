import numpy as np
import cv2
import imutils
import pytesseract
import csv
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


running = True

while running:
    cap = cv2.VideoCapture(0)
    while True:
      ret, frame = cap.read()
      cv2.imshow('Camera', frame)
      if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('anhxe.jpg', frame)
        break

    image = cv2.imread('anhxe.jpg')

    image = imutils.resize(image, width=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    edged = cv2.Canny(gray, 170, 200)
  
    cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
 

    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCnt = None 

    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0,255,0), 3)

    count = 0
    idx =7
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:  
            NumberPlateCnt = approx 
        x, y, w, h = cv2.boundingRect(c)
        new_img = gray[y:y + h, x:x + w]
        cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img)
        idx+=1

        break
    cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
    cv2.imshow("Final Image With Number Plate Detected", image)
    Cropped_img_loc = 'Cropped Images-Text/7.png'
    cv2.imshow("Cropped Image ", cv2.imread(Cropped_img_loc))
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng', config='--psm 11')

    print("Biển số xe :", text)


    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    data = [text ,current_time]


    with open('license_plates.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data])

    cv2.waitKey(0)

   
    cap.release()
    cv2.destroyAllWindows()
running = False
                             