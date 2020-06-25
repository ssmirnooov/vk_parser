import requests
import csv
token = ''
version_api = '5.110'

def take_n_posts():
    domain = 'zenit'
    count_post = 100
    offset = 0
    all_posts = []
    while offset < 1000:
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
        offset += 100
        all_posts.extend(data)
    return all_posts

all_posts = take_n_posts()

def file_writer(all_posts):
    with open('zenit.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'body', 'url'))
        img_url = 'pass'
        for post in all_posts:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except:
                pass
            a_pen.writerow((post['likes']['count'], post['text'], img_url))
all_posts = take_n_posts()
file_writer(all_posts)

