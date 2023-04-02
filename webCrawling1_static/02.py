# 2) 이미지/동영상 다운로드 방법을 참고하여 네이버에 "고양이"를 검색한 후,
#이미지 탭에서 고양이 이미지 10개를 저장하는 코드를 작성하고 결과를 제출하세요. 
import requests as rq
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36"} #user-agent 추가를 위한 header
path='./imgs/'
url='https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EA%B3%A0%EC%96%91%EC%9D%B4' #고양이 검색 후 이미지탭 주소

response=rq.get(url, headers=headers) #url 가져오기 + user-agent 추가
# print(response.status_code) 200
html_txt=response.text #text(): response값(html)=>유니코드 형태로 디코드 시킴
soup=bs(html_txt, 'html.parser') #beautifulsoup 객체 생성. html 코드 파싱 목적

# imgs=soup.find_all('img',class_='_image _listImage')# 안 되는 이유?
imgs=soup.select('img', limit=10)  #img 태그를 10개 제한으로 가져옴
# print(soup.prettify())
# print(imgs[0])

n=1 #사진 저장명을 위한 변수 선언
for i in imgs: #각 img에 대한 동작을 위한 반복문
    imgUrl=i['src'] #img들의 src 속성을 가져옴
    with urlopen(imgUrl) as f: 
        #with as: 파일 open후 close 자동 호출
        with open(path+"img"+str(n)+'.jpg','wb') as h: #저장명 선언 후 h로 받아옴
            imgs=f.read() 
            h.write(imgs) #이미지 저장
        n+=1
        # print(imgUrl)

print(len(imgs))
print("FIN!")
    
# linkArr=[]
# n=1
# for i in imgs:
#     linkArr.append(i['src'])
#     print("FIN!")

# j=0
# for k in linkArr:
#     j+=1
#     with open(path+'img'+j+'.jpg','wb')as h:
#         h.write(imgs[j].content)
