def send_data(out):
    #inserting name
    name = out[0].split(',')[0].split(" ")
    middle_name = ""
    first_name = name[1]
    last_name = ' '.join(name[2:])


    #inserting gender
    gender = out[1]

    #inserting npi
    npi = out[2]

    #inserting speciality
    speciality = out[3].split(",")[0]

    #inserting about
    about = out[9]

    #inserting email
    email = out[8].split('/')[-1]+"@gmail.com"

    #inserting address
    country = 'United States'
    city = out[7].split(',')[0]
    state = out[7].split(',')[1][1:]

    #inserting password
    password = 'DemoDoc@1234'
    verify = 'True'

    #inserting fees
    fee_list = [200, 500, 1000, 700, 600, 1500, 2000]
    fee = random.choice(fee_list)

    #education

    degree = out[0].split(',')[1:]
    university = out[5].split('- ')[1].split(',')[0]
    edu = []
    for i in degree:
         edu.append(
             {
                 'degree':i[1:],
                 'university':university,
                 'year':''
             }
         )
            
      
    #register doctors
    payload = {'firstName':first_name,
              'lastName':last_name,
              'email':email,
              'country':country,
              'state':state,
              'city':city,
              'password':password,
              'basic':{},
              'specialty':speciality,
              'registration_number':npi}
    try:
        r = rp.post('https://server.mddocz.com/doctors/register', json = payload)
    
    
        get_id = r.json()['data']['_id'] #id of created
        datas[email] = get_id

        if(len(datas.keys()) % 100 == 0):
            pickle_out = open('inserted_postman.pickle','wb')#change for another checkpoint
            pickle.dump(datas, pickle_out)
            pickle_out.close()


        #update_doctors
        payload = {
            'gender':gender,
            'id':get_id,
            'bio':about,
            'education': edu,
            'fee':fee,
            'verify':'true',
        }
        r = rp.post('https://server.mddocz.com/doctors/profile/update', json = payload)
        
    except:
        print('something wrong')

for i in tqdm(data[:10]):
    send_data(i)