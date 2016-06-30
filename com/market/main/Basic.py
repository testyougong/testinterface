import requests


class Basic():
    def login(self):
        basic = Basic()
        url = basic.basic_url()
        user = {'username': '13466640320', 'password': '000000'}
        result = requests.post(url + '/user/info/login', params=user)
        token = result.json()['content']['token']
        return token

    def basic_url(self):
        basic_url = 'http://qa.market.wmdev2.lsh123.com'
        return basic_url