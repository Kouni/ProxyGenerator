#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
1.  Renew PROXY LIST if the data is older than five minutes.
    Then save to *proxy_list.json*.
2.  Rendom get IP Information from proxy_list.json, then test it.
3.  coming soon...
'''

from urllib.request import urlopen, Request, ProxyHandler, build_opener, install_opener
from bs4 import BeautifulSoup
import lxml
# import re
import json
import os
import time
import random


'''Get newest proxy list from free-proxy-list.net.
And parsing list data to JSON format file(proxy_list.json)
'''
# Get proxy list information html.


def renew_list():
    req = Request("https://free-proxy-list.net/#list",
                  headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=1) as n:
        with open('cache.html', 'wt') as f:
            f.write(n.read().decode('UTF-8'))

    # Parsing proxy list to JSON file.
    soup = BeautifulSoup(open("cache.html"), "lxml")
    ips = []
    # ipv4_pattern = re.compile('\d+\.\d+\.\d+\.\d+')
    table_body = soup.find('tbody')

    for p_html_tr in table_body.find_all('tr'):
        tds = p_html_tr.find_all('td')
        ips.append({'IP_Address_td': tds[0].string,
                    'Port_td': tds[1].string,
                    'Code_td': tds[2].string,
                    'Country_td': tds[3].string,
                    'Anonymity_td': tds[4].string,
                    'Google_td': tds[5].string,
                    'Https_td': tds[6].string,
                    'Last_Checked_td': tds[7].string})
    with open('proxy_list.json', 'wt')as f:
        f.write(json.dumps(ips))


def get_random_ip():
    global conn_info
    with open('proxy_list.json', 'rt') as f:
        random_ip = random.choice(json.load(f))
    conn_info = json.dumps(random_ip)


'''Valid proxy
'''


def check_proxy():
    global conn_info
    conn_info = json.loads(conn_info)
    proxy_info = (conn_info['IP_Address_td'] + ':' + conn_info['Port_td'])

    opener = build_opener(ProxyHandler({'http': proxy_info}))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    with urlopen('http://ifconfig.co/ip', timeout=10) as f:
        return(f.read().decode('UTF-8'))

if __name__ == '__main__':
    if os.path.exists('proxy_list.json'):
        pass
    else:
        renew_list()

    if time.time() - os.stat("proxy_list.json").st_mtime > 300:
        renew_list()
    else:
        pass

    get_random_ip()
    print("Return IP: " + check_proxy())
    print(conn_info)
