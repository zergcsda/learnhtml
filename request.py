import requests
from bs4 import BeautifulSoup
import news_sina


res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

for news in soup.select(".blk121"):
    for h2 in news.select('a'):
        href = h2['href']
        print(h2.text.strip(),href)
        print(h2.text.strip(),news_sina.getNewsDetail(href))

