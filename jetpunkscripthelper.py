#%%
import pyautogui
import time
from selenium import webdriver
time.sleep(2)
pyautogui.click(x=204, y=1057)
time.sleep(3)
pyautogui.hotkey('command','v')
time.sleep(1)     
pyautogui.press('enter')

# j = 0
# while j < 10:
#     print(j)
#     time.sleep(2)
#     pyautogui.hotkey('command','tab')
#     time.sleep(2)
#     my_url = input('Enter URL:')
#     time.sleep(2)
#     pyautogui.hotkey('command','tab')
#     j = j + 1
# %%
