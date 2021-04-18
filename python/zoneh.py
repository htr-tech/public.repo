# Simple Python Script to Scrape Websites from Zone-h.org

# Python2 : python2 zoneh.py

# Edit the ZHE & PHPSESSID first !

import re
import os
import sys
import six
import time
import requests

snacks = {
	"ZHE" : "713dc407ce706d0a9f9cdd7ad13c027d", # Input Zone-H ZHE
	"PHPSESSID" : "vmomga7dorbva5fnlfv5m0d9r1"  # Input Zone-H PHPSESSID
	}

def zoneh():
    print("\n[1] Scrape from Onhold\n[2] Scrape from Notifier\n[3] Scrape from Special Archive\n")
    raw_menu = six.moves.input('[-] Choose an Option : ')

    if raw_menu == "1" or raw_menu == "01":
        func = '/published=0'
        output = 'onhold_' + time.ctime()[14:19].replace(':','_') + '.txt'
    elif raw_menu == "2" or raw_menu == "02":
        noti = six.moves.input('\n[-] Notifier : ')
        func = '/notifier=' + str(noti)
        output = str(noti) + '_' + time.ctime()[14:19].replace(':','_') + '.txt'
    elif raw_menu == "3" or raw_menu == "03":
        func = '/special=1'
        output = 'special_' + time.ctime()[14:19].replace(':','_') + '.txt'
    else:
        print('')
        sys.exit()

    for hulu in range(1,51):
        requ = requests.get('http://www.zone-h.org/archive'+str(func)+'/page='+str(hulu),cookies=snacks).content

        if '<input type="text" name="captcha" value="">' in requ:
            print('')
            print('[-] Captcha Occured !')
            print('')
            sys.exit()
        else:
            urls = re.findall('<td>(.*)\n							</td>', requ)
            if '/mirror/id/' in requ:
                print('\n[-] Page Number : ' + str(hulu))
                for i in urls:
                    replace_dots = i.replace('...','')
                    site_list = replace_dots.split('/')[0]
                    print('[+] ' + str(site_list))
                    with open(output,'a') as rdp:
                        rdp.write('http://'+str(site_list)+'\n')
            else:
                print('')
                print('[!] Operation Completed')
                print('')
                sys.exit()
    else:
        print('')
        print('[!] Error Occured')
        print('')
        sys.exit()

if __name__ == '__main__':
    zoneh()

