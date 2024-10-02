# -*- coding: utf-8 -*-
"""
@Filename	:	🐍require.py
@Created	:	🐋2024/10/02 10:00:02
@Updated	:	🐳2024/10/02 10:00:02
@Author		:	📧goonhope@gmail.com; 🚀Teddy️; 📍Zhuhai
@Function	:	🎯required function for proxy.py
@Process	:	🌊read -> found -> extract -> done
@WitNote	:	👀by re
@Reference	:	🔖Personal project
"""
import os, time
from faker import Faker
import requests, json, random
from urllib3 import disable_warnings as dw;dw()


def fdir(subf="", md=True):
    """目录，移植默认本文件目录 done"""
    my, user = r"D:\Downloads\temp", os.path.join(os.path.dirname(__file__),"data")
    cdir = my if os.environ.get("COMPUTERNAME",'').startswith("TE") else user
    result = subf and os.path.join(cdir, subf) or cdir
    root = "." not in os.path.split(result)[-1] and result or os.path.dirname(result)
    md and not os.path.exists(root) and os.makedirs(root)
    return result


def showdir(path=""):
    """打开目录或文件——open with explorer"""
    os.system(r'start "" "{}"'.format(path))


def google_hder(host=None, o=True):
    """'google search url headers"""
    hders = {'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN, zh;q=0.9',
             'Connection': 'keep-alive',
             'Referer': f'https://www.{"google.com.hk" if o else "qq.com"}',
             'Upgrade-insecure-requests': '1',
             'User-Agent': Faker("zh_CN").chrome()}  # fr..user_agent()
    if host and isinstance(host, (str, dict)):
        hders |= host if isinstance(host, dict) else dict(Host=host)
    return hders


def tsleep(max=0., min=0.5):
    """固定随机sleep时间"""
    time.sleep(random.uniform(min, max) if max > min else min)


def err(func):
    """错误时返回函数名称"""
    def inner(*args, **kwargs):
        intime = time.strftime("%Y/%m/%d %H:%M:%S")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return print(f"@ERROR: {intime}->{func.__name__}\nDetail: {e}!")
    return inner


@err
def fetch(url="", m=True, p=None, h=None, data=None, json=None, proxy=None, raw=False, tout=30):
    """网页提取"""
    headers = google_hder((isinstance(h, dict) and h or dict()) | dict(Host=url.split("/")[2]))
    proxy = random.choice(proxy) if isinstance(proxy, list) else proxy
    kw = dict(url=url, headers=headers, proxies=proxy, params=p, json=json, data=data, verify=False)
    data = requests.request(method='GET' if m else 'POST', timeout=tout, **kw)
    if data.status_code == 200: return data.text if raw else data.json()
    else: return print("@fetch check !")


def config(jsn=None, file=''):
    """json 读写：生成或读取配置文件"""
    with open(file or fdir('config.ini'), 'w' if jsn else 'r', encoding='utf8') as f:
        return json.dump(jsn,f) if jsn else json.load(f)


def filed(file, content="", enc="utf-8"):
    """文件读写操作"""
    mode = "w" if content else "r"
    with open(file, mode, encoding=enc) as of:
        return of.write(content) if content else of.read().splitlines()
