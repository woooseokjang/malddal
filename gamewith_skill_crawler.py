from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
import pandas as pd
import numpy as np
import time
import openpyxl
import xlwt
import os
import sys
import urllib.request
import json
import time

with open("./APISETTING.json", 'r') as f:
    json_data = json.load(f)


option = EdgeOptions()
option.use_chromium = True
option.add_argument('--headless')
option.add_argument('disable-gpu')

driver = webdriver.Chrome(
    executable_path=r'msedgedriver.exe', options=option)

driver.get("https://gamewith.jp/uma-musume/article/show/257928")
tbody = driver.find_element_by_xpath(
    "/html/body/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/div/table/tbody")
trs = tbody.find_elements_by_tag_name("tr")

skilldata = []

for tr in trs:
    if tr == trs[0]:
        continue
    tds = tr.find_elements_by_tag_name("td")
    for td in tds:
        if td == tds[0]:
            continue
        temp = td.text.split("\n")
        for t in temp:
            if t == temp[1]:
                client_id = json_data["client_id"]
                client_secret = json_data["client_secret"]
                encText = urllib.parse.quote(t)
                data = "source=ja&target=en&text=" + encText
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(
                    request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode != 200):
                    print("PAPAGO API ERR? -> " + rescode)
                elif(rescode == 200):
                    response_body = response.read()
                    resmess = json.loads(response_body.decode('utf-8'))
                    skilldata.append(
                        resmess['message']['result']['translatedText'])
                    print(resmess['message']['result']['translatedText'])
            if t == temp[0]:
                print(t)
                skilldata.append(t)
            time.sleep(0.11)

npData = np.array(skilldata)
npDataReshaped = npData.reshape(int(len(skilldata) / 2), 2)

df = pd.DataFrame(npDataReshaped, columns=["skillName", "skillInfo"])
df.to_excel("./skill_spec_en.xls")
print("************************")
print("skill crawling finished!")
print("************************")
