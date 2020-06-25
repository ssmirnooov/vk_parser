import requests
import csv
import nltk
import pymorphy2

token = '0c83d8b30c83d8b30c83d8b3c20cf147c600c830c83d8b35277d56aec18f250e38d3881'
version_api = '5.110'
names = {'Джордж Мартин' : 0, 'Владимир Путин' : 1}
vk_groups = ['true_lentach', 'vladimir_vladimirovichp', 'er_ru']
prob_thresh = 0.4
morph = pymorphy2.MorphAnalyzer()
site = 'https://vk.com/'
file = open('data.csv', 'w')
pen = csv.writer(file)
pen.writerow(('name', 'url'))
all_posts = []

def take_n_posts():
    number_words = 0
    for domain in vk_groups:
        count_post = 100
        offset = 0
        while offset < 100:
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params = {
                                        'access_token' : token,
                                        'v' : version_api,
                                        'domain' : domain,
                                        'count' : count_post,
                                        'offset' : offset
                                    }
                                    )
            data = response.json()['response']['items']
            all_posts.extend(data)
            offset += 100

        for i in data:
            text = nltk.word_tokenize(i['text'])
            number_words += len(text)
            for j in range(1, len(text)-1):
                    prev = morph.parse(text[j - 1])[0].normal_form.lower()
                    current = morph.parse(text[j])[0].normal_form.lower()
                    next = morph.parse(text[j + 1])[0].normal_form.lower()
                    for name, id in names.items():
                        first_name = name.split()[0].lower()
                        surname = name.split()[1].lower()
                        if current == surname.lower():
                            if prev == first_name or next == first_name:
                                pen.writerow((id, (site + domain + '?w=wall' + str(i['owner_id']) + '_' + str(i['id']))))
                                break

take_n_posts()
