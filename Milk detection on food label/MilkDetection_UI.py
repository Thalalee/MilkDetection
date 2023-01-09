from PyQt5 import QtCore, QtGui, QtWidgets
import os , re , cv2 , pytesseract
from PyQt5.QtGui import  QIcon , QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import matplotlib.pylab as plt
from PIL import Image, ImageFont, ImageDraw 
from itertools import chain
from scipy import ndimage
import statistics
from statistics import mode
import sys

class Ui_MainWindow(object):
        def __init__(self):
                pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1200, 800)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("UI/869664.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                MainWindow.setWindowIcon(icon)
                MainWindow.setStyleSheet("background-color: rgb(252, 249, 204);")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.title = QtWidgets.QLabel(self.centralwidget)
                self.title.setGeometry(QtCore.QRect(480, 30, 241, 51))
                font = QtGui.QFont()
                font.setFamily("Agency FB")
                font.setPointSize(20)
                font.setBold(True)
                font.setItalic(False)
                font.setWeight(75)
                font.setStyleStrategy(QtGui.QFont.PreferDefault)
                self.title.setFont(font)
                self.title.setAutoFillBackground(False)
                self.title.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.title.setFrameShadow(QtWidgets.QFrame.Plain)
                self.title.setAlignment(QtCore.Qt.AlignCenter)
                self.title.setWordWrap(False)
                self.title.setObjectName("title")
                self.importimgshow = QtWidgets.QLabel(self.centralwidget)
                self.importimgshow.setGeometry(QtCore.QRect(60, 180, 500, 500))
                self.importimgshow.setFrameShape(QtWidgets.QFrame.WinPanel)
                self.importimgshow.setText("")
                self.importimgshow.setAlignment(QtCore.Qt.AlignCenter)
                self.importimgshow.setObjectName("importimgshow")
                self.detectbttn = QtWidgets.QPushButton(self.centralwidget)
                self.detectbttn.setGeometry(QtCore.QRect(750, 110, 201, 51))
                font = QtGui.QFont()
                font.setFamily("Franklin Gothic Demi Cond")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.detectbttn.setFont(font)
                self.detectbttn.setAutoFillBackground(False)
                self.detectbttn.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(145, 218, 0);")
                self.detectbttn.setAutoDefault(False)
                self.detectbttn.setObjectName("detectbttn")
                self.detectimgshow = QtWidgets.QLabel(self.centralwidget)
                self.detectimgshow.setGeometry(QtCore.QRect(600, 180, 500, 500))
                self.detectimgshow.setFrameShape(QtWidgets.QFrame.WinPanel)
                self.detectimgshow.setText("")
                self.detectimgshow.setAlignment(QtCore.Qt.AlignCenter)
                self.detectimgshow.setObjectName("detectimgshow")
                self.exitbttn = QtWidgets.QPushButton(self.centralwidget)
                self.exitbttn.setGeometry(QtCore.QRect(920, 700, 141, 31))
                font = QtGui.QFont()
                font.setFamily("Franklin Gothic Demi Cond")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.exitbttn.setFont(font)
                self.exitbttn.setAutoFillBackground(False)
                self.exitbttn.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(145, 218, 0);")
                self.exitbttn.setAutoDefault(False)
                self.exitbttn.setObjectName("exitbttn")
                self.clearbttn = QtWidgets.QPushButton(self.centralwidget)
                self.clearbttn.setGeometry(QtCore.QRect(750, 700, 141, 31))
                font = QtGui.QFont()
                font.setFamily("Franklin Gothic Demi Cond")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.clearbttn.setFont(font)
                self.clearbttn.setAutoFillBackground(False)
                self.clearbttn.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(145, 218, 0);")
                self.clearbttn.setAutoDefault(False)
                self.clearbttn.setObjectName("clearbttn")
                self.Importbttn = QtWidgets.QPushButton(self.centralwidget)
                self.Importbttn.setGeometry(QtCore.QRect(210, 110, 201, 51))
                font = QtGui.QFont()
                font.setFamily("Franklin Gothic Demi Cond")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.Importbttn.setFont(font)
                self.Importbttn.setAutoFillBackground(False)
                self.Importbttn.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(145, 218, 0);")
                self.Importbttn.setAutoDefault(False)
                self.Importbttn.setObjectName("Importbttn")
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.Importbttn.clicked.connect(self.browseImage)
                self.detectbttn.clicked.connect(self.detectmilk)
                self.detectbttn.setEnabled(False)
                self.clearbttn.clicked.connect(self.clearimage)
                self.exitbttn.clicked.connect(MainWindow.close) # type: ignore
                
                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Milk Detector"))
                self.title.setText(_translate("MainWindow", "MILK DETECTOR"))
                self.detectbttn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Click to detect &quot;MILK&quot; or &quot;นม&quot; in food label</p></body></html>"))
                self.detectbttn.setText(_translate("MainWindow", "Detect Milk"))
                self.exitbttn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Click to exit the application</p></body></html>"))
                self.exitbttn.setText(_translate("MainWindow", "Exit"))
                self.clearbttn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Click to clear output image</p></body></html>"))
                self.clearbttn.setText(_translate("MainWindow", "Clear"))
                self.Importbttn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Click to import food label</p></body></html>"))
                self.Importbttn.setText(_translate("MainWindow", "Import Image"))

        def browseImage(self):
                options = QtWidgets.QFileDialog.Options()
                options |= QtWidgets.QFileDialog.DontUseNativeDialog
                self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(options=options)
                if self.fileName:
                        pattern = ".(jpg|png|jpeg|bmp|jpe|tiff)$"
                        if re.search(pattern,self.fileName):
                                self.putImageinspace(self.fileName)

        def putImageinspace(self,fileName):
                self.importimgshow.setPixmap(QPixmap(fileName))
                self.detectbttn.setEnabled(True)
        
        def detectmilk(self):
                # read non-rotated img
                img_nr = cv2.imread(self.fileName)
                img_nr = cv2.cvtColor(img_nr, cv2.COLOR_RGB2BGR)

                # ----------- Rotate image ---------------

                # change image to grayscale
                gray_ori = cv2.cvtColor(img_nr, cv2.COLOR_BGR2GRAY)
                # Apply canny
                canimg = cv2.Canny(gray_ori, 60, 200)
                # Apply Hough
                lines = cv2.HoughLines(canimg, 1, np.pi/180.0, 250, np.array([]))
                # rotate image
                if np.all(lines != None):
                        deg = []
                        for line in lines:
                                theta = line[0,1]
                                deg.append(180*theta/np.pi - 90)

                        deg_mode = mode(deg)
                        # rotation angle in degree
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

                # ------------- Develop image -------------
                
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

                #-------------- Detect English --------------
                new_img = img.copy()
                p1 = p2 = p3 = p4 = 0

                pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                
                # Extract the English word
                detectmilk = 'milk'
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                for i, word in enumerate(data["text"]):
                        data["text"][i] = re.sub(',|:', '', word)
                wordrecog_en = [ i for i, text in enumerate(data["text"]) if text.lower() == detectmilk]

                # try enhaced image it real image does not work
                if wordrecog_en == 0:
                        detectmilk = 'milk'
                        data = pytesseract.image_to_data(dev, output_type=pytesseract.Output.DICT)
                        for i, word in enumerate(data["text"]):
                                data["text"][i] = re.sub(',|:', '', word)
                        wordrecog_en = [ i for i, text in enumerate(data["text"]) if text.lower() == detectmilk]

                for word in wordrecog_en:
                        # get top, left position and width, height of extracted word
                        w = data["width"][word]
                        h = data["height"][word]
                        l = data["left"][word]
                        t = data["top"][word]
                        # define 4 coordinates of box
                        x1 = (l, t)
                        x2 = (w + l, t)
                        x3 = (w + l, h + t)
                        x4 = (l, h + t)
                        # draw 4 lines to create the box
                        new_img = cv2.line(new_img, x1, x2, color=(255, 0, 0), thickness=5)
                        new_img = cv2.line(new_img, x2, x3, color=(255, 0, 0), thickness=5)
                        new_img = cv2.line(new_img, x3, x4, color=(255, 0, 0), thickness=5)
                        new_img = cv2.line(new_img, x4, x1, color=(255, 0, 0), thickness=5)
                
                # ----------- Detect Thai --------------

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
                #save output image as detectedmilk.jpg
                plt.imsave("detectedmilk.jpg", new_img)

                #Show the saved output image
                pixmap = QPixmap('detectedmilk.jpg')
                self.detectimgshow.setPixmap(pixmap)
                self.detectbttn.setEnabled(True)

                #Create window to show output in text whether it contains milk or not
                messagebox = QMessageBox()
                #if it has milk as an ingredient, show "CONTAIN MILK"
                if len(wordrecog_th) + len(wordrecog_en) != 0:
                        messagebox.setText("CONTAIN MILK")
                #if it not has milk as an ingredient, show "NOT CONTAIN MILK"
                else:
                        messagebox.setText("NOT CONTAIN MILK")
                messagebox.setWindowTitle("SHOW OUTPUT")
                messagebox.setStandardButtons(QMessageBox.Close)
                x = messagebox.exec_()

        def clearimage(self):
                self.detectimgshow.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
