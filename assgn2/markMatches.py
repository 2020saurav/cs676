import sys
import struct
import cv2
import random

imgName1 = sys.argv[1]
imgName2 = sys.argv[2]
# imgName1 = 'img1.png'
# imgName2 = 'img3.png'
fileName = 'Match_' + imgName1 + imgName2 + '.match'

f = open(fileName, 'r')

img1 = cv2.imread(imgName1)
img2 = cv2.imread(imgName2)

def drawCircle(img, x, y, color, thick):
    cv2.circle(img, (y,x), 5, color, thick)


def randomColor():
    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)
    return (b, g, r)


def randomThick():
    return random.randint(2, 2)
i=0
for line in f.readlines():
     i+=1
     #if (i%10==1):
     (x1, y1, x2, y2) = map(lambda x : int(float(x)), line.strip().split('  '))
     print (x1, y1, x2, y2)
     color = randomColor()
     thick = randomThick()
     drawCircle(img1, x1, y1, color, thick)
     drawCircle(img2, x2, y2, color, thick)


cv2.imwrite('Match1_' + imgName1 + imgName2, img1)
cv2.imwrite('Match2_' + imgName1 + imgName2, img2)
