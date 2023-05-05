from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

serv=Service('C:/pythontemp/chromedriver') #크롬드라이버 객체 생성
opt=Options() #옵션 추가하기 위한 객체 생성
opt.add_experimental_option("detach",True) #창 꺼짐을 막는 옵션 추가
opt.add_experimental_option("excludeSwitches",["enable-logging"]) #불필요한 광고 방지 옵션

url='https://www.nintendo.co.kr/software/switch/index.php' #크롤링 할 페이지

driver=webdriver.Chrome(service=serv, options=opt) #크롬창 열기
driver.get(url) #url을 읽어옴

time.sleep(3) #로딩 시간 주기

moreBtn=driver.find_element(By.CLASS_NAME,('btn_softwareAllView')).send_keys(Keys.ENTER) #SW 전체 보기 버튼 클릭

### 게임 정보로 스크롤
scr=driver.find_elements(By.XPATH,'//*[@id="switem20"]/p[1]') #스크롤해 내려갈 요소 선언
ac=ActionChains(driver) 
ac.move_to_element(scr[13]).perform() #스크롤 하기
# driver.execute_script("window.scrollTo(0,window.innerHeight/2)")

###게임 정보 크롤링
# 1.이름
nameList2=[] #이름 text를 읽어와 저장할 빈 배열 선언
nameList1=driver.find_elements(By.CLASS_NAME,'tit') #tit class의 모든 요소를 가져와 리스트를 만듦
for name in nameList1: #리스트 내 요소마다
    nameList2.append(name.get_attribute('innerText')) #text를 읽어와 배열에 추가
# print(nameList2[:3])
    
# 2.이미지 링크 
srcList=[] #이미지 링크를 읽어와 저장할 빈 배열 선언 
imgList=driver.find_elements(By.XPATH,'//*[@id="switem20"]/a/img')
for img in imgList: #읽어온 이미지마다
    src=img.get_attribute('src') #src요소를 찾아서
    srcList.append(src) #빈 배열에 추가
# print("src: ",srcList) 
   
# 3.제작사
compList2=[] #제작사 정보를 읽어와 저장할 빈 배열 선언
compList1=driver.find_elements(By.CLASS_NAME,'releaseInfo') #이 요소에는 발매일 + 제작사 정보가 함께 있으므로
for comp in compList1: # 요소마다
    compList2.append(comp.get_attribute('innerText')[12:]) #발매 연도 + 월 + 일 후부터 슬라이싱 해 추가
# print("comp: ",compList2[:3])

# 4.발매일  
dateList2=[]
dateList1= driver.find_elements(By.CLASS_NAME,'releaseInfo') 
for date in dateList1:
    dateList2.append(date.get_attribute('innerText')[:10]) #발매 연도 + 월 + 일까지 슬라이싱 해 추가
# print("date: ",dateList2[:3])

# # 5.발매 타입 : 다운로드 / 패키지 /체험판 여부
# typeList2=[] #요소의 text를 저장할 배열 
# idxList=[] #슬라이싱을 위한 인덱스 배열
# resList=[] #슬라이싱을 적용한 결과 배열
# start=0 #슬라이싱 시작 기준이 되는 변수
# typeList1=driver.find_elements(By.CLASS_NAME,'ico_rel') #첫번째 배열에 요소들을 넣어줌

# for type in typeList1: #요소마다
#     typeList2.append(type.get_attribute('innerText')) #text를 읽어와 두번째 배열에 추가
# for i in range(len(typeList2)): #text마다
#     typeList2=sorted(typeList2[i])
#     if (typeList2[i])=='DL'  : #모든 게임은 DL + (optional) PK, 체험판 형태로 배포되므로 DL 기준으로 슬라이싱 할 것
#         idxList.append(i) #DL이 나온다면 다음 게임인 것. => 인덱스 리스트엔 DL의 인덱스(다음 게임의 기준이 되는 정보)가 담김
# if typeList2[-1]=='DL' or typeList2[-1]=='체험판': # 마지막 발매 타입이 DL이라면
#     idxList.append(len(typeList2)-1) #인덱스 리스트에 마지막 게임의 인덱스 추가
# for idx in idxList:
#     if idx >= start: #인덱스가 시작 변수보다 크거나 같다면
#         resList.append(typeList2[start:idx+1]) #시작부터 인덱스 +1 까지 슬라이싱(DL인 인덱스 전까지)
#         start=idx+1 #시작 변수를 인덱스 다음으로 재선언 해야 중복이 안 일어남
        
# if start < len(typeList2): #시작 변수가 총 발매 타입이 담긴 리스트의 길이보다 적다면 == 아직 슬라이싱 할 게 남았다면 + 더 이상 리스트에 DL이 없이 PK | 체험판이라면
#     resList.append(typeList2[start:]) #나머지를 각각 슬라이싱 해 추가

driver.quit()
# print(nameList2, len(nameList2))
# print(compList2,len(compList2))
# print(dateList2,len(dateList2))
# print(srcList,len(srcList))
    
### csv 형태로 저장
datas=pd.DataFrame( #pandas를 통해 col : row 형식의 데이터 프레임을 만듦
    {
        "타이틀": nameList2,
        "제작사": compList2,
        "이미지링크": srcList,
        "발매일": dateList2,
        # "발매 타입": resList
    }
)
# print(datas.head(3))
datas.to_csv(".\\csv\\1.gameInfo.csv",encoding='utf-8-sig') # to_csv(저장경로/저장명.확장자, 인코딩)