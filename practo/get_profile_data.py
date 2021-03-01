import urls_collector

#scrap out information of doctors
def get_profile(url):
    driver = Edge(options = options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    out = {}
    try:
        name = soup.find('h1', {'data-qa-id':'doctor-name'}).text
        qualification = soup.find('p', {'data-qa-id':'doctor-qualifications'}).text
        lives = soup.find('p',{'data-qa-id':'clinic-address'}).text
        specilization_lis = []
        specilization = soup.find('div', {'id':'specializations'})
        specilization_names = specilization.find_all('a')
        for i in specilization_names:
            specilization_lis.append(i.text)
        education_lis = []
        education = soup.find('div', {'id':'education'})
        education_list = education.find_all('div', {'class':'pure-u-1'})
        for i in education_list:
            education_lis.append(i.find('span').text)

        out['name'] = name
        out['qualification'] = qualification
        out['lives'] = lives
        out['specilization'] = ",".join(specilization_lis)
        out['education'] = ",".join(education_lis)
    except:
        pass
    return out

output = []
pickle_out = open('checkpoint2.pickle','wb')#change for another checkpoint
pickle.dump(output, pickle_out)
pickle_out.close()

for i in tqdm(data[1051:]):
    out = get_profile('https://www.practo.com'+i)
    if(len(output)%50 == 0):
        
        pickle_in = open('checkpoint2.pickle', 'rb')#change for another checkpoint
        previous_array = pickle.load(pickle_in)
        saving = np.array(output)
        pickle_in.close()
        
        saving1 = np.concatenate((previous_array, saving))
        
        pickle_out = open('checkpoint2.pickle','wb')#change for another checkpoint
        pickle.dump(saving1, pickle_out)
        pickle_out.close()
        output = []
        
    output.append(out)