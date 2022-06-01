
import cv2
import numpy as np
import pytesseract
import pyautogui
import time
from PIL import Image
import webbrowser
pytesseract.pytesseract.tesseract_cmd = 'E:/tesseract/tesseract.exe'



#going to the website

webbrowser.open("https://monkeytype.com")
time.sleep(8)#give more or less time depending on your internet and browser speed :)
im = pyautogui.screenshot("monke.jpg")


#cropping the screenshot taken and saving it

img = Image.open("monke.jpg")
x1,x2,y1,y2 = 375,449,1530,612
cropim = img.crop((x1,x2,y1,y2))
cropim.save("monkeyc.jpg")



#reading and applying thresholding
#compensating for yellow cursor that may appear

image = cv2.imread("monkeyc.jpg")


hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
lower_yel = np.array([22, 93, 0])
upper_yel = np.array([45, 255, 255])

mask=cv2.inRange(hsv,lower_yel,upper_yel)
image[mask>0]=(0,0,0)
cv2.imwrite("result.jpg",image)
img = cv2.imread("result.jpg")



gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


im2 = img.copy()


file = open("typemonke.txt", "w+")
file.write("")
file.close()

for cnt in contours:
	x, y, w, h = cv2.boundingRect(cnt)
	
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	cropped = im2[y:y + h, x:x + w]
	
	file = open("typemonke.txt", "a")
	
	text = pytesseract.image_to_string(cropped)
	
	file.write(text)
	file.write("\n")
	file.close()
 
# cv2.imshow('Truncated Threshold',thresh1)
# cv2.waitKey()

with open("typemonke.txt", "r+") as file:
    file.seek(0)
    line = file.readlines()
L = []
for i in line:
        i = i[:-1:]
        i += " "
        if i != " ":
            L.append(i)

n = len(L)
a = ""
for i in range(len(L)):
    a += L[i]

file.close()
time.sleep(2)
for letter in a:
    pyautogui.press(letter)
