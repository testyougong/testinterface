import requests


class Basic():
    def login(self):
        basic = Basic()
        url = basic.basic_url()

        headers = {'device-id': '1'}
        user = {'username': '16001346601', 'password': '000000','device-id':'1'}
        result = requests.post(url + '/user/info/login', params=user, headers = headers)
        token = result.json()['content']['token']
        return token

    def basic_url(self):
        basic_url = 'http://qa.market.wmdev2.lsh123.com'
        return basic_url


    def mis_login(self):
        mis = Basic()
        url = mis.mis_url()
        user = {'email':'admin@lsh123.com','pwd':'111111qQ'}
        result = requests.post(url + '/account/user/checklogin',params=user)
        cookies = result.headers.get('Set-Cookie')
        return cookies

    def mis_url(self):
        mis_url = 'http://qa.market-mis.wmdev2.lsh123.com'
        return mis_url
