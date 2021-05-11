# Simple Python Spammer using pyautogui

# Python2 : python2 formatter.py <text> <count>
# Python3 : python3 formatter.py <text> <count>

import sys
import time
import pyautogui

def main(msg,count):
    time.sleep(3)
    for i in range(int(count)):
        pyautogui.typewrite(msg)
        pyautogui.press('enter')
        time.sleep(0.25)

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1],sys.argv[2])
    else:
        sys.exit('[-] Type : ' + __file__ + ' <text> <count>')
