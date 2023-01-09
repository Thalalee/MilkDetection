import pytesseract
import cv2
import matplotlib.pylab as plt
import re
import numpy as np
from scipy import ndimage
from statistics import mode
import sys

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# read non-rotated img
img_nr = cv2.imread('snack64.jpg')
img_nr = cv2.cvtColor(img_nr, cv2.COLOR_RGB2BGR)

# -------------------------------- Rotate image ---------------------------------------

# change image to grayscale
gray_ori = cv2.cvtColor(img_nr, cv2.COLOR_BGR2GRAY)

# Apply canny
canimg = cv2.Canny(gray_ori, 60, 200)

# Apply Hough
lines = cv2.HoughLines(canimg, 1, np.pi/180.0, 250, np.array([]))

# rotate image
if np.all(lines != None):
    deg = []
    # convert radian to degree
    for line in lines:
        theta = line[0,1]
        deg.append(180*theta/np.pi - 90)
    # Find the angle that are detected most frequently
    deg_mode = mode(deg)

    # rotate the image according to the tilted angle
    if deg_mode >= 20 and deg_mode <= 50:
        img = ndimage.rotate(img_nr, mode(deg) - 45)
    elif deg_mode <= -20 and deg_mode >= -50:
        img = ndimage.rotate(img_nr, mode(deg) - 45 + 90)
    elif deg_mode < -50 and deg_mode >= -90:
        img = ndimage.rotate(img_nr, mode(deg) + 90)
    elif deg_mode > 50 and deg_mode <= 90:
        img = ndimage.rotate(img_nr, mode(deg) - 90)
    else:
        img = ndimage.rotate(img_nr, mode(deg))

# -------------------------------- Develop image ----------------------------------------

# convert rotated image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# dev image
threshadap = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 9)

# opening
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
opening = cv2.morphologyEx(threshadap, cv2.MORPH_OPEN, kernel)

# closing
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
dev = closing

#--------------------------------- Detect English ------------------------------------

new_img = img.copy()
p1 = p2 = p3 = p4 = 0

# Extract the English word
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
detectmilk = 'milk'
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
# Delete unnecessary string
for i, word in enumerate(data["text"]):
    data["text"][i] = re.sub(',|:', '', word)
# Detect 'milk' from string
wordrecog_en = [ i for i, text in enumerate(data["text"]) if text.lower() == detectmilk]

# Try enhaced image if raw image does not work
if wordrecog_en == 0:
    detectmilk = 'milk'
    data = pytesseract.image_to_data(dev, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data["text"]):
        data["text"][i] = re.sub(',|:', '', word)
    wordrecog_en = [ i for i, word in enumerate(data["text"]) if word.lower() == detectmilk]

# Draw box around detected word
for word in wordrecog_en:
    # get top, left position and width, height of extracted word
    w = data["width"][word]
    h = data["height"][word]
    l = data["left"][word]
    t = data["top"][word]
    # define 4 coordinates of box
    x1 = (l, t)
    x2 = (w + l, t)
    x3 = (w + l, t + h)
    x4 = (l, h + t)
    # draw 4 lines to create the box
    new_img = cv2.line(new_img, x1, x2, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x2, x3, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x3, x4, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x4, x1, color=(255, 0, 0), thickness=5)

# Draw X on top of the image if milk is detected
if len(wordrecog_en) != 0:
    h, w, c = img.shape
    new_img = cv2.line(new_img, (0,0), (w,h), color=(255, 0, 0), thickness=20)
    new_img = cv2.line(new_img, (0,h), (w,0), color=(255, 0, 0), thickness=20)
    # If 'milk' is already found, there is no need to detect 'นม'. The program stops here.
    plt.imsave("detectedmilk.jpg", new_img)
    fig = plt.figure("Milk Detection")
    plt.subplot(1,2,1), plt.imshow(img_nr), plt.title('Original'), plt.axis('off')
    plt.subplot(1,2,2), plt.imshow(new_img), plt.title('Output'), plt.axis('off')
    plt.show()
    print("already found milk, stop here")
    sys.exit(0)

# ---------------------------------- Detect Thai --------------------------------------

# reuse parameters
x1 = x2 = x3 = x4 = 0
h, w = gray.shape

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Extract Thai string
data_th = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang="tha")
# detect both 'น' that follows by 'ม' and 'นม'
wordrecog_m = [ i for i, text in enumerate(data_th['text']) if text == 'น']
wordrecog_k = [ i for i, text in enumerate(data_th['text']) if text == 'ม']
wordrecog_th = []
wordrecog_th = [ i for i, text in enumerate(data_th['text']) if text == 'นม']
for i,m in enumerate(wordrecog_m):
    for j,k in enumerate(wordrecog_k):
        if k-m == 1:
            wordrecog_th.append(m)

# try enhaced image if real image does not work
if wordrecog_th == 0:
    data_th = pytesseract.image_to_data(dev, output_type=pytesseract.Output.DICT, lang="tha")
    wordrecog_m = [ i for i, text in enumerate(data_th['text']) if text == 'น']
    wordrecog_k = [ i for i, text in enumerate(data_th['text']) if text == 'ม']
    wordrecog_th = []
    wordrecog_th = [ i for i, text in enumerate(data_th['text']) if text == 'นม']
    for i,m in enumerate(wordrecog_m):
        for j,k in enumerate(wordrecog_k):
            if k-m == 1:
                wordrecog_th.append(m)

# Draw X if the snack contains milk
if len(wordrecog_th) + len(wordrecog_en) != 0:
    new_img = cv2.line(new_img, (0,0), (w,h), color=(255, 0, 0), thickness=20)
    new_img = cv2.line(new_img, (0,h), (w,0), color=(255, 0, 0), thickness=20)
# Draw ✓ if the snack does not contain milk
else:
    new_img = cv2.line(new_img, (0,np.int(h*3/4)), (np.int(w/6),h), color=(0, 255, 0), thickness=20)
    new_img = cv2.line(new_img, (np.int(w/6),h), (w,0), color=(0, 255, 0), thickness=20)

# Draw box around detected word
for word in wordrecog_th:
    # get top, left position and width, height of extracted word
    w = data_th["width"][word] + data_th["width"][word+1]
    h = data_th["height"][word]
    l = data_th["left"][word]
    t = data_th["top"][word]
    # define 4 coordinates of the box
    x1 = (l, t)
    x2 = (w + l, t)
    x3 = (w + l, t + h)
    x4 = (l, h + t)
    # draw 4 lines to create the box
    new_img = cv2.line(new_img, x1, x2, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x2, x3, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x3, x4, color=(255, 0, 0), thickness=5)
    new_img = cv2.line(new_img, x4, x1, color=(255, 0, 0), thickness=5)

plt.imsave("detectedmilk.jpg", new_img)

# ------------------------------- Show image ---------------------------------------

fig = plt.figure("Milk Detection")
plt.subplot(1,2,1), plt.imshow(img_nr), plt.title('Original'), plt.axis('off')
plt.subplot(1,2,2), plt.imshow(new_img), plt.title('Output'), plt.axis('off')
plt.show()