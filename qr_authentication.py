import cv2
import numpy as np
from pyzbar.pyzbar import decode

# NOTE: use '0' as a parameter in cv2.VideoCapture method while using device's webcam ->
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1)

# reading the txt file for authentication of persons:
with open('Resources/name_list.txt') as file:
    myDataList = file.read().splitlines()

while True:
    _, img = cap.read()
    # decoding QR code from image and returning its data
    for barcode in decode(img):
        # print(barcode.data)
        myData = barcode.data.decode('utf-8')
        print(f"NAME OF PERSON : {myData}")

        if myData in myDataList:
            outputText = "Authorized"
            outputColor = (0, 255, 0)
        else:
            outputText = "Un-Authorized"
            outputColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, outputColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, outputText, (pts2[0] - 5, pts2[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 0.9, outputColor, 2)

    # showing the webcam for output
    cv2.imshow("qr_code_scanner", img)
    if cv2.waitKey(1) == 27:
        break
