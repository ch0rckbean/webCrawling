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
opt.add_experimental_option("detach",True)
opt.add_experimental_option("excludeSwitches",["enable-logging"])
opt.add_argument(f'user-agent={userAgent}')

url='https://www.google.co.kr/search?q=%EC%BD%94%EB%A1%9C%EB%82%98&sxsrf=APwXEdeQtOWJfCCrf2oN6QxkU5c5A4sLEQ:1680518337829&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmjcLUwo3-AhWPC94KHarBCZUQ_AUoA3oECAEQBQ&biw=638&bih=560&dpr=1.5'
driver=webdriver.Chrome(service=serv, options=opt)
driver.get(url)
time.sleep(2)

ele_list=driver.find_elements(By.TAG_NAME,'a')
# el_list=driver.find_elements(By.CSS_SELECTOR,('#_0hUsZJQjqdzaug-Io4_YCw_24 > div > video'))
#왜 CLASS_NAME으로 하면 video를 못 받아오는지
#비디오를 왜 4개만 가져오는지
#왜 비디오가 재생 안 되는지
# print(el_list)

url_list=[]
for ele in ele_list:
    href=ele.get_attribute('href')
    if href and (href.startswith("https://www.youtube.com") or href.startswith("https://youtu.be")):
        url_list.append(href)
        
# for el in el_list:
#     href2=ele.get_attribute('src')
#     if href2 and href2.startswith("https://"):
#         url_list.append(href2)
folder_path='./videos/'

print(len(url_list))
print(url_list)

i=0
for link in (url_list):
    i+=1
    urlretrieve(link,folder_path+f'{i} .mp4')
    print(i)
    
driver.quit()