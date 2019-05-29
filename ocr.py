from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import warnings
warnings.filterwarnings("ignore")

def pdftostring(path):
    arr = []
    pages = convert_from_path(path, 500)
    for i in range(len(pages)):
        pages[i].save('output.jpg', 'JPEG')
        try:
            text = pytesseract.image_to_string(Image.open('output.jpg'))
            arr.append(text)
        except:
            pass
    Text = ". ".join(arr)
    return Text

def imagetostring(path):
    text = pytesseract.image_to_string(Image.open(path))
    return text