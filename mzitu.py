import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os


if __name__ == '__main__':
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
    all_url = 'http://www.mzitu.com/all'  ##开始的URL地址
    start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
    #print(start_html.text) ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
    Soup = BeautifulSoup(start_html.text, 'lxml')
    all_a = Soup.find('div', class_ = 'all').find_all('a');
    #PS:  ‘find’ 只查找给定的标签一次，就算后面还有一样的标签也不会提取出来哦！ 而  ‘find_all’ 是在页面中找出所有给定的标签！有十个给定的标签就返回十个（返回的是个list哦！！）,想要了解得更详细，就是看看官方文档吧！
    all_a.pop(0)
    for a in all_a:
        #print(a)
        title = a.get_text()

        path = str(title).strip()  ##去掉空格
        os.makedirs(os.path.join("D:\mzitu", path))  ##创建一个存放套图的文件夹
        os.chdir("D:\mzitu\\" + path)  ##切换到上面创建的文件夹

        href = a['href']
        #print(href)
        html = requests.get(href, headers=headers)  ##上面说过了
        html_Soup = BeautifulSoup(html.text, 'lxml')  ##上面说过了
        maxSpan = html_Soup.find('div',class_ = 'pagenavi').find_all('span')[6].get_text()
        #print(maxSpan)
        for page in range(1,int(maxSpan)+1):
            page_url = href+ '/' + str(page)
            #print(page_url)
            img_html = requests.get(page_url, headers=headers)
            img_Soup = BeautifulSoup(img_html.text, 'lxml')
            img_url = img_Soup.find('div',class_ = 'main-image').find('img')['src']
            print(img_url)
            name = img_url[-9:-4]  ##取URL 倒数第四至第九位 做图片的名字
            headers_ = {"Referer":"http://www.mzitu.com/149051",'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
            img = requests.get(img_url, headers=headers_)
            f = open(name + '.jpg', 'wb')  ##写入多媒体文件必须要 b 这个参数！！必须要！！
            f.write(img.content)  ##多媒体文件要是用conctent哦！
            f.close()

