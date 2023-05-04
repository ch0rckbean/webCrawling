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

#스크롤 내리기
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
ytbUrlList=[]
for href in hrefList:
    if "youtube" in href:
        # while "youtube" in href:
        ytbUrlList.append(href)
# set(ytbUrlList) 순서 변경돼서 쓰면 안 됨
driver.get(ytbUrlList[0])
time.sleep(2)
# print("url: ",ytbUrlList[0])
# socialBtn.send_keys(Keys.ENTER)
# socialBtns[53].send_keys(Keys.ENTER)

###youtube 공식 계정 페이지 접속
for i in range(0,2): #스크롤:유튜브는 끝까지 내려야 함
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        # actions.send_keys(Keys.END).perform()

###비디오 링크 읽어오기
vdoList=driver.find_elements(By.CLASS_NAME,'yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail') 
urlList=[]
# print(vdoList)
for vdo in vdoList:
    vdoHref=vdo.get_attribute('href')
    if vdoHref:
        urlList.append(vdoHref)
print("url: ",urlList)
print(len(urlList))

###동영상 저장하기
folder_path='./video/' #동영상을 저장할 경로

i=0
for link in urlList:
    i+=1
    urlretrieve(link,f'{i}.mp4')
    if i==10:
        break
print(i)
import os
cwd=os.getcwd()
os.chdir(cwd+'/webCrawling3_nintendo/')
print(os.getcwd())
# ###video title 읽어오기 : 작동 x
# vdoTitle=driver.find_elements(By.ID,'video-title')
# for title in vdoTitle: #영상 제목을 받아올 코드
#     # print(title)
#     araLb=title.get_attribute('title')
# print("ara: ",araLb)

driver.quit()