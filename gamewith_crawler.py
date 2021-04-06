from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
import pandas as pd
import numpy as np
import time
import openpyxl
import xlwt

urls = []
umamusumes = []
eventdata = []

option = EdgeOptions()
option.use_chromium = True
option.add_argument('--headless')
option.add_argument('disable-gpu')


driver = webdriver.Chrome(
    executable_path=r'msedgedriver.exe', options=option)


driver.get("https://gamewith.jp/uma-musume/article/show/253241")

tableListedByHosi = driver.find_element_by_xpath(
    "//*[@id=\"article-body\"]/div[2]/table")
tbodyListedByHosi = tableListedByHosi.find_element_by_tag_name("tbody")
trListedByHosi = tbodyListedByHosi.find_elements_by_tag_name("tr")
tdListedByHosi = trListedByHosi[1].find_elements_by_tag_name("td")
for td in tdListedByHosi:
    a = td.find_element_by_tag_name("a")
    urls.append(a.get_attribute("href"))

for url in urls:
    print("get <-" + url)
    driver.get(url)
    div_class = driver.find_element_by_xpath(
        "//*[@id=\"article-body\"]/div[1]")
    table = div_class.find_element_by_tag_name("table")
    tbody = table.find_element_by_tag_name("tbody")
    tr = tbody.find_elements_by_tag_name("tr")
    iter = 1
    for data in tr:
        if data == tr[0]:
            continue
        td = data.find_elements_by_tag_name("td")
        a = td[0].find_elements_by_tag_name("a")
        for tagA in a:
            if iter % 2 != 0:
                umamusumes.append(tagA.get_attribute("href"))
            iter = iter + 1

iter = 0
for umamusume in umamusumes:
    print("get <-" + umamusume)
    driver.get(umamusume)
    articleBody = driver.find_element_by_xpath("//*[@id=\"article-body\"]")
    umaChoiceTables = articleBody.find_elements_by_class_name(
        "uma_choice_table")
    for umaChoiceTable in umaChoiceTables:
        table = umaChoiceTable.find_element_by_tag_name("table")
        tbody = table.find_element_by_tag_name("tbody")
        trs = tbody.find_elements_by_tag_name("tr")
        iter2 = 1
        for tr in trs:
            script = tr.find_element_by_tag_name("th")
            eventdata.append(script.text)
            td = tr.find_element_by_tag_name("td")
            temp = td.text.replace("\n", "&")
            eventdata.append(temp)
            eventdata.append(iter)
            eventdata.append(iter2)
            iter2 = iter2 + 1
        iter = iter + 1

suports = []
urls = []
driver.get("https://gamewith.jp/uma-musume/article/show/255035")
table = driver.find_element_by_xpath(
    "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/table")
tbody = table.find_element_by_tag_name("tbody")
trs = tbody.find_elements_by_tag_name("tr")
tr = trs[1]
tds = tr.find_elements_by_tag_name("td")

for td in tds:
    a = td.find_element_by_tag_name("a")
    urls.append(a.get_attribute("href"))

urls2 = []
for url in urls:
    print("get <-" + url)
    driver.get(url)
    tbody = driver.find_element_by_xpath(
        "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/table/tbody")
    trs = tbody.find_elements_by_tag_name("tr")
    for tr in trs:
        if tr == trs[0]:
            continue
        tds = tr.find_elements_by_tag_name("td")
        td = tds[0]
        a = td.find_element_by_tag_name("a")
        urls2.append(a.get_attribute("href"))


for url in urls2:
    print("get <-" + url)
    driver.get(url)
    div = driver.find_element_by_xpath("//*[@id=\"article-body\"]")
    umaChoiceTables = div.find_elements_by_class_name("uma_choice_table")
    for umaChoiceTable in umaChoiceTables:
        table = umaChoiceTable.find_element_by_tag_name("table")
        tbody = table.find_element_by_tag_name("tbody")
        trs = tbody.find_elements_by_tag_name("tr")
        iter2 = 1
        for tr in trs:
            script = tr.find_element_by_tag_name("th")
            eventdata.append(script.text)
            td = tr.find_element_by_tag_name("td")
            temp = td.text.replace("\n", "&")
            eventdata.append(temp)
            eventdata.append(iter)
            eventdata.append(iter2)
            iter2 = iter2 + 1
        iter = iter + 1


npData = np.array(eventdata)
npDataReshaped = npData.reshape(int(len(eventdata) / 4), 4)

df = pd.DataFrame(npDataReshaped, columns=["script", "spec", "iter", "iter2"])
df.to_excel("./character_script_spec.xls")
print("************************")
print("event crawling finished!")
print("************************")


driver.quit()
