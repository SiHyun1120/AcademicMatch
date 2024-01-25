import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity

#======================= 데이터 업로드 및 전처리 ======================
df=pd.read_csv('Data\datafile\data_inflearn.csv')

df=df.loc[:,['content','tags']]
df = df.drop_duplicates(subset=['content'],keep='first').reset_index(drop=True)
df['Recommended Index'] = ''

# ================ 단어 빈도수를 통해 유사한 스터디 모집글 분류 =============

# ====== 모델 학습 ======
contents = df["content"].tolist()

uni_tfidf = text.TfidfVectorizer()
uni_matrix = uni_tfidf.fit_transform(contents) 
uni_sim = cosine_similarity(uni_matrix)

#========모델 저장=========
with open('uni_tfidf_model.pkl', 'wb') as tfidf_file:
    pickle.dump(uni_tfidf, tfidf_file)

with open('uni_sim_matrix.pkl', 'wb') as sim_file:
    pickle.dump(uni_sim, sim_file)

# ===== 유사한 모집글 분류 작업 =====
def recommend_articles_index(xx): # 분류 함수
        a = df.iloc[xx.argsort()[::-1][1:6], : ]['content'] # 추천 기사들의 본문들

        b = a.index[(df.iloc[xx.argsort()[::-1][0], :]['content'] != a) ] # 같은 내용은 추천에서 제외

        return b.tolist()

df['Recommended Index'] = [recommend_articles_index(x) for x in uni_sim]

# ======= 결과 도출 ========
k=1260
print('특정 스터디: \n', df['tags'].iloc[k] + '\n')
print('추천 스터디: \n', df.iloc[df['Recommended Index'][k]][['tags','content']].values)