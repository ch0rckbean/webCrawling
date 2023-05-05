from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import urlretrieve
# https://www.youtube.com/channel/UCkH3CcMfqww9RsZvPRPkAJA

userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'
serv=Service('C:/pythontemp/chromedriver')
opt=Options()
opt.add_experimental_option("detach",True)
opt.add_experimental_option("excludeSwitches",["enable-logging"]) 
opt.add_argument(f'user-agent={userAgent}') #보안 이슈를 피하기 위한 userAgent 추가

url='https://www.nintendo.co.jp/'

driver=webdriver.Chrome(service=serv, options=opt)
driver.get(url)
# time.sleep(2)

###스크롤 내리기
scr=driver.find_element(By.CLASS_NAME, 'nc3-c-gfooter-sitemap__mainCat')
ac=ActionChains(driver)
ac.move_to_element(scr).perform()

###닌텐도 공식 SNS 버튼 중 유튜브 버튼 클릭
ytbBtn=driver.find_element(By.XPATH,'//*[@id="nc3-c-gfooter"]/div[2]/div[1]/ul/li[2]/a').send_keys(Keys.ENTER)
# ytbHref=ytbBtn.get_attribute('href')
# script=f"window.open(`{ytbHref}`);"
# driver.execute_script(script)

###유튜브 링크 버튼 클릭
socialBtns=driver.find_elements(By.CLASS_NAME,'local-social__contentColLink')

hrefList=[]
for btns in socialBtns:
    hrefs=btns.get_attribute('href')
    hrefList.append(hrefs)
# hrefList=set(hrefList) #순서 변경 되서 쓰면 안 됨
# print(hrefList)
# print(len(hrefList))
    
#원래 아래 구문들은 위 for문 안에 있었으나, driver.get으로 유튜브를 열어도 for문이 계속 돌아 element is not attaged to the page document 에러가 발생 
ytbhrefList=[]
for href in hrefList:
    if "youtube" in href:
        # while "youtube" in href:
        ytbhrefList.append(href)
# set(ytbhrefList) 순서 변경돼서 쓰면 안 됨
driver.get(ytbhrefList[0])
time.sleep(2)
# print("url: ",ytbhrefList[0])
# socialBtn.send_keys(Keys.ENTER)
# socialBtns[53].send_keys(Keys.ENTER)

###youtube 공식 계정 페이지 접속
for i in range(0,2): #스크롤:유튜브는 끝까지 내려야 함
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        # actions.send_keys(Keys.END).perform()

###비디오 링크 읽어오기
##1.href 읽어오기(각 비디오의 재생 페이지)
vdoBoxList=driver.find_elements(By.CLASS_NAME,'yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail') 
hrefList=[]
# print(vdoBoxList)
i=0
for vdoBox in vdoBoxList:
    vdoHref=vdoBox.get_attribute('href')
    if vdoHref:
        hrefList.append(vdoHref)
    i+=1
    if i==3: #개수 맞추기: 이슈
        break
print("url: ",hrefList)
print(len(hrefList))

##2.각 비디오의 재생 페이지로 이동: driver.get(href)로 모든 href를 여는 것은 비효율적
for i,href in enumerate(hrefList):
    script=f"window.open('{href}');"
    driver.execute_script(script)
    
#모든 영상 페이지가 열릴 때까지 대기
while len(driver.window_handles)<=len(hrefList): 
    #driver.window_handles: 프로세스상 열려있는 모든 창 리턴/ 참고 링크: https://velog.io/@exoluse/python-14.-Selenium-%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80-%EC%A1%B0%EC%9E%91
    # => 열려있는 창이 href의 전체 리스트보다 작으면 pass
    pass

#3.각 영상 페이지에서 vdoBox 내 src 추출
srcList=[]
for i,handle in enumerate(driver.window_handles):
    driver.switch_to.window(handle)
    vdoBox=driver.find_elements(By.CLASS_NAME,'video-stream.html5-main-video')
    for vdo in vdoBox:
        srcList.append(vdo.get_attribute('src'))

    ##video title 읽어오기 : 빈 값 + 갯수 맞추기 이슈
    vdoTitle=driver.find_elements(By.ID,'title')
    for title in vdoTitle: #영상 제목을 받아올 코드
        # print(title)
        araLb=title.get_attribute('innerText')
        print("ara: ",araLb) 
srcList=list(filter(None,srcList))
print("srcList1: ",srcList)    
###동영상 저장하기
folder_path='./video/' #동영상을 저장할 경로

# i=0
#urllib의 HTTP404 에러 막기 위해 src 내 불필요한 문자열 제거
for i in range(len(srcList)):
    srcList[i]=srcList[i].strip("blob:")
    urlretrieve(srcList[i],folder_path+f'{i}.mp4')

print("srcList2: ",srcList)    

###동영상 저장하기
    # i+=1
    # urlretrieve(src,folder_path+f'{i}.mp4')
    # # print(i)
    # print(src)
    # if i==10:
    #     break

driver.quit()