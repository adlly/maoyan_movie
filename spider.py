#-*-coding:UTF-8 -*-
import json
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
        # for i in items:
        #     a = ''.join(i).encode('utf-8')
        #     print a
        #     write_to_file(a)
        for i in  items:
            yield{
                'index': i[0],
                'image': i[1],
                'title': i[2],
                'actor': i[3].strip()[3:],
                'time': i[4].strip()[5:],
                'score': i[5] + i[6]
            }



    except Exception,e:
        print e.message

def write_to_file(content):
    with open('initial.text', 'a') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+ str(offset)
    html = get_url_page(url)
    #print html
    # text = open('./initial.html', 'w+')
    # text.write(html)
    # text.close()
    for item in parse_one_page(html):
        print item
        write_to_file(item)



if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
