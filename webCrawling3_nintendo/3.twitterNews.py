# https://twitter.com/nintendo
# https://topics.nintendo.co.jp/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import urlretrieve
import googletrans as gt

serv=Service('C:/pythontemp/chromedriver')
opt=Options()
opt.add_experimental_option("detach",True) #창 꺼짐을 막는 옵션 추가
opt.add_experimental_option("excludeSwitches",["enable-logging"]) #불필요한 광고 방지 옵션

url='https://topics.nintendo.co.jp/'
# url='https://twitter.com/nintendo'

###크롤링 진행
driver=webdriver.Chrome(service=serv,options=opt)
driver.get(url)
time.sleep(3)

# ###일정 부분 스크롤 : 고치기
# scr=driver.find_element(By.CLASS_NAME,'nc3-c-articleCard__main')
# ac=ActionChains(driver)
# ac.move_to_element(scr).perform()

###토픽 정보 크롤링
transList=[]
topicTitles=driver.find_elements(By.CLASS_NAME,'nc3-c-articleCard__name')
# topicTitles=driver.find_elements(By.CLASS_NAME,'css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')

topicTitles2=[]
i=0
for title in topicTitles:
    topicTitles2.append(title.get_attribute('innerText'))
topicTitles2=list(filter(None,topicTitles2)) #배열 내 None 값 필터링하기
# for title in topicTitles2: for checking type that can be used as JSON
#     print(type(title))

##한국어로 번역하기
for i in range(len(topicTitles2)):
    translator=gt.Translator()
    korean=translator.translate(topicTitles2[i],dest='ko')
    transList.append(korean)
    
for translated in transList:
    print(translated.text)
# print(transList)
print(len(transList))

print(topicTitles2)

driver.quit()