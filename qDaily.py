# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://www.qdaily.com'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)

class Main(Wox):
  
    def request(self,url):
        #break wall
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}

        #get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
            }
            return requests.get(url,proxies = proxies, headers=headers)
        
        return requests.get(url, headers=headers)
			
    def query(self, param):
        r = self.request(URL + "/tags/29.html")
        bs = BeautifulSoup(r.content, 'html.parser')
        posts = bs.find_all('div', 'packery-item')
        result = []
        
        for p in posts:
            if p.find('a') is None:
                continue
            content = p.find("a")
            title = content.find('h3').text
            category = content.find('p', 'category').find('span').text
            timesince = content.find('span', 'smart-date')['data-origindate']
            link = URL + content['href']
            
            item = {
                'Title': full2half(title),
                'SubTitle': category + " | " + timesince,
                'IcoPath': os.path.join('img', 'q.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [link]
                }
            }
            result.append(item)
        
        return result
    
    def open_url(self, url):
        webbrowser.open(url) #use default browser

if __name__ == '__main__':
    Main()
