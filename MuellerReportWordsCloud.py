# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:14:43 2019

@author: Peng Wang

Create word clouds for Mueller Report
https://cdn.cnn.com/cnn/2019/images/04/18/mueller-report-searchable.pdf
"""

import re
from nltk.corpus import stopwords
from collections import Counter 
import numpy as np
import PyPDF2
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

additional_stop_words = ['president','said','told','too','also','could','would','may']
# White House http://www.pngmart.com/files/4/White-House-PNG-File.png
mask_image_filename = r"the-white-house.png" 
saved_image_filename = r'wordcloud.png'
muller_report_filename = r'mueller-report-searchable.pdf'

# Convert image pixel value 0 to 255 
def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

# Load background image to create a mask for the word cloud     
def load_image_mask():
    # Load background image
    mask = np.array(Image.open(mask_image_filename))
    # Convert 3D numpy to 2D 
    # https://stackoverflow.com/questions/37500804/convert-3d-numpy-array-to-2d
    mask = mask.reshape((mask.shape[0],-1), order='F')
    mask_2d = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)    
    for i in range(len(mask)):
        mask_2d[i] = list(map(transform_format, mask[i]))
    
    return mask_2d

# Clean up text
def text_cleanup(text):     
    # Remove non-alphabet
    text = re.sub("[^a-zA-Z]"," ", text)
    # Remove single letter word
    text = re.sub(r"\b\w{1,1}\b","", text)
    # Convert to lowercase
    text = text.lower().split()
    # Filter out stop words in English 
    stops = set(stopwords.words("english")).union(additional_stop_words) 
    text = [w for w in text if not w in stops]
    text = list(set(text))
    return text

# Create word cloud image
def wordcloud(text):
    # Load background image as a mask
    mask = load_image_mask()
    # Plot word cloud
    wordcloud = WordCloud(background_color="white", max_words=500, mask=mask, 
                          random_state=12, scale=.5, margin=5, collocations = False,
                          contour_width=3, contour_color='firebrick')
    wordcloud.generate(" ".join([i for i in text]))
    plt.figure(figsize=(16,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()   
    # Save the word cloud image
    wordcloud.to_file(saved_image_filename)      
    
# creating a pdf reader object
report_reader = PyPDF2.PdfFileReader(open(muller_report_filename, 'rb'))
# Read in each page in PDF
report_content = [report_reader.getPage(x).extractText() for x in range(report_reader.numPages)]
# Clean up all pages in the report
report_cleaned = []
for page in report_content:
    report_cleaned = report_cleaned + text_cleanup(page)
# Show the top 20 most appeared word in the report
Counter(report_cleaned).most_common(20)
# Plot word cloud      
wordcloud(report_cleaned)
