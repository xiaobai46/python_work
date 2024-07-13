import requests

headers={

'Host': 'p1.meituan.net',
'Connection': 'keep-alive',
'M-Appkey': 'com.sankuai.meituan',
'M-TraceId': '-309049890263213520',
'User-Agent': 'AiMeiTuan /Xiaomi-14-2211133C',
'Accept-Encoding': 'gzip, deflate'
}

url='http://p1.meituan.net/289.288.80/business/914a596b2aa8205cfc5cfb18437c5946371576.jpg.webp@format=mic'
req=requests.get(url,headers=headers)
req.encoding='utf-8'
print(req.text)