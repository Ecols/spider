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
    dblist = cb.combine(['all.csv'], f_name, 0)
    gs0 = ss.g_set_cls()
    gs0.g_sall = set(dblist)
    ss.crawl_weekly_top10(gs0)
    ss.init_file_navigation(gs0.file_out)
    ss.crawl_loop(gs0)
    exit()
    
elif (len(sys.argv) == 2):
    dblist = cb.combine(sys.argv[1:], f_name, 0)
    gs0 = ss.g_set_cls()
    gs0.g_s0 = {'https://movie.douban.com/subject/27165956/'}
    gs0.g_sall = set(dblist)
    print("len(gs0.g_s0)=%s"%(len(gs0.g_s0)))
    print("len(gs0.g_sall)=%s"%(len(gs0.g_sall)))
    ss.init_file_navigation(gs0.file_out)
    ss.crawl_loop(gs0)
    exit()
else:
    wflg = int(sys.argv[-1]) if (len(sys.argv) > 2 and (re.search('^[0-1]$', sys.argv[-1]))) else 0
    list = sys.argv[1:-1] if (len(sys.argv) > 2 and (re.search('^[0-1]$', sys.argv[-1]))) else sys.argv[1:]
    ss.init_file_navigation(f_name)
    dblist = cb.combine(list, f_name, wflg)
    print("len(dblist)=%s" % (len(dblist)))
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
