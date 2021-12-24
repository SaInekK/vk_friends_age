import datetime

import requests

ACCESS_TOKEN = ''  # Your access token
API_URL = 'https://api.vk.com/method'
VERSION = '5.131'


def get_id_by_username(username):
    url = f'{API_URL}/users.get'
    r = requests.get(url, params={
        'access_token': ACCESS_TOKEN,
        'user_ids': username,
        'v': VERSION
    })
    return r.json()['response'][0]['id']


def get_friends_by_username(username):
    uid = get_id_by_username(username)
    url = f'{API_URL}/friends.get'
    r = requests.get(url, params={
        'access_token': ACCESS_TOKEN,
        'user_id': uid,
        'fields': 'bdate',
        'v': VERSION
    })
    return r.json()['response']['items']


def calc_age(username):
    friends = get_friends_by_username(username)
    today = datetime.date.today()
    ages_dict = {}
    for friend in friends:
        date_str = friend.get('bdate')
        if not date_str:
            continue
        if len(date_str.split('.')) == 3:
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
            delta = today - date
            years = int(delta.days / 365.2425)
            if years not in ages_dict:
                ages_dict[years] = 1
            else:
                ages_dict[years] += 1
    res = [(k, v) for k, v in ages_dict.items()]
    res.sort(key=lambda x: (-x[1], x[0]))
    return res


if __name__ == '__main__':
    username = 'reigning'  # 'reigning'

    counts = calc_age(username)
    print(counts)
