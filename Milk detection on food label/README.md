# Milk Detection on food label

This project is a part of EGBI 443 Image Processing in medicine, Department of Biomedical Engineering, Mahidol university.
The aim is to detect the Thai and English word "milk" and "นม" on food labels.

The dataset for this project can be accessed from the google drive link in .txt file.

You can see some examples of output images in the "output" folder.

## Pytesseract

This project was build based on [Pytesseract](https://github.com/UB-Mannheim/tesseract/wiki).
Note that the default installation path is: "C:\Users\USER\AppData\Local\Tesseract-OCR".

```sh
pip install pytesseract
```

Please set the tesseract path in the script before calling `image_to_string`

```sh
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
```
