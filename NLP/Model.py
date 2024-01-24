# 형태소 분석기 Mecab 설치
!pip install konlpy
!pip install mecab-python
!bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

!pip install --upgrade pip
!pip install --upgrade numpy

import pandas as pd
from konlpy.tag import Mecab
from gensim.models.doc2vec import TaggedDocument
from tqdm import tqdm

df = pd.read_csv('/content/data_inflearn_addTitle.csv',  sep=',')
df = df.dropna()
df

#직접 불용어 사전 제작.

#불용어 사전
stop_words = "안녕 하 세요 ~ / ? % ( ) & -  , : . https open kakao '하 있 습니다 은 는 이 가 을 를 의  합니다 하는 할 하고 한다 그리고 입니다 그 등 이런 것 및 제 더 되 었 는데 하 면 봅니다 에 대한 으신 한 와 과 으면 것 같 아요 기  + 적 에서 고 서 만큼 지 지만 면서 고자 으로 더라도 나 그런 이왕 아서 해 으나 자 라도 위 시 니까요"

stop_words = set(stop_words.split(' '))

#토큰화하고 불용어 제거 전 
mecab = Mecab()

tagged_corpus_list = []

for index, row in tqdm(df.iterrows(), total=len(df)):
  text = row['content']
  tag = row['tags']

  result = [word for word in mecab.morphs(text) if not word in stop_words]
  tokens = TaggedDocument(tags=[tag], words=result)

  #토큰화하고 불용어 제거 후
  tagged_corpus_list.append(tokens)

print('문서의 수 :', len(tagged_corpus_list))

from gensim.models import doc2vec

model = doc2vec.Doc2Vec(vector_size=300, alpha=0.025, min_alpha=0.025, workers=8, window=8)

# Vocabulary 빌드
model.build_vocab(tagged_corpus_list)
print(f"Tag Size: {len(model.docvecs)}", end=' / ')

# Doc2Vec 학습
model.train(tagged_corpus_list, total_examples=model.corpus_count, epochs=50)

# 모델 저장
model.save('dart.doc2vec')

#모델 결과 확인
similar_doc = model.docvecs.most_similar('경기도 부천시 주말 모각코 모집합니다 (인근 지역 포함)')
print(similar_doc)

similar_doc = model.docvecs.most_similar('레거시 코드 활용 전략 - 온라인 스터디 모집')
print(similar_doc)
