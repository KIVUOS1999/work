from bs4 import *
import requests as rp
import os
from msedge.selenium_tools import *
import time
from tqdm import tqdm
import pickle
import numpy as np
import psycopg2 as ps

options = EdgeOptions()
options.use_chromium = True
#options.add_argument("headless")
options.add_argument("disable-gpu")

#urls of doctor pages
pickle_in = open('zocdoc_remaining_doctor.pickle', 'rb')
cleaned_data_without_repetation = pickle.load(pickle_in)

#to initialize database
def push_to_table(name, gender, npi, specialities, practice_name, eduandtrain, langspoken, lives, address, about, rating, review):
    conn = ps.connect(
        host = '127.0.0.1',
        database = 'zocdoc',
        user = 'postgres',
        password = 'ss123546',
    )
    cur = conn.cursor()
    cur.execute("insert into zocdoc_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name, gender, npi, specialities, practice_name, eduandtrain, langspoken, lives, address, about, rating, review))
    conn.commit()
    conn.close()    

#get_datas_of_inputURLS
def get_page_data(string):
    out = {}
    data = []
    driver = Edge(options = options)
    driver.get(string)
    soup = BeautifulSoup(driver.page_source, 'html.parser')  
    name = soup.find('h1').text
    lives = soup.find_all('h2')[1].text
    specalist = soup.find('section',{'data-test':"Specialties-section"})
    practice = soup.find('section',{'data-test':"Practice-section"})
    education = soup.find('section',{"data-test":"Education-section"})
    language = soup.find('section',{'data-test':"Languages-section"})
    gender = soup.find('section',{'data-test':"Sex-section"})
    npi = soup.find('section',{'data-test':"NPI-section"})
    
    for i in [specalist, practice, education, language]:
        ind = i.find('h3').text
        data = []
        for j in i.find_all('li'):
            data.append(j.text)
        out[ind] = ",".join(data)

    out['npi'] = npi.find('p',{'itemprop':'identifier'}).text
    out['gender'] = gender.find('p').text
    out['name'] = name
    out['lives'] = lives
    out['address'] = string

    try:
        out['about'] = soup.find('span', {'class':'sc-1opoey3-2 itqzoH'}).text + soup.find('span', {'class':'sc-1opoey3-3 jSGFbe'}).text
    except:
        out['about'] = ''
    try:   
        b= soup.find_all('div', {'data-test':'location-card-address-container'})
        add = []
        for i in b:
            add.append(i.text)
            out['location'] = ";".join(add)
    except:
        out['location'] = ''
    try:
        out['rating'] = soup.find('div', {'data-test':'star-rating-score'}).text
    except:
        out['rating'] = ''
    try:
        out['review'] = soup.find('div', { 'data-test':"reviews-filter-panel-review-count"}).text.split(" ")[0]
    except:
        out['review'] = ''
        
    driver.close()
    return out

#driver change the number to total_you_have_scraped + 1
for i in tqdm(cleaned_data_without_repetation[5039:]):
    try:
        out = get_page_data(i)
    except:
        continue
    push_to_table(out['name'], out['gender'], out['npi'], out['Specialties'], out['Practice names'], out['Education and training'], out['Languages spoken'], out['lives'], out['address'], out['about'], out['rating'], out['review'])