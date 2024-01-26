
#__next > main > main > ul > li:nth-child(1) > a > div.css-ece8i8.e1yoxoiv3 > p #본문
#__next > main > main > ul > li:nth-child(1) > a > div.css-12krszf.e1yoxoiv2 > div.css-1j4ebmn.e1yoxoiv11 #상태
#__next > main > main > ul > li:nth-child(1) > a > div.css-ece8i8.e1yoxoiv3 > h2 #제목
import requests
from bs4 import BeautifulSoup
import pandas as pd

contentlist = []

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = "https://community.programmers.co.kr/study"
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
paragraphs = soup.select('#__next > main > main > ul > li')  # 스터디 모집글 크롤링

for paragraph in paragraphs:
    url_help = 'https://community.programmers.co.kr/'

    # 모집 중 여부
    condition = paragraph.select_one('a > div.css-12krszf.e1yoxoiv2 > div.css-1j4ebmn.e1yoxoiv11').text.strip()

    if condition != '모집중':
        continue

    # 스터디 제목
    a_title = paragraph.select_one('a > div.css-ece8i8.e1yoxoiv3 > h2').text.strip()

    # 스터디 모집글
    content = paragraph.select_one('a > div.css-ece8i8.e1yoxoiv3 > p').text.strip()

    # 스터디 모집글 링크
    a_url = paragraph.select_one('a').attrs['href']

    print(condition)
    print(a_title)
    print(content)
    print(url_help + a_url)

    # NLP 분들은 이 부분부터 수정하시면 될것 같아요.
    contentlist.append(content)  # 내용
    contentlist.append(a_title)  # 제목
    contentlist.append(url_help + a_url)  # url

# dataframe으로 변환
df = pd.DataFrame()
df["content"] = contentlist[::3]  # content는 리스트의 0, 3, 6, ... 인덱스에 위치
df["title"] = contentlist[1::3]  # title은 리스트의 1, 4, 7, ... 인덱스에 위치
df["url"] = contentlist[2::3]  # url은 리스트의 2, 5, 8, ... 인덱스에 위치

print(df.head(5))

df.to_csv("test_program.csv", encoding="utf-8-sig")
