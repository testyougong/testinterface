# -*- coding: utf_8 -*-
import requests
import json


class TestApi():
    def apitest(self, method, url, getparams, postparams):
        result = ''
        if method == 'GET':
            if getparams != '':
                result = requests.get(url, getparams)
            else:
                result = requests.get(url)
        if method == 'POST':
            if postparams != '':
                result = requests.post(url, postparams)

        data = json.loads(result.text)
        return data
