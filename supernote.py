import requests, os
from hashlib import sha256, md5

# thank you 
# https://github.com/adrianba/supernote-cloud-api/
# https://github.com/colingourlay/supernote-cloud-api/

API_BASE = "https://cloud.supernote.com/api/"

def _sha256_s(s):
    return sha256(s.encode('utf-8')).hexdigest()
def _md5_s(s):
    return md5(s.encode('utf-8')).hexdigest()
def _md5_b(b):
    return md5(b).hexdigest()

def _post_json(path, payload, token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    if token is not None:
        headers['x-access-token'] = token
    response = requests.post(API_BASE+path, json=payload, headers=headers)
    return response.json()

def _get_random_code(email):
    # countrycode 
    payload = {'countryCode': "1", "account":email }
    data = _post_json("official/user/query/random/code", payload)
    return (data['randomCode'], data['timestamp'])

def _get_access_token(email, password, rc, timestamp):
    pd = _sha256_s(_md5_s(password) + rc);
    payload = {'countryCode':1, 'account':email, 'password':pd, 
        'browser':'Chrome107', 'equipment':"1", "loginMethod":"1", "timestamp":timestamp, "language":"en"}
    data = _post_json("official/user/account/login/new", payload)
    return data['token']

# returns access token
def login(email, password):
    (rc, timestamp) = _get_random_code(email)
    return _get_access_token(email, password, rc, timestamp)

def file_list(token, directory=0):
    payload = {"directoryId": directory, "pageNo":1, "pageSize":100, "order":"time", "sequence":"desc"}
    data = _post_json("file/list/query", payload, token=token)
    return data['userFileVOList']

def download_file(token, id, filename=None):
    payload = {"id":id, "type":0}
    data = _post_json("file/download/url", payload, token=token)
    c = requests.get(data['url']).content
    if(filename is not None):
        f = open(filename,'wb')
        f.write(c)
        f.close()
    else:
        return c

def upload_file(token, filename, directory=0):
    file_contents = open(filename,'rb').read()
    data_md5 = _md5_b(file_contents)
    payload = {'directoryId':directory, 'fileName':filename, 'md5':data_md5, 'size':len(file_contents)}
    data = _post_json('file/upload/apply', payload, token=token)
    if(data['success']):
        put_headers = {'Authorization':data['s3Authorization'], 'x-amz-date':data['xamzDate'], "x-amz-content-sha256": "UNSIGNED-PAYLOAD"}
        requests.put(data['url'], file_contents, headers=put_headers)
        inner_name = os.path.basename(data['url'])
        payload = {"directoryId":directory, "fileName":filename, "fileSize":len(file_contents), "innerName":inner_name,"md5":data_md5}
        data = _post_json("file/upload/finish", payload, token=token)
    else:
        print("Error: %s" % (data['errorMsg']))

# as an example, we download the latest NYT crossword and put it on the folder Document/puzzles
# your auth.txt file in the current folder should have
# username,password
# NYT-cookie0 (load the NYT page and copy your cookies)
# NYT-cookie1 ("print" a crossword and copy your cookies from that request)
if __name__ == '__main__':
    import nyt
    uploaded=False
    auth = open('auth.txt').read().split('\n')
    (username,password) = auth[0].split(',')
    puzzle_fn = nyt.get(auth[1], auth[2])
    if puzzle_fn is not None:
        token = login(username, password)
        if token is None:
            print("Couldn't log into supernote")
        else:
            for d in file_list(token):
                if(d['isFolder']=='Y' and d['fileName']=="Document"): 
                    document_id = d['id']
                    for d in file_list(token, document_id):
                        if(d['isFolder']=='Y' and d['fileName']=="puzzles"): 
                            puzzles_id = d['id']
                            upload_file(token, puzzle_fn, directory=puzzles_id)
                            uploaded = True
            if not uploaded:
                print("Didn't upload puzzle. Check you have a puzzles folder in Document on Supernote cloud")

    else:
        print("Problem downloading puzzle, bad NYT cookies?")
