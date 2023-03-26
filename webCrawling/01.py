# 1) 해당 링크에 있는 내용을 따라 간단한 네이버 뉴스 크롤링 코드를 작성하고 결과를 제출하세요.
import requests as rq
from bs4 import BeautifulSoup as bs

#url 변수에 크롤링 할 웹 주소를 저장
url= 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EC%A0%A4%EB%8B%A4+%EC%8B%A0%EC%9E%91&oquery=%EB%8B%8C%ED%85%90%EB%8F%84&tqi=itJhJsp0JXVssZk1q%2F8ssssst40-319430'

response= rq.get(url) #url 요청해 response 변수에 담음
# print(response.url)
html_txt= response.text #text(): response값(html)=>유니코드 형태로 디코드 시킴
# print(response.text)

soup=bs(html_txt,'html.parser') #beautifulsoup 객체 생성. html 코드 파싱 목적
print(soup.select_one('a.news_tit').get_text())
#get_text: 1개의 html 태그에만 사용 가능
#select_one: 가장 처음 나오는 것 하나만 선택
#텍스트를 추출하고 싶은 html 요소 1개 선택

print('\n<SELECT from now on>') #구분자
titles=soup.select('a.news_tit') #해당 클래스 이름을 가진 모든 요소 선택

#get_text함수는 1개의 html 태그에만 사용 가능 => 
#반복문 통해 1 by 1으로 가져오기
for i in titles: 
    title=i.get_text()
    print(title)