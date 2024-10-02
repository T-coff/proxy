# -*- coding: utf-8 -*-
"""
@Filename	:	🐍proxy.py
@Created 	:	🐋2024/09/29  18:50
@Updated	:	🐳2024/09/29  18:50
@Author 	:	📧goonhope@gmail.com; 🚀Teddy️; 📍Zhuhai
@Function	:	🎯 指定地区代理获取，默认china
@Process 	:	🌊 curl -> all.txt -> filter -> china.json
@WitNote	:	👀备注
@Reference	:	🔖https://raw.githubusercontent.com/Noctiro/getproxy/refs/heads/master/file/all.txt🌾
"""
from require import fdir, tsleep,fetch,config,filed, err


class Proxy:
    """代理"""
    def __init__(self,c='china',*args,**kwargs):
        self.country, self.k = c, "http https socks4 socks5".split()
        super().__init__(*args,**kwargs)
        self.hold, self.url = [], "https://raw.githubusercontent.com/Noctiro/getproxy/refs/heads/master/file/all.txt"
        self.i, self.q = dict.fromkeys(self.k,0), "qurey country".split()

    @err
    def single(self,url):
        """验证过滤"""
        t, ip, port = [x.strip('/') for x in url.split(":")]
        if info := fetch(f"http://ip-api.com/json/{ip}?fields=status,country,city",proxy={t: url}):
            if info.get("status") == "success" and self.country in info.get('country', '').lower():
                info.pop("status")
                info.update(dict(port=url, t=t))
                self.hold.append(info)
                print(f'@Proxy: {url}')
                self.i[t] += 1

    def _save(self):
        """save json"""
        if self.hold: config(self.hold, fdir(f'{self.country or "all"}.json'))

    def go(self,n=100):
        """获取ip"""
        s = filed(fdir('all.txt'))
        hold = {k: [i for i in s if i.split(':')[0].strip() == k and i.count(':') == 2] for k in self.k}
        ips = [x for i in hold.values() for x in i[:n]]
        for url in ips:
            self.single(url)
            tsleep(1, 0.5)
        self._save()


if __name__ == '__main__':
    Proxy().go()
