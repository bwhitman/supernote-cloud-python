# nyt.py
# get puzzle
import requests, datetime, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

def get(cookie0, cookie1):
    referer = 'https://www.nytimes.com/crosswords/archive/daily'
    today = datetime.datetime.now().strftime('%m%d%y')
    headers = {"cookie":cookie0, "User-Agent":UA, "Referer":referer}
    url = "https://www.nytimes.com/crosswords"
    d = requests.get(url, headers=headers)
    puzzle_id = re.search(r"\"daily_puzzle\"\:\[\{\"puzzle_id\"\:(.*?)\,", str(d.content)).groups()[0]
    url = 'https://www.nytimes.com/svc/crosswords/v2/puzzle/'+str(puzzle_id)+'.pdf'
    headers.update( {"cookie":cookie1, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9','Cache-Control': 'no-cache' })
    d = requests.get(url, headers=headers)
    if(len(d.content)>1000):
        f = open('puzzle-%s.pdf' % (today), 'wb')
        f.write(d.content)
        f.close()
        return "puzzle-%s.pdf" % (today)
    else:
        print("problem saving crossword")
    return None