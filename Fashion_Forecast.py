from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.firefox import GeckoDriverManager
from skimage import measure
import cv2 as p
from cv2 import cv2
import sys
import operator
import argparse
import math
import urllib
from skimage import io
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from skimage import measure
import skimage.metrics 

import imutils
from matplotlib import cm
import csv
from collections import OrderedDict
# from selenium.webdriver.firefox.options import Options 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
c=2
options = Options()
options.add_argument('-headless')
parser=argparse.ArgumentParser()
parser.add_argument('-k',help='keyword', dest='key')

args=parser.parse_args()
key=args.key
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
wait = WebDriverWait(driver, timeout=10)
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
img=[]

while(c<3):
    if (c == 2):
        c += 1
        driver.get("https://www.ajio.com/search/?query=%3Arelevance&text="+key+"&gridColumns=5&viewType=productview")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html5lib")
        for a in soup.findAll('div', attrs={'class':'item rilrtl-products-list__item item'}):
            images = a.find('img')
            if(images.get('src')==None):break
            img.append(images.get('src'))
   
#     if(c==1):
#         c+=1
#         driver.get("https://www.flipkart.com/q/"+key+"?sort=popularity")
    
#         content = driver.page_source
#         soup = BeautifulSoup(content, features="html5lib")
#         for a in soup.findAll('div', attrs={'class':'IIdQZO _1SSAGr'}):
#             images = a.find('img', attrs={'class':'_3togXc'})
#             img.append(images.get('src'))
            
#     if(c==0):
#         c += 1
#         driver.get("https://www.amazon.in/s?k="+key+"&ref=nb_sb_noss")
#         content = driver.page_source
#         soup = BeautifulSoup(content, "html5lib")
#         for a in soup.findAll('div', attrs={'class':'s-expand-height s-include-content-margin s-latency-cf-section'}):
#             images = a.find('img', attrs={'class':'s-image'})
#             img.append(images.get('src'))
    

driver.close()

shop={}
for i in range(0,len(img)):
    c=0.00
    for j in range(0,len(img)):
        original = io.imread(img[i])
        original = cv2.resize(original, (100, 133))
        contrast = io.imread(img[j])
        contrast = cv2.resize(contrast, (100, 133))
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

        (score, diff) = skimage.metrics.structural_similarity(original, contrast, full=True)
        if(score!=1.00):
            a=img[i]
            if(a in shop):
                shop[a]=max(score, c)
                c=score
            else:
                a=img[i]
                shop[a]=score
                c=score
sorted_x=sorted(shop.items(), key=operator.itemgetter(1), reverse=True)
with open("file.txt", "w") as o:
    for i in range(math.floor(math.sqrt(len(sorted_x)+1))):
        o.write(str(sorted_x[i][0])+'\n')

wr=open("shop.html", "w")
f=open("file.txt", "r")
for m in f:  
    wr.write("<html><body><br><img src="+m+"></br></body></html>")

wr.close()
    # print(sorted_x[i][0])


# #            
