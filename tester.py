#%%
from __future__ import unicode_literals
from __future__ import print_function
from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import numpy as np
import pyautogui
import time
import bs4
import pyperclip
import unicodedata
import sys
import os
import re
import exrex

# LINKS
my_url = 'https://www.jetpunk.com/quizzes/how-many-countries-can-you-name'
#my_url = 'https://www.jetpunk.com/quizzes/highest-grossing-movies-quiz-2'
#my_url = 'https://www.jetpunk.com/user-quizzes/91108/countries-by-first-and-last-two-letters'
#my_url = 'https://www.jetpunk.com/user-quizzes/234916/all-first-level-subdivision-capitals-of-the-world-on-a-map'
#my_url = 'https://www.jetpunk.com/quizzes/flags-of-the-world-quiz'
my_url = 'https://www.jetpunk.com/quizzes/biggest-world-cities-quiz'
#my_url = 'https://www.jetpunk.com/quizzes/rhode-island-trivia'
# my_url = 'https://www.jetpunk.com/quizzes/countries-with-highest-gdp-as-a-percent-of-continent'
# my_url = 'https://www.jetpunk.com/user-quizzes/331916/countries-by-cartoon-riddles'
#my_url = 'https://www.jetpunk.com/quizzes/movies-by-year-1990-2009'
#my_url = 'https://www.jetpunk.com/user-quizzes/2/fast-typing-a-to-z'
#my_url = 'https://www.jetpunk.com/user-quizzes/6121/countries-of-the-world-with-an-empty-map'

uClient = uReq(my_url)
pagehtml = uClient.read()
uClient.close()

# PARSING

pagesoup = soup(pagehtml,"html.parser")
scripts = pagesoup('script')
answerblock = str(scripts[8])

# if not (("PYTHONIOENCODING" in os.environ) and re.search("^utf-?8$", os.environ["PYTHONIOENCODING"], re.I)):
#     sys.stderr.write(sys.argv[0] + ": Please set your PYTHONIOENCODING envariable to utf8\n")
#     sys.exit(1)

AnswerStart = '"answers":'
AnswerEnd = ',"whatkind"'
NewBlock = answerblock.partition(AnswerStart)[2]
NewerBlock = NewBlock.partition(AnswerEnd)[0]


for i in range(NewerBlock.count('"id":')):
    NewestBlock = NewerBlock.replace('},{"id":','},\n{"id":')

lines = NewestBlock.split(",\n")
answers = np.empty(np.size(lines), dtype = object)
answers2 = np.empty(np.size(lines), dtype = object)

for i in range(np.size(lines)):
    if(lines[i].count('"isName":false') > 0):
        start = lines[i].find('"cols":')
        end = lines[i].find(']')
        temp = lines[i].replace(lines[i][0:start+8],"")
        temp2 = temp.replace(temp[end - start - 8:len(temp)],"")
        parsetemp = temp2.split('","')
        temp3 = parsetemp[len(parsetemp)-1]
        temp4 = temp3.replace('"',"")
        answers2[i] = temp4
        answers[i] = exrex.getone(temp4)
        if(answers[i].count('<br />') > 0):
            answers[i] = answers[i].replace("<br />"," ")
    elif(lines[i].count('"typeins"') > 0):
        start = lines[i].find('"val"')
        end = lines[i].find(',"mode"')
        temp = lines[i].replace(lines[i][0:start+6],"")
        temp2 = temp.replace(temp[end - start - 6:len(temp)],"")
        temp3 = temp2.replace('"',"")
        answers[i] = exrex.getone(temp3)
        if(answers[i].count('<br />') > 0):
            answers[i] = answers[i].replace("<br />"," ")
        answers2[i] = temp3


answers = list(set(answers))

# %%
