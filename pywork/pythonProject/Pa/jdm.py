import requests
import re
from bs4 import BeautifulSoup
import html


# 处理字符串的函数
def process_html_content(html_str):
    # 使用HTMLParser库来解码HTML实体
    from html.parser import HTMLParser
    class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
            # 这里我们简单地将数据添加到result中，但不处理标签
            self.result.append(data)

        def handle_starttag(self, tag, attrs):
            # 对于<br/>标签，我们添加一个换行符
            if tag == 'br':
                self.result.append('\n')

    parser = MyHTMLParser()
    parser.result = []
    parser.feed(html_str)

    # 连接所有处理后的数据部分
    processed_content = ''.join(parser.result)

    # 替换剩余的&nbsp;为空格（如果有的话）
    processed_content = processed_content.replace('&nbsp;', ' ')

    return processed_content

url = 'http://m.isiluke.org/html/46451/14405777.html'
aaa=1
next_page=1
next_zhang=1
while next_page!=-1 or next_zhang!=-1:

    req = requests.get(url, timeout=100)
    req.encoding = 'utf-8'
    # print(req.text)
    text = re.findall(
        '<div id="content_tip"><b>最新网址：m.isiluke.org</b></div>(.*?)<div id="content_tip"><b>最新网址：m.isiluke.org</b></div>',
        req.text, re.DOTALL)
    if len(text)==0:
        text = re.findall(
             r'告！\r\n    </p>(.*?)<p><script>crcowwltp' ,
            req.text, re.DOTALL)
    # print(text)
    # 获取标签内的文本内容，同时转换HTML实体
    text_content = process_html_content(text[0])
    with open('jdm.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + text_content)

    # 判断有没有下一页
    next_page = req.text.find('下一页')
    if next_page != -1:
        soup = BeautifulSoup(req.text, 'html.parser')  # 或者使用'html.parser'
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            if text.startswith('下') and text.endswith('页') and href.startswith('/html/46451/'):
                url='http://m.isiluke.org'+href
    else:
        # 判断有没有下一章
        next_zhang = req.text.find('下一章')
        if next_zhang != -1:
            print(aaa)
            aaa+=1
            soup = BeautifulSoup(req.text, 'html.parser')  # 或者使用'html.parser'
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                text = a_tag.get_text(strip=True)
                if text.startswith('下') and text.endswith('章')  and href.startswith(
                        '/html/46451/'):
                    url = 'http://m.isiluke.org' + href
