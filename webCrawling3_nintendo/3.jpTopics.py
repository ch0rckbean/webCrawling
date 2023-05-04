# https://topics.nintendo.co.jp/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import googletrans as gt
import pandas as pd

serv=Service('C:/pythontemp/chromedriver')
opt=Options()
opt.add_experimental_option("detach",True) #창 꺼짐을 막는 옵션 추가
opt.add_experimental_option("excludeSwitches",["enable-logging"]) #불필요한 광고 방지 옵션

url='https://topics.nintendo.co.jp/'

###크롤링 진행
driver=webdriver.Chrome(service=serv,options=opt)
driver.get(url)
time.sleep(3)

# ###일정 부분 스크롤 
scr=driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[6]/div/a/div[1]/div')
ac=ActionChains(driver)
ac.move_to_element(scr).perform()

###토픽 정보 크롤링
topicTitles=driver.find_elements(By.CLASS_NAME,'nc3-c-articleCard__name') #토픽 정보를 담은 webElements를 넣을 리스트

topicTitles2=[] #토픽 정보를 담은 webElement에서 문자열을 가져와 담을 리스트
for title in topicTitles:
    topicTitles2.append(title.get_attribute('innerText')) #각 webElement에서 문자열을 가져옴
topicTitles2=list(filter(None,topicTitles2)) #배열 내 None 값 필터링하기 
topicTitles2=list(set(topicTitles2))
# for title in topicTitles2: for checking type that can be used as JSON
#     print(type(title))

###한국어로 번역하기: googletrans library 사용
transList=[]  #번역 결과를 넣을 리스트
for i in range(len(topicTitles2)): #토픽 정보만큼
    translator=gt.Translator() #번역기 객체 생성('2.exceptions.ProtocolError: Invalid input ConnectionInputs.RECV_PING in state ConnectionState.CLOSED' 에러가 나므로 반복문 내에서 번역 시마다 번역기 객체 생성)
    korean=translator.translate(topicTitles2[i],dest='ko') #한국어로 번역
    transList.append(korean) #변역 결과 리스트에 번역 결과 추가
    
# for translated in transList: 
for i in range(len(transList)): #변역 결과 리스트 내 변역 결과마다: 배열 내 요소 대체 위해 변수(윗줄) 대신 인덱스 사용
    transList[i]=transList[i].text #text로 바꿔 대체함
# print(transList) #변역 결과 리스트 최종 확인
# # print(len(transList))

###토픽 업로드 날짜 크롤링
dateList=[]
dates=driver.find_elements(By.CLASS_NAME,'nc3-c-articleCard__dateAndPrice')

for date in dates:
    dateTxt=date.get_attribute('innerText')
    if dateTxt:
        dateList.append(dateTxt)
# print(dateList)

driver.quit()

###csv 형태로 저장
datas=pd.DataFrame(
    {
        "토픽 제목": topicTitles2,
        "번역 결과": transList,
        # "업로드 날짜": dateList
    }
)
# print(datas.head(3))
datas.to_csv(".\\csv\\3.jpTopics.csv",encoding='utf-8-sig') #to_csv(저장경로/저장명.확장자, 인코딩)