# -*- coding:UTF-8 -*-
import time

import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import  PyQuery as pq
from config import *
from bs4 import BeautifulSoup
import redis

browser = webdriver.Chrome()
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 200)


def search_url(url):
    browser.get(url)
    #print browser.page_source
    time.sleep(5)
    input_box = browser.find_element_by_id('key')
    submit_btn = browser.find_element_by_css_selector('#search > div > div.form > button > i')
    input_box.send_keys(u'手机')
    submit_btn.click()
    time.sleep(1)
    page = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > em:nth-child(1) > b')
    get_urls()
    return page.text

    # print numbers
    # browser.find_element_by_id('J_goodsList')
    # get_urls()

def save_to_redis(urls):



def get_urls():
    #file_text = browser.page_source()
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList > ul')))
    html = browser.page_source
    # doc = pq(html)
    # ss = doc('#J_goodsList > ul')
    first_pattern = re.compile('<div id="J_goodsList".*?><ul class="gl-warp clearfix".*?>(.*?)</ul><span class="clr"></span></div>',re.S)
    first_content = re.findall(first_pattern, html)
    #print first_content[0]
    second_pattern = re.compile(
        '<div class="p-name p-name-type-\d+">.*?<a target="_blank".*?href="(.*?)".*?</a>.*?</div>', re.S)
    items = re.findall(second_pattern, first_content[0])
    for i in items:
        print i + '\n'

#https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDk0MTAzNzQ4MC5odG1s&log=oiGfZupKTra0gVhJB0u9oPzw7mN-MMw1xMRjmnNEUTWnVHSpv5_FSBwGxRfA7Ma_0bm-riF9JgGeODpqqtEdiDYu1IvseDKBEablfck3jh2pvW7qYc1d4UFxQ5szKj3_3Kov43Rr45Qj9VygDjjKUy-AfJjxYFU4LdmNGo0S7RFK8-3BEulK4YzpFzJEVSgQpr9dJTnxEYMVHSYytaoVjld0Nf-nFKWRqI6mMM4i6RxKbCUr0C_yxq4IqVm5AMbcSJHcoPOJ3hZj_65JQWKYQ_0YK_jFpe9Vw9bN4SlHaoEYKZ9qPzW0nOTQ388EJO0w1ONWY9-S4e06f_AiboaJnm1_YOObCE7AGuYHonj4KhDxF-Uy0zMIp_ja_0bd3oXE1QjG-OBSGYEfWqw3eWS6GzRYWoUtwuEw7E6odumgqZ0&v=404


    # file_text = browser.page_source()



#J_goodsList > ul

def next_page(number):
    try:
        print '正在翻页...第' + str(number) + '页'
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
            # lambda driver:
            # driver.find_element_by_css_selector('#J_bottomPage > span.p-skip > input')
        # )
        # submit_btn =  browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > a')
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
        input_box.clear()
        input_box.send_keys(number)
        submit_btn.click()
        time.sleep(1)
        get_urls()
        # wait.until(EC.staleness_of(input_box))
        # wait.until(EC.staleness_of(submit_btn))
    except(StaleElementReferenceException):
        next_page(number)
    # wait.until(EC.text_to_be_present_in_element(
    #     # J_bottomPage > span.p-num > a.curr
    #     (By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(number)))
    # time.sleep(2)


def main():
    total = search_url('https://www.jd.com')
    numbers = int(total)
    #print type(numbers)
    for i in range(2, numbers):
        next_page(i)


if __name__ == '__main__':
    main()
