import re
import sys

new_start = []

if_def = 'test.csv'
of_def = 'urls.csv'
ifile = sys.argv[1] if len(sys.argv) > 1 else if_def
ofile = sys.argv[2] if len(sys.argv) > 2 else of_def
print(ifile)
print(ofile)
urls = []
with open(ifile, "r", encoding='utf-8_sig') as fin, open(ofile, "w", encoding='utf-8_sig') as fout:
    while True:
        buf = fin.readline()
        if (buf):
            dlink = re.search(".*(https://movie.douban.com/subject/[0-9]+/),.*", buf)
            if (dlink):
                url = dlink.group(1)
                urls.append(url)
                fout.write(url+'\n')
        else:
            break
print("len=%s"%len(urls))