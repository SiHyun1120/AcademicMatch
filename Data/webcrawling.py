import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

contentlist=[]

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for i in range(0,10): #페이지 별로
  url="https://www.inflearn.com/community/studies?page="+str(i+1)+"&order=recent"
  data = requests.get(url,headers=headers)

  soup = BeautifulSoup(data.text, 'html.parser')
  paragraphs =soup.select('#main > section.community-body > div.community-body__content > div.question-list-container > ul > li') #스터디 모집글 크롤링

  for paragraph in paragraphs:
    #P태그 안 본문 내용만 출력하도록!!!!
    content = paragraph.select_one('a > div > div > p').text.strip()

    #태그를 가져오기 때문에 
    print(content)
    contentlist.append(content)


# dataframe으로 변환
df=pd.DataFrame()
df["content"] =contentlist
print(df.head(5))

df.to_csv("test.csv", encoding = "utf-8-sig")
