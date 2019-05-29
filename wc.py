from wordcloud import WordCloud, STOPWORDS

txt = "Many times you might have seen a cloud filled with lots of words in different sizes, which represent the frequency or the importance of each word. This is called Tag Cloud or WordCloud. For this tutorial, you will learn how to create a WordCloud of your own in Python and customize it as you see fit. This tool will be quite handy for exploring text data and making your report more lively."
print(txt)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords).generate(txt)
wordcloud.to_file("2.png")