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

#%%
# OPEN BROWSER
drive = webdriver.Chrome(executable_path='Documents/Random/CS/Jetpunk/chromedriver')
drive.get('https://www.jetpunk.com/user-stats')
pyautogui.hotkey('command','ctrl','f')

time.sleep(1)
pyautogui.click(x=1460, y=151)
username = 'jetpunkspeedrun'
password = '11111111'
pyautogui.click(x=876, y=257)
time.sleep(1)
pyautogui.typewrite(username)
pyautogui.press('tab')
pyautogui.typewrite(password)
pyautogui.press('enter')
time.sleep(2)
pyautogui.click(x=693, y=700)
time.sleep(1)
pyautogui.click(x=681, y=850)
pyautogui.sleep(1)
pyautogui.click(x=733, y=649)

# pyautogui.hotkey('command', 'shift','p')
# pyautogui.press('enter')
# time.sleep(5)

# # GET POSITION
# # print(pyautogui.position())

#%%
j = 0
while j < 10:
    time.sleep(3)
    pyautogui.click(x=591, y=799) #click on first quiz
    time.sleep(3)
    pyautogui.click(x=322, y=63) #click on search bar
    time.sleep(1)
    pyautogui.hotkey('command','c') #copy link
    pyautogui.click(x=166, y=664) #click out of url
    time.sleep(2)
    pyautogui.hotkey('command','tab') #go to code
    time.sleep(1)
    pyautogui.hotkey('ctrl','tab') #go to jetpunkscripthelper
    time.sleep(3)
    pyautogui.hotkey('ctrl','enter') #run jetpunkscripthelper in jupyter cell
    my_url = input('Enter URL:') #link
    time.sleep(1)
    pyautogui.hotkey('ctrl','tab') #go back to jetpunkscript.py
    time.sleep(3)
    pyautogui.hotkey('command','tab') #go to chrome tab
    time.sleep(1)

    # LINKS
    #my_url = 'https://www.jetpunk.com/quizzes/how-many-countries-can-you-name'
    #my_url = 'https://www.jetpunk.com/quizzes/highest-grossing-movies-quiz-2'
    #my_url = 'https://www.jetpunk.com/user-quizzes/91108/countries-by-first-and-last-two-letters'
    #my_url = 'https://www.jetpunk.com/user-quizzes/234916/all-first-level-subdivision-capitals-of-the-world-on-a-map'
    #my_url = 'https://www.jetpunk.com/quizzes/flags-of-the-world-quiz'
    #my_url = 'https://www.jetpunk.com/quizzes/biggest-world-cities-quiz'
    #my_url = 'https://www.jetpunk.com/quizzes/rhode-island-trivia'
    # my_url = 'https://www.jetpunk.com/quizzes/countries-with-highest-gdp-as-a-percent-of-continent'
    # my_url = 'https://www.jetpunk.com/user-quizzes/331916/countries-by-cartoon-riddles'
    #my_url = 'https://www.jetpunk.com/quizzes/movies-by-year-1990-2009'
    #my_url = 'https://www.jetpunk.com/user-quizzes/2/fast-typing-a-to-z'

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
    #answers2 = np.empty(np.size(lines), dtype = object)

    for i in range(np.size(lines)):
        if(lines[i].count('"isName":false') > 0):
            start = lines[i].find('"cols":')
            end = lines[i].find(']')
            temp = lines[i].replace(lines[i][0:start+8],"")
            temp2 = temp.replace(temp[end - start - 8:len(temp)],"")
            parsetemp = temp2.split('","')
            temp3 = parsetemp[len(parsetemp)-1]
            temp4 = temp3.replace('"',"")
            #answers2[i] = temp4
            answers[i] = exrex.getone(temp4)
        elif(lines[i].count('"typeins"') > 0):
            start = lines[i].find('"val"')
            end = lines[i].find(',"mode"')
            temp = lines[i].replace(lines[i][0:start+6],"")
            temp2 = temp.replace(temp[end - start - 6:len(temp)],"")
            temp3 = temp2.replace('"',"")
            #answers2[i] = temp3
            answers[i] = exrex.getone(temp3)


    answers = list(set(answers))

    # answer = 0

    # unicodedata.normalize('NFKD', answer).encode('ascii', 'ignore')

    #%%
    #PRINT ANSWERS
    #pyautogui.click(x=685, y=584)
    start = drive.find_element_by_id('start-button')
    start.click()
    time.sleep(1)
    for i in answers:
        pyperclip.copy(i)
        pyautogui.hotkey('command','v',interval = 0.001)
        pyautogui.hotkey('command', 'a',interval = 0.001)
        pyautogui.hotkey('delete',interval = 0.001)

    # for i in answers:
    #     pyautogui.typewrite(i)
    #     time.sleep(0.001)
    pyautogui.click(x=247, y=565)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.click(x=24, y=62)
    j = j + 1

# %%
