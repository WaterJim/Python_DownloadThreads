from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    WebDriverException, NoSuchElementException, TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
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
2. 需要先登录才能获取推荐列表
3. 马丹，发现推荐列表会重复
'''

'''
---------------------------------------------------------------
'''
seed_url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=60035216'  # 起始搜索页
baseSavePath = ''  # 保存路径
baseTag = ()  # tag条件
baseSize = {'width': 0, 'height': 0}  # 尺寸条件（width, height, 0则不限制）
baseViewCount = 2000  # 默认浏览数
account_info = {'id': 'waterjim90@gmail.com', 'pwd': '159753'}
'''
---------------------------------------------------------------
'''
root_url = "http://www.pixiv.net"
phantom_path = "E:\phantomjs-2.1.1-windows\\bin\phantomjs.exe"
login_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'


def has_page_load(driver):
    return driver.execute_script("return document.readyState") == 'complete'

class PixivCrawl(object):
    def __init__(self, webkit_path, root):
        # 匿名爬虫
        # 假定9999端口开启tor服务
        self.driver = webdriver.PhantomJS(executable_path=webkit_path)
        self.rootUrl = root
        pass

    def login_and_cookies(self, target_url):
        try:
            self.driver.get(target_url)
            user_input = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/span/form/div[1]/div[1]/input')
            password_input = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/span/form/div[1]/div[2]/input')
            submit_btn = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/span/form/button')
        except NoSuchElementException:
            print("login page structure have changed!, exit")
            exit(-1)

        user_input.send_keys(account_info['id'])
        password_input.send_keys(account_info['pwd'])
        submit_btn.click()
        try:
            WebDriverWait(self.driver, 3).until(staleness_of(submit_btn))
        except TimeoutException:
            raise Exception("Wrong username or password!")

        try:
            WebDriverWait(self.driver, timeout=20).until(has_page_load)
        except TimeoutException as e:
            # raise Exception("Login timeout! exit!")
            print(e)

        try_times = 0
        while True:
            time.sleep(1)
            if target_url != self.driver.current_url:
                return self.driver.get_cookies()

            try_times += 1
            if try_times > 10:
                raise Exception("Getting cookie info failed!")

        pass

    def load_web_source(self, target_url):

        self.driver.get(target_url)
        # 页面完全加载后的原始数据
        return self.driver.page_source

    def fetch_next_link(self, web_html):
        """
        获取当前页的推荐列表的所有连接
        :param web_html:
        :return: 推荐栏的地址列表
        """
        try:
            soup = BeautifulSoup(web_html, "html.parser")
            next_link_element = soup.select('li.image-item > a')
            next_link = []
            for element in next_link_element:
                next_link.append(root_url + element['href'])
            return next_link
        except Exception as e:
            print(e)
            # print("error! get link from web html, exit")
            return []

if __name__ == '__main__':

    print("启动Pixiv小爬虫......")
    print("爬虫目标起始地址：" + seed_url)
    # time.sleep(3)
    pixiv_crawl = PixivCrawl(phantom_path, root_url)
    cookie = pixiv_crawl.login_and_cookies(login_url)

    crawl_queue = [seed_url]  # 保存待爬路径 （未去重）
    seen_queue = set(crawl_queue)  # 保存待爬路径 （去重）
    while crawl_queue:
        url = crawl_queue.pop()
        html = html = pixiv_crawl.load_web_source(seed_url)
        # 做点别的操作
        # 获取下一个爬取路径
        print("获取推荐列表地址......")
        for link in pixiv_crawl.fetch_next_link(html):
            if link not in seen_queue:
                print('new link : ' + link)
                seen_queue.add(link)  # 保存新的路径
                crawl_queue.append(link)  # 保存新的路径
