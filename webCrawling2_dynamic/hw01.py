# 이미지/동영상 다운로드 방법을 참고하여 네이버에 "고양이"를 검색한 후,이미지 탭에서 고양이 이미지 10개를 저장하는 코드를 작성하고 결과를 제출하세요. 

# https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el
#https://hobbylists.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-findelement%EC%9D%98-InvalidArgumentException-NoSuchElementException-%EC%97%90%EB%9F%AC-%EC%9D%B4%EC%8A%88-%EA%B4%80%EB%A0%A8
# https://goddino.tistory.com/353 option설명

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Service: 다음 기능들을 실행하는 모듈
# - chromedriver 실행/중지 + 백그라운드에서 따로 실행되도록
# - 크롬드라이버 경로 특정
serv=Service('C:/pythontemp/chromedriver') 
# 크롬드라이버 서비스 객체 생성

opt=Options() #셀레니움 기본 설정을 위한 객체 생성(여기선 창 실행되자마자 꺼지지 않도록 하기 위해 사용)
opt.add_experimental_option("detach",True) #브라우저 꺼짐 방지 코드
opt.add_experimental_option("excludeSwitches",["enable-logging"]) #불필요한 에러 메시지 제거

import time
url='https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EA%B3%A0%EC%96%91%EC%9D%B4'
driver=webdriver.Chrome(service=serv, options=opt) #크롬 드라이버 객체 생성
driver.get(url) #웹 페이지로 이동
time.sleep(3) #프로세스 3초간 일시 정지

ele_thumbnail= driver.find_elements(By.CLASS_NAME,'_image._listImage') 
#웹페이지 이동 후 해당 아이디를 가진 요소들을 찾아 ele_thumbnail에 저장
    
url_thumbnail=[] #빈 리스트 선언 

for img in ele_thumbnail: #찾은 요소==해당 아이디를 가진 img마다 
    url_thumbnail.append(img.get_attribute('src')) #src == img를 빈 리스트에 저장

folder_path='./imgs/' #img를 저장할 경로

from urllib.request import urlretrieve
#urllib: url을 가져오기 위한 모듈
#urlretrieve: 해당 함수를 통해 바로 파일에 자료 입력 가능

i=0 #img 저장 이름을 위한 변수

for src in url_thumbnail: #저장 된 src마다
    i+=1
    urlretrieve(src,folder_path+f'{i}.jpg')
    #urlretrieve(url, filename)
    print(i)
    if(i==10): #10개까지만 저장하기 위해
        break

driver.quit()