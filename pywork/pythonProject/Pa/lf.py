from retrying import retry
import requests
from urllib.parse import urlparse
import os
import subprocess

# @retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def dlf(url,bdurl):#url访问路径，bdurl本地保存路径
    # try:
    if not os.path.exists(bdurl + bdurl.split('/')[-1] + '.mp4'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        m1_jpg_text = requests.get(url, headers=headers)
        # print(m1_jpg_text.text)
        # 从一级地址中解析二级地址
        m1_jpg_text_list = m1_jpg_text.text.split('\n')
        # 截取ip地址
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc

        m2_url = base_url + m1_jpg_text_list[-2]
        m2_jpg_text = requests.get(m2_url, headers=headers)
        # print(m2_jpg_text.text)
        jpg_url_list = []
        for line in m2_jpg_text.text.split('\n'):
            if not line.startswith('#'):
                jpg_url = 'https://play.modujx10.com' + line
                jpg_url_list.append(jpg_url)
        for i, url in enumerate(jpg_url_list):
           a = 1
           while a==1:
               try:
                   print(str(len(jpg_url_list)) + '_________________________' + str(
                       jpg_url_list.index(url)) + '___________________________' + str(
                       (i + 1) / len(jpg_url_list) * 100))
                   jpg_data = requests.get(url, headers=headers,timeout=10)#爬取每一个ts视频数据
                   # print(response.raise_for_status())
                   jpg_name = url.split('/')[-1]
                   jpg_path = bdurl + '/' + jpg_name.split('.')[0] + '.ts'
                   text_path = bdurl + '/filelist.txt'
                   if not os.path.exists(jpg_path):
                       with open(jpg_path, 'wb') as f:
                           f.write(jpg_data.content)
                       with open(text_path, 'a') as f:
                           f.write("file '{}'\n".format(jpg_name.split('.')[0] + '.ts'))
                   a = -1
               except Exception as e:
                   print(e)


            # 使用ffmpeg合并ts片段
        ffmpeg_cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', text_path,
            '-c', 'copy',
            bdurl + bdurl.split('/')[-1] + '.mp4',
        ]

            # 执行ffmpeg命令
        subprocess.run(ffmpeg_cmd, check=True)
    # except requests.exceptions.RequestException as e:
    #     print(f"Request failed: {e}")
    #     raise  # 注意：如果要在重试后继续抛出异常，请保留这一行