# Simple Url Shortner script using tinyurl.com's api

# Python2 : python2 short.py 'url'
# Python3 : python3 short.py 'url'

import sys
if sys.version_info[0] == 2:
    from urllib import urlopen as url
else:
    from urllib.request import urlopen as url

def main(link):
    apiurl=('http://tinyurl.com/api-create.php?url='+link)
    tinyurl=url(apiurl).read().decode('utf-8')
    print('Shortened Url : '+str(tinyurl))

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        sys.exit('[-] Type : ' + __file__ + ' <link>')

