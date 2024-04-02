import requests, os
from hashlib import sha256, md5

# thank you 
# https://github.com/adrianba/supernote-cloud-api/

def sha256_d(s):
    return sha256(s.encode('utf-8')).hexdigest()

def md5_d(s):
    return md5(s.encode('utf-8')).hexdigest()

def post_json(path, payload, token=None):
    base = "https://cloud.supernote.com/api/"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    if token is not None:
        headers['x-access-token'] = token
    response = requests.post(base+path, json=payload, headers=headers)
    return response.json()

def get_random_code(email):
    # countrycode 
    payload = {'countryCode': "1", "account":email }
    data = post_json("official/user/query/random/code", payload)
    return (data['randomCode'], data['timestamp'])

def get_access_token(email, password, rc, timestamp):
    pd = sha256_d(md5_d(password) + rc);
    payload = {'countryCode':1, 'account':email, 'password':pd, 
        'browser':'Chrome107', 'equipment':"1", "loginMethod":"1", "timestamp":timestamp, "language":"en"}
    data = post_json("official/user/account/login/new", payload)
    return data['token']

# returns access token
def login(email, password):
    (rc, timestamp) = get_random_code(email)
    return get_access_token(email, password, rc, timestamp)

def file_list(token, directory=0):
    payload = {"directoryId": directory, "pageNo":1, "pageSize":100, "order":"time", "sequence":"desc"}
    data = post_json("file/list/query", payload, token=token)
    return data['userFileVOList']

def download_file(token, id, filename=None):
    payload = {"id":id, "type":0}
    data = post_json("file/download/url", payload, token=token)
    c = requests.get(data['url']).content
    if(filename is not None):
        f = open(filename,'wb')
        f.write(c)
        f.close()

    




