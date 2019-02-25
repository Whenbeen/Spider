# _*_coding:UTF-8 _*
import urllib2
from bs4 import BeautifulSoup
import re


class Jianshu:

    def __init__(self):
        self.download = Download()
        self.parser = Parse()

    def spider_pro(self, speed_urls, base_url):
        # self.download.save_html("dfdf",r"每实爱情感动瞬间征文妻子今天四周岁.html".decode('utf-8'))
        data = set()
        url_content = self.download.download(speed_url)
        if url_content != None:
            data = self.parser.get_all_urls(base_url, url_content)
            count = 0
            for url in data:
                content= self.download.download(url)
                name = self.parser.get_title(content)
                name=self.sub_replace(name)+".html"
                self.download.save_html(content,  name)

    def sub_replace(self, str):
        regex = re.compile(ur"\|")
        print regex.sub('', str)
        return regex.sub('', str)


class Download(object):

    def download(self, url):
        if url is None:
            return None
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Cookie": "Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1466075280; __utma=194070582.826403744.1466075281.1466075281.1466075281.1; __utmv=194070582.|2=User%20Type=Visitor=1; signin_redirect=http%3A%2F%2Fwww.jianshu.com%2Fsearch%3Fq%3D%25E7%2594%259F%25E6%25B4%25BB%26page%3D1%26type%3Dnote; _session_id=ajBLb3h5SDArK05NdDY2V0xyUTNpQ1ZCZjNOdEhvNUNicmY0b0NtMnVuUUdkRno2emEyaFNTT3pKWTVkb3ZKT1dvbTU2c3c0VGlGS0wvUExrVW1wbkg1cDZSUTFMVVprbTJ2aXhTcTdHN2lEdnhMRUNkM1FuaW1vdFpNTDFsQXgwQlNjUnVRczhPd2FQM2sveGJCbDVpQUVWN1ZPYW1paUpVakhDbFVPbEVNRWZzUXh5R1d0LzE2RkRnc0lJSHJEOWtnaVM1ZE1yMkt5VC90K2tkeGJQMlVOQnB1Rmx2TFpxamtDQnlSakxrS1lxS0hONXZnZEx0bDR5c2w4Mm5lMitESTBidWE4NTBGNldiZXVQSjhjTGNCeGFOUlpESk9lMlJUTDVibjNBUHdDeVEzMGNaRGlwYkg5bHhNeUxJUVF2N3hYb3p5QzVNTDB4dU4zODljdExnPT0tLU81TTZybUc3MC9BZkltRDBiTEsvU2c9PQ%3D%3D--096a8e4707e00b06b996e8722a58e25aa5117ee9; CNZZDATA1258679142=1544596149-1486533130-https%253A%252F%252Fwww.baidu.com%252F%7C1486561790; _ga=GA1.2.826403744.1466075281; _gat=1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        content = ""
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read() 
        except urllib2.URLError, e:
            if hasattr(e, "reason") and hasattr(e, "code"):
                print e.code
                print e.reason
            else:
                print "请求失败"
        return content

    def save_html(self, content, name):
        #  title = name + ".html"
        with open(name, "wb") as f:
            # 写文件用bytes而不是st，所以要转码
            # print  name + ".html"
            f.write(content)
            f.close() 


class Parse(object):

    def get_all_urls(self, base_url, content):
        soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
        url_data = set()
        content_list = soup.find_all("a", {"class": "wrap-img"})
        for div in content_list:
            article_url = base_url + div.get("href")
            url_data.add(article_url);
        return url_data;

    def get_title(self, content):
        soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
        name = soup.find("h1", {"class": "title"}).get_text()
        return name


if __name__ == '__main__':
    speed_url = 'https://www.jianshu.com/trending/weekly?utm_medium=index-banner-s&utm_source=desktop'
    jianshu = Jianshu()
    jianshu.spider_pro(speed_url, "https://www.jianshu.com/")
