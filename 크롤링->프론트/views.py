import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse  # Response를 전달해 주는 모듈

#import re              #이건 쓸지 모르겠음
#import pandas as pd    #이건 쓸지 모르겠음


def hello(request):
    return HttpResponse("안녕하세요. 링크에 main/을 추가해보시겠어요?")

def crawl():
  contentlist=[]
  a_titlelist=[]
  a_urllist=[]
  url_help = 'https://www.inflearn.com'
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
  for i in range(0,2): #페이지 별로
    url="https://www.inflearn.com/community/studies?page="+str(i+1)+"&order=recent"
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    paragraphs =soup.select('#main > section.community-body > div.community-body__content > div.question-list-container > ul > li') #스터디 모집글 크롤링
     
    for paragraph in paragraphs:
        
      #모집 중 여부
      condition = paragraph.select_one('a > div > div > div.question__title > div > div > span').text.strip()
      if condition!='모집중':
          continue
        
      #스터디 제목
      a_title = paragraph.select_one('a > div > div > div.question__title > h3').text.strip()#
       
      #스터디 모집글
      content = paragraph.select_one('a > div > div > p').text.strip()
         
      #스터디 모집글 링크
      a_url = paragraph.select_one('a').attrs['href']
      #print(condition)
      #print(a_title)
      #print(content)
      #print(url_help+a_url)

      a_titlelist.append(a_title)
      a_urllist.append(url_help+a_url) #이게 안된다면 url+help+a_url으로 하기.
      contentlist.append(content)

    #list=[a_titlelist,a_urllist,contentlist]
    return a_titlelist,a_urllist,contentlist
    #return list


def listingg(request):
    #list = crawl()  #ver1
     a_titlelist,a_urllist,contentlist = crawl()   #ver2

#    context = {'list':list}  #ver1
     context = {'a_titlelist':a_titlelist,'a_urllist':a_urllist,'contentlist':contentlist}
     
     return render(request,'listingg.html',context)
     
