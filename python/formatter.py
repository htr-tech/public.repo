# Simple Python Script to mass add http & format a website list

# Python2 : python2 formatter.py <list>
# Python3 : python3 formatter.py <list>

import sys
def main(file):
    try:
        hunt = open(file).read()
    except IOError:
        sys.exit('[!] File Not Found')
    output = 'formatted_' + str(file)
    hunt = open(file,'r')
    for hulu in hunt:
        hulu = hulu.rstrip()
        replace_dots = hulu.replace('...','')
        site_list = replace_dots.split('/')[0]
        print('[+] http://' + str(site_list))
        with open(output,'a') as rdp:
            rdp.write('http://' + str(site_list) + '\n')
    else:
        sys.exit('\n[!] Operation Completed\n')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        sys.exit('[-] Type : ' + __file__ + ' <list>')

