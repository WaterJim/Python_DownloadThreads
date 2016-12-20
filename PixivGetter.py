from selenium import webdriver
from bs4 import BeautifulSoup
import os
import DownloadTask
import time

'''
爬取Pixiv中浏览数在一定数值上的图片
可选功能应有以下几点：
1. 应支持标签选择功能（比如只搜索含有“东方”标签的）
2. 应支持尺寸大小选择功能，满足想要获取壁纸的用户
3. 可定义图片保存路径，默认保存名为 P站ID+图片标题
4. 可定义浏览数大小（太小了一堆文件会不会炸磁盘啊）

目前发现问题：
1. 右侧推荐栏还是需要动态加载才能获取数据
'''

'''
---------------------------------------------------------------
'''
seedUrl = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=60035216'  # 起始搜索页
baseSavePath = ''  # 保存路径
baseTag = ()  # tag条件
baseSize = {'width': 0, 'height': 0}  # 尺寸条件（width, height, 0则不限制）
baseViewCount = 2000  # 默认浏览数
'''
---------------------------------------------------------------
'''
rootUrl = "http://www.pixiv.net"
phantomPath = "E:\phantomjs-2.1.1-windows\\bin\phantomjs.exe"


def loadWebPageSource(targetUrl, webkitPath):
    # 匿名爬虫
    # 假定9999端口开启tor服务
    driver = webdriver.PhantomJS(executable_path=webkitPath)
    driver.get(targetUrl)
    # 页面完全加载后的原始数据
    return driver.page_source


def getAllNextLink(webHtml):
    '''
    获取当前页的推荐列表的所有连接
    :param webHtml: 当前页的原文件
    :return: 推荐栏的地址列表
    '''
    try:
        soup = BeautifulSoup(webHtml, "html.parser")
        nextLinkElement = soup.select('li.image-item > a')
        nextLink = []
        for element in nextLinkElement:
            nextLink.append(rootUrl + element['href'])
        return nextLink
    except Exception:
        print("error! get link from web html, exit")
        return -1
    pass


if __name__ == '__main__':
    print("启动Pixiv小爬虫......")
    print("爬虫目标起始地址：" + seedUrl)
    time.sleep(3)

    crawl_queue = [seedUrl]  # 保存待爬路径 （未去重）
    seen_queue = set(crawl_queue)  # 保存待爬路径 （去重）
    while crawl_queue:
        url = crawl_queue.pop()
        html = loadWebPageSource(url, phantomPath)
        # 做点别的操作
        print(html)
        # 获取下一个爬取路径
        for link in getAllNextLink(html):
            if link not in seen_queue:
                print('new link : ' + link)
                seen_queue.add(link)  # 保存新的路径
                crawl_queue.append(link)  # 保存新的路径
        time.sleep(5)  # 避免运行过快
