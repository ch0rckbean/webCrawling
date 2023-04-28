from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time

serv=Service('C:/pythontemp/chromedriver')
opt=Options()
opt.add_experimental_option("detach",True)
opt.add_experimental_option("excludeSwitches",["enable-logging"])

url='https://www.nintendo.co.kr/software/switch/index.php'

driver=webdriver.Chrome(service=serv, options=opt)
driver.get(url)

time.sleep(3)

moreBtn=driver.find_element(By.CLASS_NAME,('btn_softwareAllView')).send_keys(Keys.ENTER) #SW 전체 보기

# 게임 정보로 스크롤
scr=driver.find_elements(By.XPATH,'//*[@id="switem20"]/p[1]')
ac=ActionChains(driver)
ac.move_to_element(scr[13]).perform()
# driver.execute_script("window.scrollTo(0,window.innerHeight/2)")

###SW 정보 크롤링

# 1.이름
nameList2=[]
nameList1=driver.find_elements(By.CLASS_NAME,'tit')
for name in nameList1:
    nameList2.append(name.get_attribute('innerText'))
print(nameList2[:3])

# 2.이미지 링크 
srcList=[]
imgList=driver.find_elements(By.XPATH,'//*[@id="switem20"]/a/img')
for img in imgList:
    src=img.get_attribute('src')
    srcList.append(src)
print("src: ",srcList[4]) 
   
# 3.제작사
compList2=[]
compList1=driver.find_elements(By.CLASS_NAME,'releaseInfo')
for comp in compList1:
    compList2.append(comp.get_attribute('innerText')[12:])
print("comp: ",compList2[:3])

# 4.발매일  //*[@id="switem20"]/p[2]/text()[1] //*[@id="switem20"]/p[2]/text()[2]
dateList2=[]
dateList1= driver.find_elements(By.CLASS_NAME,'releaseInfo')
for date in dateList1:
    dateList2.append(date.get_attribute('innerText')[:10])
print("date: ",dateList2[:3])

# 5.발매 타입 : 다운로드 / 칩 여부
typeList2=[]
idxList=[]
resList=[]
start=0
typeList1=driver.find_elements(By.CLASS_NAME,'ico_rel')

for type in typeList1:
    typeList2.append(type.get_attribute('innerText'))
for i in range(len(typeList2)):
    if (typeList2[i])=='DL':
        idxList.append(i)
if typeList2[-1]=='DL':
    idxList.append(len(typeList2)-1)
for idx in idxList:
    if idx >= start:
        resList.append(typeList2[start:idx+1])
        start=idx+1
if start < len(typeList2):
    resList.append(typeList2[start:])

print(idxList)
print(resList)
print(len(resList))
print(len(nameList2))
# print("type: ",typeList2)
    

###3. csv 형태로 저장
datas=pd.DataFrame(
    {
        "타이틀": nameList2,
        "제작사": compList2,
        "발매일": dateList2,
        "이미지 링크": srcList,
        "발매 타입": resList
    }
)
driver.quit()
print(datas.head(3))
datas.to_csv("C:\pythontemp\VentureStartup\webCrawling3_nintendo\gameInfo.csv",encoding='utf-8-sig')
