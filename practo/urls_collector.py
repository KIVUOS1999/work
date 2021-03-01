from bs4 import *
import requests as rp
import os
from msedge.selenium_tools import *
import time
from tqdm import tqdm
import pickle
import numpy as np

options = EdgeOptions()
options.use_chromium = True
options.add_argument("headless")
options.add_argument("disable-gpu")

#returns lists of doctors urls from a page.
def get_urls(url):
    data = []
    driver = Edge(options = options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_urls = []
    out = soup.find_all('div', {'class':'info-section'})
    for i in out:
        links = i.find('a')['href']
        data.append(links)
    return data

#travells through specific city and all its pages.
def url_collector(city = 'mumbai'):#change city
    all_urls = []
    for i in range(1,1000):#no of pages you want to travell
        if(len(all_urls) == 2000): #total data you want to collect
            break
        if(i%10 == 0):
            print(i, len(all_urls))
        url = "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22doctor%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22type%22%7D%5D&city="+city+"&page="+str(i)
        try:
            b = get_urls(url)
            if(len(b) == 0):
                print(i)
            all_urls += b
        except:
            continue
    return all_urls