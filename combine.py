# -*- coding: utf-8 -*-
import util
import re
import time

def combine(inf_list, outfile, wflg):
    #enc = 'utf-8_sig' if (util.isWindows) else 'utf-8'
    enc = 'utf-8'
    only_list, ofp = [], ''
    t0=time.time()
    if (wflg):
        ofp = open(outfile, "a", encoding=enc)
    for inf in inf_list:
        with open(inf, "r", encoding=enc) as ifp:
            for line in ifp.readlines():
                match_link = re.search(".*,(https://movie.douban.com/subject/[0-9]+/),.*", line)
                if (match_link):
                    link = match_link.group(1)
                    if (link not in only_list):
                        only_list.append(link)
                        if (wflg):
                            ofp.write(line)
        ifp.close()
    print("[%s]: len(only_list)=%s"%(combine.__name__, len(only_list)))
    if wflg:
        ofp.close()
    t1 = time.time()
    print("[%s]: using time=%.5s"%(combine.__name__, (t1-t0)))
    return only_list

if (__name__ == "main"):
    print("running as main")