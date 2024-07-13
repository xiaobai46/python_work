import requests
from bs4 import BeautifulSoup
from lf import dlf
import os
from retrying import retry

url_lf='https://moduzy.cc/list6'
url_lf_list=[url_lf]
for i in range(2,54):
    url_lf_list.insert(0,url_lf+'-'+str(i)+'/')


for url_lf in url_lf_list:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.get(url_lf, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('p', {'class': 'articlecontent', 'id': 'articlecontent'})

    url_list = []  # 番剧列表
    # bdurl = ''
    bdurl_list=[]
    for a_tag in soup.find_all('a', {'class': 'h4', 'target': '_blank'}, href=True, ):
        href = a_tag['href']
        text = a_tag.get_text(strip=True)
        # print(href, text)
        url_list.append('https://moduzy.cc' + href)
        if not os.path.exists('F://lifan/' + text):
            if '.' in text:
                # 注意：这里只是简单地移除了所有的点号，你可能需要更复杂的逻辑来处理文件名
                # 例如，你可能想要保留文件扩展名中的点号
                text = text.replace('.', '')
            os.makedirs('F://lifan/' + text)
        bdurl_list.append('F://lifan/' + text)
    for url,bdurl in zip(url_list,bdurl_list):  
        lf = requests.get(url, headers=headers)

        soup = BeautifulSoup(lf.text, 'html.parser')
        # lf_series_list=[]
        for a_tag in soup.find_all('a', {'class': 'copy_text', 'target': '_blank'}, href=True, ):
            text = a_tag.get_text(strip=True)
            print(bdurl + '/' + text[0:3] + '__________' + text[4:])
            if not os.path.exists(bdurl + '/' + text[0:3]):
                if '.' in bdurl:
                    # 注意：这里只是简单地移除了所有的点号，你可能需要更复杂的逻辑来处理文件名
                    # 例如，你可能想要保留文件扩展名中的点号
                    bdurl = bdurl.replace('.', '')

                os.makedirs(bdurl + '/' + text[0:3])
            dlf(text[4:], bdurl + '/' + text[0:3])

