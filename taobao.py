#-*- coding:UTF-8 -*-
import json
import re
from selenium import  webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
#from selenium.webdriver import phantomjs
from config import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')
## 比如下面 就没有这个包; 怎么办  alter+enter 直接安装就行 但是你要知道 他后台条用的也是 pip install 就行
## 这样是不是比较好




#browser = webdriver.Chrome()
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 100)

def search():
    try:
        print('正在搜索....')
        browser.get('http://www.taobao.com')
        # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        # input 与系统函数 input() 同名 可能发生错误
        input_box = browser.find_element_by_id('q')
        # element = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.ID, "myDynanicElement"))
        # )
        # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        submit = browser.find_element_by_css_selector('#J_TSearchForm > div.search-button > button')
        input_box.send_keys(u'美食')
        submit.click()
        total = browser.find_element_by_css_selector('#mainsrp-pager > div > div > div > div.total')
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        print('正在翻页'+ str(page_number))
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        submit = browser.find_element_by_css_selector('#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')
        input_box.clear()
        input_box.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()

    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'url': item.find('.title .a').attr('href'),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }

        #  如果你清楚的知道数据结构, 你应该按预期的结果走啊
        # dict 如何便利?
        # 此处的i 已经不是 dict 了
        # product 才是
        # 你这还有一个误区
        # dict 怎么便利
        # for i in product:
        #     # file.write(json.dumps(i))
        #     file.write(('key: ' + str(i) + ' value: ' + str(product[i])).encode('utf-8'))
        #
        #print product
        type(json.dumps(product))
        print json.dumps(product)
        file.write(json.dumps(product).decode('unicode_escape')+'\n')

file = open('information.txt', 'w+')
def main():
    # file在本函数中的变量, 智能在本函数中使用
    # 1. 要么传参给下级函数用
    # 2. 或者定位全局变量

    total = search()
    numbers = int(re.compile('(\d+)').search(total).group(1))
    # print numbers
    for i in range(2, numbers + 1):
        next_page(i)
    file.close()
    browser.close()


if __name__ == '__main__':

    main()
















