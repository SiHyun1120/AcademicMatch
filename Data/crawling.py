import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

contentlist=[]

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for i in range(0,2): #페이지 별로
  url="https://www.inflearn.com/community/studies?page="+str(i+1)+"&order=recent"
  data = requests.get(url,headers=headers)

  soup = BeautifulSoup(data.text, 'html.parser')

  paragraphs =soup.select('#main > section.community-body > div.community-body__content > div.question-list-container > ul > li') #스터디 모집글 크롤링


  for paragraph in paragraphs:
    url_help = 'https://www.inflearn.com'

    #모집 중 여부
    condition = paragraph.select_one('a > div > div > div.question__title > div > div > span').text.strip()
    
    if(condition!='모집중'):
      continue
    #스터디 제목
    a_title = paragraph.select_one('a > div > div > div.question__title > h3').text.strip()
    
    #스터디 모집글
    content = paragraph.select_one('a > div > div > p').text.strip()
    
    #스터디 모집글 링크
    a_url = paragraph.select_one('a').attrs['href']


    print(condition)
    print(a_title)
    print(content)
    print(url_help+a_url)

    #NLP 분들은 이 부분부터 수정하시면 될것 같아요.
    contentlist.append(content)


# dataframe으로 변환
df=pd.DataFrame()
df["content"] =contentlist
print(df.head(5))

df.to_csv("test.csv", encoding = "utf-8-sig")