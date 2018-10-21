import cv2
from pyfirmata import Arduino, util, serial
import time

board = serial.Serial('/dev/cu.usbmodem145301', 9600)

videoCapture = cv2.VideoCapture(0)

cascadeClassifierFaces = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cascadeClassifierSmiles = cv2.CascadeClassifier("haarcascade_smile.xml")

initialFrames = 0
sendCommandPermission = False
maxFrames = 5
smileDetected = False
output = 0

while(True):

  ret, frame = videoCapture.read()

  if initialFrames < maxFrames:
      initialFrames += 1
      sendCommandPermission = False
  else:
      initialFrames = 0
      sendCommandPermission = True

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  detectFacesResults = cascadeClassifierFaces.detectMultiScale(
   gray,
   scaleFactor=1.3,
   minNeighbors=5,
   minSize=(50, 50),
   flags = cv2.CASCADE_SCALE_IMAGE
  )

  for (x, y, w, h) in detectFacesResults:

    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    print(x)
    output = 125 - ((float(125 - 0) / float(1100 - 5))) * (x - 5)
    #output = (2500 + ((float(-5800) / float(780))) * (x - 10))

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]

    detectSmileResults = cascadeClassifierSmiles.detectMultiScale(
      roi_gray,
      scaleFactor= 1.8,
      minNeighbors=10,
      minSize=(15, 15),
      flags = cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in detectSmileResults:
      for x in range(1):

          if sendCommandPermission:
              print('Send smile')
              board.write(str(242) + '/n')
              board.flush()

      cv2.rectangle(roi_color, (x, y), (x+w, y+h), (0, 0, 255), 1)#
      smileDetected = True
      break

    if sendCommandPermission and not(smileDetected):
        print('Send face')
        board.write(str(output) + '/n')
        board.flush()

  smileDetected = False

  cv2.imshow('frame', frame)

  if 0xFF & cv2.waitKey(1) == 27:
    break

videoCapture.release()
cv2.destroyAllWindows()
