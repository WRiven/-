from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

browser=webdriver.Chrome()
wait=WebDriverWait(browser,90)

def index_page(years):
    '''
    抓取索引页
    :param years:年份
    '''
    print('正在爬取',years,'年数据')
    try:
        url='http://data.stats.gov.cn/easyquery.htm?cn=E0103'
        browser.get(url)
        if years:
            button=browser.find_element_by_css_selector('#mySelect_sj\
 div.dtHead')
            button.click()
            input=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#mySelect_sj\
 div.dtFoot>input')))
            submit=wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#mySelect_sj\
 div.dtFoot>div.dtTextBtn')))
            input.clear()
            input.send_keys(years)
            submit.click()
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,'#table_main')))
        get_datas()
    except TimeoutException:
        index_page(years)

def get_datas():
    '''
    提取统计数据
    '''
    element=browser.find_element_by_css_selector('#table_main')
    td_content=element.find_elements_by_tag_name("td")
    lis=[]
    for td in td_content:
        lis.append(td.text)
        while len(lis)>=11:
            product={
                'area':lis[0],
                'data':lis[1:]
            }
            print(product)
            save_to_mongo(product)
            lis=[]

MONGO_URL='localhost'
MONGO_DB='GDP'
MONGO_COLLECTION='economic'
