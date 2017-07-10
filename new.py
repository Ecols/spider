# -*- coding: utf-8 -*-
import re
import sys
import time
import sharkspider as ss
import combine as cb

tm_suf=time.strftime("%Y%m%d-%H%M%S", time.localtime())
f_name="uniq-" + tm_suf + ".csv"
dblist=[]


if ((len(sys.argv) == 3)
    and sys.argv[1] == "test"
    and ('https://movie.douban.com/subject/' in sys.argv[2])):
    ss.crawl_url_and_print(sys.argv[2])
    exit()

if (len(sys.argv) == 1):
    pass
elif (len(sys.argv) == 2):
    dblist = cb.combine(sys.argv[1:], f_name, 0)
else:
    wflg = int(sys.argv[-1]) if (len(sys.argv) > 2 and (re.search('^[0-1]$', sys.argv[-1]))) else 0
    list = sys.argv[1:-1] if (len(sys.argv) > 2 and (re.search('^[0-1]$', sys.argv[-1]))) else sys.argv[1:]
    ss.init_file_navigation(f_name)
    dblist = cb.combine(list, f_name, wflg)
    print("len(dblist)=%s" % (len(dblist)))
    exit()

gs0 = ss.g_set_cls()
gs0.g_s0 = {'https://movie.douban.com/subject/26420932/',
            'https://movie.douban.com/subject/26935251/',
            'https://movie.douban.com/subject/26884892/',
            'https://movie.douban.com/subject/26528871/',
            'https://movie.douban.com/subject/26668283/',
            'https://movie.douban.com/subject/26606743/',
            'https://movie.douban.com/subject/26362764/',
            'https://movie.douban.com/subject/26309788/'}
gs0.g_sall = set(dblist)
print("len(gs0.g_s0)=%s"%(len(gs0.g_s0)))
print("len(gs0.g_sall)=%s"%(len(gs0.g_sall)))
ss.init_file_navigation(gs0.file_out)
ss.crawl_loop(gs0)

exit()




# if_def = 'test.csv'
# of_def = 'urls.csv'
# ifile = sys.argv[1] if len(sys.argv) > 1 else if_def
# ofile = sys.argv[2] if len(sys.argv) > 2 else of_def
# print(ifile)
# print(ofile)
# urls = []
# with open(ifile, "r", encoding='utf-8_sig') as fin, open(ofile, "w", encoding='utf-8_sig') as fout:
#     while True:
#         buf = fin.readline()
#         if (buf):
#             dlink = re.search(".*(https://movie.douban.com/subject/[0-9]+/),.*", buf)
#             if (dlink):
#                 url = dlink.group(1)
#                 urls.append(url)
#                 fout.write(url+'\n')
#         else:
#             break
#
# print("len=%s"%len(urls))
