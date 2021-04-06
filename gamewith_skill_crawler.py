from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
import pandas as pd
import numpy as np
import time
import openpyxl
import xlwt

option = EdgeOptions()
option.use_chromium = True
option.add_argument('--headless')
option.add_argument('disable-gpu')

driver = webdriver.Chrome(
    executable_path=r'msedgedriver.exe', options=option)

driver.get("https://gamewith.jp/uma-musume/article/show/257928")
skillTable = driver.find_element_by_xpath(
    "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div/table")
tbody = skillTable.find_element_by_tag_name("tbody")
trs = tbody.find_elements_by_tag_name("tr")

skilldata = []

for tr in trs:
    if tr == trs[0]:
        continue
    tds = tr.find_elements_by_tag_name("td")
    for td in tds:
        skilldata.append(td.text)

npData = np.array(skilldata)
npDataReshaped = npData.reshape(int(len(skilldata) / 2), 4)

df = pd.DataFrame(npDataReshaped, columns=["skillName", "skillInfo"])
df.to_excel("./skill_spec.xls")
print("************************")
print("skill crawling finished!")
print("************************")
