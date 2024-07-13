import requests
import re
from bs4 import BeautifulSoup
import html


def nextpage(url,page):
    u = 'https://www.blwenla.org' + url + '_'+str(page)+'.html'
    req = requests.get(u, timeout=100)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(req.text, 'html.parser')

    # 查找class为"articlecontent"且id为"articlecontent"的<p>标签
    p_tag = soup.find('p', {'class': 'articlecontent', 'id': 'articlecontent'})

    if p_tag:
        # 获取标签内的文本内容，同时转换HTML实体
        text_content = p_tag.get_text(separator='\n', strip=True)  # separator='\n'将<br/>转换为换行符

        # 进一步处理文本内容，将HTML实体转换为对应字符
        # 这里只处理&nbsp;为空格，但你可以根据需要添加其他实体的处理
        text_content = html.unescape(text_content)
        # 写入到文本文件
        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + text_content)

    next_page = req.text.find('下一页')
    return next_page

url='https://www.blwenla.org/52/52015/'
req=requests.get(url,timeout=100)
# print(req.text)
# list=re.findall(r'<li><a href="(/52/52015/.*?).html">第\d+章</a></li>',req.text)

list=[]
# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(req.text, 'html.parser')  # 或者使用'html.parser'

# 查找所有的<a>标签
# for a_tag in soup.find_all('a', href=True):
#     # 提取href属性和文本内容
#     href = a_tag['href']
#     text = a_tag.get_text(strip=True)
#
#     # 检查文本是否以“第”开头，并后跟一个或多个数字，以及“章”结尾
#     if text.startswith('第') and text.endswith('章') and text[1:-1].isdigit():
#         # 如果满足条件，打印href和文本内容
#         print(f"链接: {href}, 章节: {text}")

    # 如果你只想提取特定路径下的链接（例如/52/52015/开头的），你可以添加一个额外的条件判断
aaa=0
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    text = a_tag.get_text(strip=True)

    if text.startswith('第') and text.endswith('章') and text[1:-1].isdigit() and href.startswith('/52/52015/'):
        print(f"链接: {href}, 章节: {text},{href.split(".")[0]}")
        cleaned_text = re.sub(r'\D', '', text)  # \D 匹配任何非数字字符
        if int(cleaned_text)%6==0:
            list.append(href.split(".")[0]+str(aaa))
        else:
            list.append(href.split(".")[0])
            parts = href.split("/")
            number = parts[-1].split(".")[0]
            aaa=int(number)+1
for i in range(100):
    list.append('/52/52015/'+str(int(list[-1].split("/")[-1])+1))
for i in list:#只有六十章
    # print(i)
    u='https://www.blwenla.org'+i+'.html'
    req=requests.get(u,timeout=100)

    # textlist = re.findall('<p class="articlecontent" id="articlecontent">(.*?)</p>', req.text, re.DOTALL)


    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(req.text, 'html.parser')

    # 查找class为"articlecontent"且id为"articlecontent"的<p>标签
    p_tag = soup.find('p', {'class': 'articlecontent', 'id': 'articlecontent'})

    if p_tag:
        # 获取标签内的文本内容，同时转换HTML实体
        text_content = p_tag.get_text(separator='\n', strip=True)  # separator='\n'将<br/>转换为换行符

        # 进一步处理文本内容，将HTML实体转换为对应字符
        # 这里只处理&nbsp;为空格，但你可以根据需要添加其他实体的处理
        text_content = html.unescape(text_content)

        # 写入到文本文件
        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write('\n'+text_content)

    #再判断有没有下一页有下一页的话访问下一页，没有的话执行下一次循环
    next_page=req.text.find('下一页')
    page=2
    while next_page>0:
        next_page=nextpage(i,page)
        page=page+1
