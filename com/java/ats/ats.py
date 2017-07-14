import json

import requests

host = 'http://test.api.ats.lsh123.com'
headers = {'Content-Type': 'application/json', 'api-version': 'v1.0', 'random': '12345', 'platform': 'H5'}
data = {
    "channel": 1,
    "businessCode" : "111293",
    "audio" : "111212",
    "ext" : ""
}
result = requests.post( host +'/ats/api/transfer/common',data = json.dumps(data) ,headers = headers)
print result.text
