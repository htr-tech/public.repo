# Simple Python Script to fetch Url from the Wayback Machine

# Python2 : python2 short.py <domain>
# Python3 : python3 short.py <domain>

import sys
import requests

def scrape(site):
    url='http://web.archive.org/cdx/search/cdx?url={}/*&fl=original&collapse=urlkey&output=txt'.format(site)
    dat=requests.get(url).text
    if dat:
        out = open(site+'.txt', 'w')
        out.write(dat)
        out.close()
        print('[-] File saved as : {}.txt'.format(site))
    else:
        print('[-] No waybackurls Found')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        scrape(sys.argv[1])
    else:
        sys.exit('[-] Type : ' + __file__ + ' <domain>')

