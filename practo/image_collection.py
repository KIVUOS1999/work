from bs4 import *
import requests as rp
from msedge.selenium_tools import *
import time
from tqdm import tqdm
import pickle

options = EdgeOptions()
options.use_chromium = True
options.add_argument("headless")
options.add_argument("disable-gpu")
import urllib.request
import os

def get_image(url):
    driver = Edge(options = options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_links = soup.find_all('img', {'class':'u-circle profile-photo'})
    for i in img_links:
        save_image(i['src'], i['alt'])
        
def image_collector(city):
    len([name for name in os.listdir('.') if os.path.isfile(name)])
    for i in tqdm(range(1,1000)):
        count = len(os.listdir('E:/Youtube game/works/'))
        if(count > 2000):
            break
        url = "https://www.practo.com/search?results_type=doctor&q=%5B%7B%22word%22%3A%22doctor%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22type%22%7D%5D&city="+city+"&page="+str(i)
        get_image(url)
    return count

def save_image(url, file_name, file_path = 'E:/Youtube game/works/'):
    try:
        full_path = file_path+file_name+'.jpg'
        urllib.request.urlretrieve(url, full_path)
    except:
        print('something wrong with: '+url)
       
    
image_collector('mumbai')