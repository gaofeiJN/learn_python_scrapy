import httpx
import random
import time
from bs4 import BeautifulSoup

import lxml
import html5lib
import chardet

# User-Agent池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
]

# 设置请求头
# "Accept-Encoding": "gzip, deflate, br, zstd",
#       最好删除这个请求头
#       httpx 库支持 Brotli（br）和 Zstandard（zstd）压缩算法，安装命令： uv add 'httpx[zstd,brotli]'
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

url = "https://books.toscrape.com/"


def test1():
    print("---开始爬取---")
    res = httpx.get(url=url, headers=headers)

    with open("./debug.txt", "w", encoding="utf-8") as dbg:
        dbg.write(str(res.status_code) + "\n")
        dbg.write("-" * 30)
        dbg.write(str(res.ok) + "\n")
        dbg.write("-" * 30)
        dbg.write(res.text)


def test2():
    print("---开始爬取---")
    res = httpx.get(url=url, headers=headers)

    # 检查请求是否成功
    if res.status_code == 200:
        print("页面获取成功！")
    else:
        print(f"请求失败，状态码：{res.status_code}")
        exit()

    # print("状态码:", res.status_code)
    # print("响应头 Content-Type:", res.headers.get("Content-Type"))
    # print("requests 自动检测的编码:", res.encoding)
    # print("响应前100个字节:", res.content[:100])  # 查看原始字节

    # 2. 用 bs4 解析 HTML 内容
    # html.parser : Python 自带，速度一般，容错性中等，适合简单场景
    # 不要依赖 res.text，因为 requests 的编码检测可能出错。
    # soup = BeautifulSoup(res.text, "html.parser")

    # lxml        : 速度最快，容错性好，需安装 lxml 库
    # soup = BeautifulSoup(res.text, "lxml")

    # html5lib    : 容错性最强（类似浏览器），速度最慢，需安装 html5lib
    # soup = BeautifulSoup(res.text, "html5lib")

    # 编码问题
    # 方法一（最简单）：直接传给 BeautifulSoup 原始字节
    soup = BeautifulSoup(res.content, "lxml")  # 用 res.content 而不是 res.text

    # 方法二：手动纠正 res.encoding
    # 不要依赖 res.text，因为 requests 的编码检测可能出错。
    # 不要手动设置 res.encoding，除非你确切知道编码且上述方法失败
    # res.encoding = "utf-8"  # 或者 'gbk'，根据网站实际情况
    # html = res.text
    # soup = BeautifulSoup(html, "lxml")

    # 方法三：使用 chardet 自动检测
    # detected = chardet.detect(res.content)
    # res.encoding = detected["encoding"]
    # print(res.encoding)  # None ...
    # soup = BeautifulSoup(res.text, "lxml")

    # 3. 提取数据（观察网页结构，找到每本书的容器）
    # 每本书的信息都在 <article class="product_pod"> 里
    books = soup.find_all("article", class_="product_pod")

    # 4. 遍历并获取书名和价格
    for book in books:
        # 书名在 <h3> -> <a> 的 title 属性中
        title = book.h3.a["title"]  # 或者 book.h3.a.get('title')
        # 价格在 <div class="product_price"> -> <p class="price_color"> 中
        price = book.find("p", class_="price_color").text
        print(f"书名：{title:<100s} | 价格：{price}")


def main():
    # test1()
    test2()


if __name__ == "__main__":
    main()
