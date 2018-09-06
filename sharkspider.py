#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import os
from lxml import etree
import util

class g_set_cls():
    g_index = 0
    g_loop = 0
    g_depth = 10
    g_delay = 5
    g_s0=set()
    g_sn=set()
    g_sall=set()
    Domain='https://movie.douban.com'
    Base_url = 'https://movie.douban.com/top250'
    tmpre=time.strftime("%Y%m%d-%H%M%S", time.localtime())
    pwd=os.getcwd()
    file_out = pwd + '/movies-' + tmpre + '.csv'

def crawl_weekly_top10(g_set):
    page_url = g_set.Domain
    page_sel = etree.HTML(requests.get(page_url).text)
    top10_url = page_sel.xpath('//div[@class="billboard-bd"]/table/tr/td[2]/a/@href')
    g_set.g_s0 = set(top10_url)

def crawl_top250_url(g_set):
    page_url = g_set.Base_url
    while True:
        page_sel = etree.HTML(requests.get(page_url).text)
        urls = page_sel.xpath('//div[@class="hd"]/a/@href')
        for url in urls:
            g_set.g_s0.add(url)

        page_next = page_sel.xpath('//span[@class="next"]/a/@href')
        if (page_next):
            page_url = g_set.Base_url + page_next[0]
            time.sleep(1)
        else:
            break
    g_set.g_sall = g_set.g_s0.copy()

def print_top250_url(g_set):
    for idx, url in enumerate(g_set.g_s0):
        print ("idx=%s,url=%s" % (idx, url))

def crawl_url_and_save_to_file(g_set, dep, url, fp):
    timepre = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s] crawl url: %s"%(timepre, url))
    g_set.g_loop = g_set.g_loop + 1
    req = requests.get(url)
    page_sel = etree.HTML(req.text)

    morelink = page_sel.xpath('//div [@class="recommendations-bd"]/dl/dd/a/@href')
    for link in morelink:
        link = link.split('?')[0]
        if (link not in g_set.g_sall):
            g_set.g_sn.add(link)

    if (url in g_set.g_sall):
        timepre = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[%s] skip url: %s" % (timepre, url))
        return

    rate = page_sel.xpath('//strong/text()')
    if (rate and float(rate[0]) >= 7.0):
        area = re.search('地区:</span> (.*)<', req.text)
        i08_area = area.group(1) if area else ''
        i00_are0 = i08_area.split(' ')[0]
        i02_name = page_sel.xpath('//span[@property="v:itemreviewed"]/text()')
        if (i02_name):
            i02_name = i02_name[0].split(' ')[0]
        else:
            return
        i03_rate = rate[0]
        i04_year = page_sel.xpath('//span[@class="year"]/text()')
        if (i04_year):
            i04_year = i04_year[0].split(' ')[0]
            i04_year = re.match('\(([0-9]+).*\)', i04_year)
            i04_year = i04_year.group(1) if i04_year else ''
        else:
            return
        i05_drct = page_sel.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()')
        if (i05_drct):
            i05_drct = i05_drct[0].split(' ')[0]
        else:
            return
        i01_indx = g_set.g_index
        i06_type = page_sel.xpath('//span[@property="v:genre"]/text()')
        i06_type = ','.join(i06_type)
        i07_long = page_sel.xpath('//span[@property="v:runtime"]/@content')
        i07_long = i07_long[0] if i07_long else ''
        i09_cmnt = page_sel.xpath('//span[@property="v:votes"]/text()')[0]
        i11_dlnk = url.split('?')[0]
        i10_sbid = re.match('.*/([0-9]+)/', i11_dlnk).group(1)
        i12_ilnk = page_sel.xpath('//*[@id="info"]/a/@href')
        i13_loop = g_set.g_loop
        i14_dtop = page_sel.xpath('//span[@class="top250-no"]/text()')
        i14_dtop = i14_dtop[0].strip('No.') if i14_dtop else ''

        ilink, ilinks = '', i12_ilnk if (i12_ilnk) else ''
        for try_link in ilinks:
            if ('www.imdb.com' in try_link):
                ilink = try_link
                break
        i12_ilnk = ilink

        print ("Dep[%s]=============================================" % dep)
        print ("i00_are0=%s"%i00_are0)
        print ("i01_indx=%s"%i01_indx)
        print ("i02_name=%s"%i02_name)
        print ("i03_rate=%s"%i03_rate)
        print ("i04_year=%s"%i04_year)
        print ("i05_drct=%s"%i05_drct)
        print ("i06_type=%s"%i06_type)
        print ("i07_long=%s"%i07_long)
        print ("i08_area=%s"%i08_area)
        print ("i09_cmnt=%s"%i09_cmnt)
        print ("i10_sbid=%s"%i10_sbid)
        print ("i11_dlnk=%s"%i11_dlnk)
        print ("i12_ilnk=%s"%i12_ilnk)
        print ("i13_loop=%s"%i13_loop)
        print ("i14_dtop=%s"%i14_dtop)

        try:
            fp.write(i00_are0.__str__() + ',')
            fp.write(i01_indx.__str__() + ',')
            fp.write('"' + i02_name.__str__() + '"' + ',')
            fp.write(i03_rate.__str__() + ',')
            fp.write(i04_year.__str__() + ',')
            fp.write('"' + i05_drct.__str__() + '"' + ',')
            fp.write('"' + i06_type.__str__() + '"' + ',')
            fp.write(i07_long.__str__() + ',')
            fp.write(i08_area.__str__() + ',')
            fp.write(i09_cmnt.__str__() + ',')
            fp.write(i10_sbid.__str__() + ',')
            fp.write(i11_dlnk.__str__() + ',')
            fp.write(i12_ilnk.__str__() + ',')
            fp.write(i13_loop.__str__() + ',')
            fp.write(i14_dtop.__str__() + '\n')
            g_set.g_index += 1
            g_set.g_sall.add(url)
        except:
            print("Error writing, need to check!")
            fp.write('\n')
            return
    else:
        return

def init_file_navigation(file):
    enc = 'utf-8_sig' if (util.isWindows) else 'utf-8'
    with open(file, 'a', encoding=enc) as fp:
        fp.write('i00_are0,i01_indx,i02_name,i03_rate,'
                 'i04_year,i05_drct,i06_type,i07_long,'
                 'i08_area,i09_cmnt,i10_sbid,i11_dlnk,'
                 'i12_ilnk,i13_loop,i14_dtop\n')
        fp.close()

def crawl_url_and_print(url):
    timepre = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("[%s] crawl url: %s" % (timepre, url))
    req = requests.get(url)
    page_sel = etree.HTML(req.text)
    rate = page_sel.xpath('//strong/text()')
    if (rate and float(rate[0]) >= 7.0):
        area = re.search('地区:</span> (.*)<', req.text)
        i08_area = area.group(1) if area else ''
        i00_are0 = i08_area.split(' ')[0]
        i01_indx = 0
        i02_name = page_sel.xpath('//span[@property="v:itemreviewed"]/text()')
        if (i02_name):
            i02_name = i02_name[0].split(' ')[0]
        else:
            return
        i03_rate = rate[0]
        i04_year = page_sel.xpath('//span[@class="year"]/text()')
        if (i04_year):
            i04_year = i04_year[0].split(' ')[0]
            i04_year = re.match('\(([0-9]+).*\)', i04_year)
            i04_year = i04_year.group(1) if i04_year else ''
        else:
            return
        i05_drct = page_sel.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()')
        if (i05_drct):
            i05_drct = i05_drct[0].split(' ')[0]
        else:
            return

        i06_type = page_sel.xpath('//span[@property="v:genre"]/text()')
        i06_type = ','.join(i06_type)
        i07_long = page_sel.xpath('//span[@property="v:runtime"]/@content')
        i07_long = i07_long[0] if i07_long else ''
        i09_cmnt = page_sel.xpath('//span[@property="v:votes"]/text()')[0]
        i11_dlnk = url.split('?')[0]
        i10_sbid = re.match('.*/([0-9]+)/', i11_dlnk).group(1)
        i12_ilnk = page_sel.xpath('//*[@id="info"]/a/@href')
        i13_loop = 0
        i14_dtop = page_sel.xpath('//span[@class="top250-no"]/text()')
        i14_dtop = i14_dtop[0].strip('No.') if i14_dtop else ''

        ilink, ilinks = '', i12_ilnk if (i12_ilnk) else ''
        for try_link in ilinks:
            if ('www.imdb.com' in try_link):
                ilink = try_link
                break
        i12_ilnk = ilink

        print("i00_are0=%s" % i00_are0)
        print("i01_indx=%s" % i01_indx)
        print("i02_name=%s" % i02_name)
        print("i03_rate=%s" % i03_rate)
        print("i04_year=%s" % i04_year)
        print("i05_drct=%s" % i05_drct)
        print("i06_type=%s" % i06_type)
        print("i07_long=%s" % i07_long)
        print("i08_area=%s" % i08_area)
        print("i09_cmnt=%s" % i09_cmnt)
        print("i10_sbid=%s" % i10_sbid)
        print("i11_dlnk=%s" % i11_dlnk)
        print("i12_ilnk=%s" % i12_ilnk)
        print("i13_loop=%s" % i13_loop)
        print("i14_dtop=%s" % i14_dtop)

def crawl_set_and_save_to_file(g_set, dep):
    for url in g_set.g_s0:
        #with open(file, 'a', encoding='utf-8_sig') as fp:  #for windows run
        coding = 'utf-8_sig' if (util.isWindows) else 'utf-8'
        with open(g_set.file_out, 'a', encoding=coding) as fp:
            crawl_url_and_save_to_file(g_set, dep, url, fp)
        fp.close()
        time.sleep(g_set.g_delay)

def crawl_loop(g_set):
    print("g_s0=%s"%g_set.g_s0)
    for dep in range(g_set.g_depth):
        crawl_set_and_save_to_file(g_set, dep)
        g_set.g_s0 = g_set.g_sn.copy()
        g_set.g_sn.clear()

## main start here
# if (__name__ == "main"):
#     g_set = g_set_cls()
#     crawl_top250_url(g_set)
#     init_file_navigation(g_set.file_out)
#     crawl_loop(g_set)
