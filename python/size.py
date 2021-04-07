# Get File Size on Terminal in Byte, MB, GB, TB - Python

# Python2 : python2 size.py <script>
# Python3 : python3 size.py <script>

import os
import sys

def convert_bytes(num):
    for x in ['Byte', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def main(file):
    try:
        htr1 = open(file).read()
    except IOError:
        sys.exit('[!] File Not Found [!]')
    print('File Size : ' + str(file_size(file)))

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        sys.exit('[-] Type : ' + __file__ + ' <script>')

