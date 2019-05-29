from tkinter import *
from tkinter.filedialog import askopenfilename
import textsum
import ocr
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
stop_words = set(stopwords.words('english'))

path = "None"
def openfile():
    global text
    global path
    openlocation = askopenfilename(initialdir= "/home/aman/")
    file = open(openlocation, 'r+')
    path = file.name
    t = file.read()
    text.delete(0.0, END)
    text.insert(0.0, t)
    file.close()

def opendoc1():
    global doc1
    openlocation = askopenfilename(initialdir= "/home/aman/")
    file = open(openlocation, 'r+')
    t = file.read()
    doc1.delete(0.0, END)
    doc1.insert(0.0, t)
    file.close()

def opendoc2():
    global doc2
    openlocation = askopenfilename(initialdir= "/home/aman/")
    file = open(openlocation, 'r+')
    t = file.read()
    doc2.delete(0.0, END)
    doc2.insert(0.0, t)
    file.close()

def summarize():
    summ = textsum.generate_summary(path, 5)
    text.delete(0.0, END)
    text.insert(0.0, summ)

def read():
    global text
    global path
    openlocation = askopenfilename(initialdir= "/home/aman/")
    path = openlocation
    if ".pdf" in path.split("/")[-1]:
        Text = ocr.pdftostring(path)
        text.delete(0.0, END)
        text.insert(0.0, Text)
    else:
        Text = ocr.imagetostring(path)
        text.delete(0.0, END)
        text.insert(0.0, Text)

def wordCloud():
    global text
    global path
    name = path.split("/")[-1]
    txt = text.get("1.0", "end-1c")
    txt = str(txt)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords).generate(txt)
    fn = name.split(".")[0] + ".png"
    wordcloud.to_file(fn)      
    i = "/home/aman/Work/WORK/Work/BlackBox/" + fn
    img = Image.open(i)
    img.show()

def nlp_preprocessing(document):
    if type(document) is not int:
        string = ""
        punc = [".", "?", ",", "!", "/", "-", ":", ";", "(", ")", "_"]
        for item in punc:
            document = document.split(item)
            document = " ".join(document)
        for words in document.split():
            # remove the special chars in review like '"#$@!%^&*()_+-~?>< etc.
            word = ("".join(e for e in words if e.isalnum()))
            # Conver all letters to lower-case
            word = word.lower()
            # stop-word removal
            if not word in stop_words:
                string += word + " "
        return string

def compare():
    d1 = str(doc1.get("1.0", "end-1c"))
    d2 = str(doc2.get("1.0", "end-1c"))
    d1 = nlp_preprocessing(d1)
    d2 = nlp_preprocessing(d2)
    arr = []
    arr.append(d1)
    arr.append(d2)
    tfidf_doc_vectorizer = TfidfVectorizer(min_df = 0)
    tfidf_doc_features = tfidf_doc_vectorizer.fit_transform(arr)
    cos = cosine_similarity(tfidf_doc_features[0], tfidf_doc_features[1])
    cos_per = abs(cos[0][0])*100
    message = "The similarity between Document 1. and Document 2. is: " + str("%.2f" % cos_per) + "%"
    text.delete('1.0', END)
    text.insert(0.0, message)
    
def reset():
    text.delete('1.0', END)
    doc1.delete('1.0', END)
    doc2.delete('1.0', END)

root = Tk()
root.title("NLP Black Box")
root.minsize(width=500, height=500)
root.configure()

text = Text(root, height= 15, bg= "gray", font = ("Times", 15))
text.grid(row= 0, rowspan= 5, padx= 5, pady= 5)

doc1 = Text(root, height= 10, bg= "gray", font = ("Times", 15))
doc1.grid(row= 5, rowspan= 2, padx= 5, pady= 5)

doc2 = Text(root, height= 10, bg= "gray", font = ("Times", 15))
doc2.grid(row= 7, rowspan= 2, padx= 5, pady= 5)

scrollbar1 = Scrollbar(root)
scrollbar1.grid(row= 1, column= 1, rowspan= 2, pady= 5)
scrollbar1.config(command = text.yview)

scrollbar2 = Scrollbar(root)
scrollbar2.grid(row= 5, column= 1, rowspan= 2, pady= 5)
scrollbar2.config(command = doc1.yview)

scrollbar3 = Scrollbar(root)
scrollbar3.grid(row= 7, column= 1, rowspan= 2, pady= 5)
scrollbar3.config(command = doc1.yview)

b1= Button(root, width= 9, text = "Open", command= openfile)
b2= Button(root, width= 9, text = "Summarize", command= summarize)
b3= Button(root, width= 9, text = "PdfToText", command= read)
b4= Button(root, width= 9, text = "ImgToText", command= read)
b5= Button(root, width= 9, text = "WordCloud", command= wordCloud)
b6= Button(root, width= 9, text = "Doc1", command= opendoc1)
b7= Button(root, width= 9, text = "Doc2", command= opendoc2)
b8= Button(root, width= 9, text = "Compare", command= compare)
b9= Button(root, width= 9, text = "Reset", command= reset)

b1.grid(row= 0, column= 2, columnspan= 2, padx= 3, pady= 3)
b2.grid(row= 1, column= 2, columnspan= 2, padx= 3, pady= 3)
b3.grid(row= 2, column= 2, columnspan= 2, padx= 3, pady= 3)
b4.grid(row= 3, column= 2, columnspan= 2, padx= 3, pady= 3)
b5.grid(row= 4, column= 2, columnspan= 2, padx= 3, pady= 3)
b6.grid(row= 5, column= 2, columnspan= 2, padx= 3, pady= 3)
b7.grid(row= 6, column= 2, columnspan= 2, padx= 3, pady= 3)
b8.grid(row= 7, column= 2, columnspan= 2, padx= 3, pady= 3)
b9.grid(row= 8, column= 2, columnspan= 2, padx= 3, pady= 3)

root.mainloop()