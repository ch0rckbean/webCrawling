# 구글 사이트(https://www.google.com/)에서 검색 창에 "코로나"를 검색한 후,동영상 탭에서 한 페이지에 보이는 동영상을 저장하는 코드를 작성하고 결과를 제출하세요. (썸네일이 동영상이 아닌 이미지인 경우는 따로 저장하지 않아도 됩니다.) 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'
from urllib.request import urlretrieve
import time

serv=Service('C:/pythontemp/chromedriver')
opt=Options()
opt.add_experimental_option("detach",True) #창 꺼짐을 막는 옵션 추가
opt.add_experimental_option("excludeSwitches",["enable-logging"]) #불필요한 광고 방지 옵션
opt.add_argument(f'user-agent={userAgent}') #보안 이슈를 피하기 위한 userAgent 추가

url='https://www.google.co.kr/search?q=%EC%BD%94%EB%A1%9C%EB%82%98&sxsrf=APwXEdeQtOWJfCCrf2oN6QxkU5c5A4sLEQ:1680518337829&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmjcLUwo3-AhWPC94KHarBCZUQ_AUoA3oECAEQBQ&biw=638&bih=560&dpr=1.5' #코로나 검색 후 동영상 탭 링크
driver=webdriver.Chrome(service=serv, options=opt) #웹드라이버로 창을 엶
driver.get(url) #url로 이동

time.sleep(10) #동영상 로딩을 기다리는 시간

xpath_list=driver.find_elements(By.XPATH,'//div[@class="VYkpsb"]/video') #동영상을 포함하는 div의 클래스를 명시하는 xpath 찾기
# video_list=driver.find_elements(By.TAG_NAME,('video')) #동작 x
a_list=driver.find_elements(By.TAG_NAME,'a') #a 태그를 찾음
iframe_list=driver.find_elements(By.TAG_NAME,('iframe')) #동영상을 포함한 iframe 요소를 찾음
# class_list=driver.find_elements(By.CLASS_NAME,('DqfBw')) #동작 x

#의문점
#왜 CLASS_NAME/TAG_NAME 으로 하면 video를 못 받아오는지
#비디오를 왜 다 못 가져오는지
#왜 비디오가 재생 안 되는지
#왜 비디오가 중복으로 크롤링 되는지

url_list=[] #영상의 src를 저장할 리스트 선언
for xpath in xpath_list: #xpath로 가져온 요소들만큼 반복문이 돎
    src = xpath.get_attribute('src') #xpath 내 src 가져옴
    if src: #src라면
        url_list.append(src) #리스트에 저장
        
for a in a_list: #a 태그로 가져온 요소들만큼 반복문이 돎
    href=a.get_attribute('href') #a 태그의 링크를 걸어주는 href 찾기
    if href and (href.startswith("https://www.youtube.com") or href.startswith("https://youtu.be")):
        url_list.append(href) #href이고, 해당 링크로 href가 시작한다면 리스트에 href 추가
        
for iframe in iframe_list: #iframe으로 요소를 가져온만큼 반복문이 돎 
    driver.switch_to.frame(iframe) # 해당 iframe으로 전환
    time.sleep(10) #iframe으로의 전환을 기다리는 시간
    iframeVdo_list = driver.find_elements(By.TAG_NAME, 'video') # iframe 내부에서 video 태그 찾기 
    
    for iframeVdo in iframeVdo_list: #iframe 내 video에서 반복문 실행
        src = iframeVdo.get_attribute('currentSrc') 
        #iframe 내 video에서 currentSrc 찾기. currentSrc: 현 비디오의 src 반환. 빈 속성이라면, 빈 값 반환
        if src: #src라면
            url_list.append(src) #리스트에 추가
    driver.switch_to.default_content()  #원래 페이지로 돌아옴
       
# for classes in class_list:
#     src = classes.get_attribute('src')
#     if src:
#         url_list.append(src)
                  

folder_path='./videos/' #동영상을 저장할 경로

#참고용
print("len-url",len(url_list))
print("url",url_list)

i=0 #저장명을 위한 정수 변수
for link in (url_list): #위 과정들을 통해 저장한 리스트 내 link만큼 반복문이 돎
    i+=1 #저장명 1씩 증가
    urlretrieve(link,folder_path+f'{i}.mp4') #(링크, 저장명.확장자)
    print(i) #참고용
    
driver.quit() #드라이버 종료