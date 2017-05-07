import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&\
channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&\
page=1&page_size=20'

def getcommentCounts(newsurl):
    m = re.search('doc-i(.*).shtml',newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']

def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    timesource = soup.select('#navtimeSource')[0].contents[0].strip()
    #string convert to datetime
    dt = datetime.strptime(timesource, '%Y年%m月%d日%H:%M')
    #datetime convert to string
    result['dt'] = dt.strftime('%Y-%m-%d %H:%M')
    result['source'] = soup.select('#navtimeSource')[0].contents[1].text.strip()
    result['str1'] = ' '.join(p.text.strip() for p in soup.select('#artibody p')[:-1])
    result['author'] = soup.select('.article-editor')[0].text.lstrip("责任编辑：")
    result['comments'] = getcommentCounts(newsurl)
    return result


