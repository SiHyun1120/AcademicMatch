#REST_FRAMEWORK TEST
from rest_framework import viewsets
from myapp.serializers import RecommendSerializer
from myapp.models import RecommendModel
#============ML TEST ===================
import os 
import pickle
import numpy as np
import pandas as pd
from django.conf import settings
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity


from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

topics =[]

def main(request):
    context={}
    return render(request, 'myapp/main.html', context)


def listing(request):
    context = {}
    return render(request, 'myapp/listing.html', context)

@csrf_exempt 
def searching(request):
    return render(request, '/searching.html')
    '''if request.method =='GET':
        context = {}
        return render(request, 'myapp/search.html', context)

    else :
        topics.append({'title':request.POST['title'],'body':request.POST['body']})     

        return redirect('/result/')'''
        

def result(request):
    input_title = request.GET('input_title')
    print(input_title)
    class Recommend(views.APIView):
        def post(self,request):

            #크롤링 데이터 불러오기
            path= os.path.join(settings.MODEL_ROOT,'inflearn_data_ing.csv')
            df=pd.read_csv(path)
            df = df.drop_duplicates(subset=['content'],keep='first').reset_index(drop=True)

            try:
                #사용자가 보낸 데이터 받기
                new_title = request.data.pop('title')
                new_content = request.data.pop('content')

                new_row ={'content':new_content,'title':new_title}

                # TF-IDF
                contents = df["content"].tolist()

                uni_tfidf = text.TfidfVectorizer()
                uni_matrix = uni_tfidf.fit_transform(contents) # 학습
                uni_sim = cosine_similarity(uni_matrix)


                #추천 시스템
                def recommend_articles_index(xx, df):
                    a = df.iloc[xx.argsort()[::-1][1:6], :]['content']  # 추천 기사들의 본문들
                    b = a.index[df.iloc[xx.argsort()[::-1][0], :]['content'] != a]  # 같은 내용은 추천에서 제외
                    return b.tolist()

                df['Recommended Index'] = [recommend_articles_index(x, df) for x in uni_sim]
                
                k =len(df)-1
                predictions=df.iloc[df['Recommended Index'][k]][['title','content','url']].values
                context = {'predictions' : predictions}
            except Exception as err:
                return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
            
            return Response(predictions,status =status.HTTP_200_OK)

    
    '''global topics

    article=''
    for topic in topics:
        article+=f'<h1>{topic["title"]}</h1>{topic["body"]}'
'''

#크롤링 - listing에 데이터 띄우기

from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

def crawl_inflearn():
    # 크롤링 코드 여기에 추가
    contentlist = []
    a_titlelist = []
    a_urllist = []
    url_help = 'https://www.inflearn.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    for i in range(0, 2):  # 페이지 별로
        url = "https://www.inflearn.com/community/studies?page=" + str(i + 1) + "&order=recent"
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        paragraphs = soup.select(
            '#main > section.community-body > div.community-body__content > div.question-list-container > ul > li')
        for paragraph in paragraphs:
            condition = paragraph.select_one(
                'a > div > div > div.question__title > div > div > span').text.strip()
            if condition != '모집중':
                continue
            a_title = paragraph.select_one('a > div > div > div.question__title > h3').text.strip()
            content = paragraph.select_one('a > div > div > p').text.strip()
            a_url = paragraph.select_one('a').attrs['href']
            a_titlelist.append(a_title)
            a_urllist.append(url_help + a_url)
            contentlist.append(content)

    return a_titlelist, a_urllist, contentlist


def listing(request):
    a_titlelist, a_urllist, contentlist = crawl_inflearn()

    # zip 함수를 사용하여 데이터를 묶음
    zipped_data = zip(a_titlelist, a_urllist, contentlist)

    context = {'zipped_data': zipped_data}
    return render(request, 'listing.html', context)
     
