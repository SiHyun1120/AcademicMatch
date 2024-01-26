import pandas as pd
import numpy as np
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv('/content/inflearn_data_ing.csv')
df=df.loc[:,['content','title','url']]
df = df.drop_duplicates(subset=['content'],keep='first').reset_index(drop=True)
print(df)

# 모집글 새로 입력
new_title = input('모집글 제목: ')
new_content = input('모집글 내용: ')
print(new_title +'\n' +new_content) 

# 새로운 제목, 내용 새로운 행으로 추가 
new_row = {'content': new_content, 'title': new_title, 'url': ''}
df = df.append(new_row, ignore_index=True)
print(df)

# 추천 모집글 열 추가
df['Recommended Index'] = ''
print(df)

# TF-IDF
contents = df["content"].tolist()

uni_tfidf = text.TfidfVectorizer()
uni_matrix = uni_tfidf.fit_transform(contents) # 학습
uni_sim = cosine_similarity(uni_matrix)

uni_matrix.toarray().shape
uni_sim.shape

df.iloc[uni_sim[0].argsort()[::-1][1:5], : ]['content']

df.iloc[uni_sim[0].argsort()[::-1][0], : ]['content']

def recommend_articles_index(xx, df):
    a = df.iloc[xx.argsort()[::-1][1:6], :]['content']  # 추천 기사들의 본문들
    b = a.index[df.iloc[xx.argsort()[::-1][0], :]['content'] != a]  # 같은 내용은 추천에서 제외
    return b.tolist()

df['Recommended Index'] = [recommend_articles_index(x, df) for x in uni_sim]

df['title'].iloc

# key값을 새로 추가한 행으로 설정 
k =len(df)-1
print('특정 스터디: \n', df['title'].iloc[k] + '\n'+ df['content'].iloc[k]+ '\n')
print('추천 스터디: \n', df.iloc[df['Recommended Index'][k]][['title','content','url']].values)

#학습셋에 포함되었으므로 다시 삭제하기
df = df.drop(df.index[-1])
print(df)

