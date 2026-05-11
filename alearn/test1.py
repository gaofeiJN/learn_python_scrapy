import httpx
import random
import time
import lxml
from bs4 import BeautifulSoup

# User-Agent池
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
# ]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
]

# 设置请求头
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

url = "https://www.qykdxh.org/read/642532/30241985.html"


def test1():
    print("---开始爬取---")
    # res = httpx.get(url=url, headers=headers)
    # 关闭重定向
    res = httpx.get(url, headers=headers)

    # 检查请求是否成功
    if res.status_code == 200:
        print("页面获取成功！")
    else:
        print(f"请求失败，状态码：{res.status_code}")
        exit()

    # 2. 用 bs4 解析 HTML 内容
    soup = BeautifulSoup(res.content, "lxml")  # 用 res.content 而不是 res.text

    # 3. 提取数据（观察网页结构，找到每本书的容器）
    # 每本书的信息都在 <article class="product_pod"> 里
    bookname = soup.find("div", class_="bookname")
    chapter_name = bookname.h1.text
    content = soup.find("div", id="content")

    # 4. 存储数据
    with open(f"./{chapter_name}.txt", "w", encoding="utf-8") as f:
        f.write(content.text)


def main():
    test1()


if __name__ == "__main__":
    main()
