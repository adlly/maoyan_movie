#-*-coding:UTF-8 -*-


import re
import requests
import sys
from requests import  RequestException

reload(sys)
sys.setdefaultencoding('utf-8')

def get_url_page(url):
    try:
        response = requests.get(url)
        if(response.status_code == 200):
            return response.text
    except RequestException:
        return None

def parse_one_page(ss):
    # pattern = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?data-src"(.*?)".*?name"><a.*?>(.*?)</a>'
    #                     +'star">(.*?)</p>.*?releasetime">(.*?)</p>.*?</dd>', re.S)
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)


    try:
        items = re.findall(pattern, ss)
        for i in items:
            a = ''.join(i).encode('utf-8')
            print a
    except Exception,e:
        print e.message



def main():
    url = 'http://maoyan.com/board/4?'
    html = get_url_page(url)
    print html
    text = open('./initial.html', 'w+')
    text.write(html)
    text.close()
    parse_one_page(html)

if __name__ == '__main__':
    main()
