import httpx
import random
import time
import lxml
import re
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


def dl_chapter(url):
    global headers
    res = httpx.get(url, headers=headers)

    # 检查请求是否成功
    if res.status_code == 200:
        print(f"【dl_chapter】{url}页面获取成功！")
    else:
        print(f"【dl_chapter】{url}请求失败，状态码：{res.status_code}")
        exit()

    # 2. 用 bs4 解析 HTML 内容
    soup = BeautifulSoup(res.content, "lxml")  # 用 res.content 而不是 res.text

    # 3. 提取数据（观察网页结构，找到每本书的容器）
    # 章节名
    bookname = soup.find("div", class_="bookname")
    chapter_name = bookname.h1.text

    # re.sub(
    #   pattern: str | Pattern[str],
    #   repl: str | ((Match[str]) -> str),
    #   string: str,
    #   count: int = 0,
    #   flags: _FlagsType = 0)
    #   -> str
    chapter_name = re.sub(
        r"第(\d+)章", lambda m: f"第{int(m.group(1)):04d}章", chapter_name
    )

    # 章节内容
    content = soup.find("div", id="content")

    # 4. 存储数据
    with open(f"./小说/{chapter_name}.txt", "w", encoding="utf-8") as f:
        f.write(content.text)


def dl_list():
    global headers
    url = "https://www.qykdxh.org/read/642532/"

    print("---开始抓取---")
    res = httpx.get(url, headers=headers)

    # 检查请求是否成功
    if res.status_code == 200:
        print("【dl_list】页面获取成功！")
    else:
        print(f"【dl_list】请求失败，状态码：{res.status_code}")
        exit()

    # 2. 用 bs4 解析 HTML 内容
    soup = BeautifulSoup(res.content, "lxml")  # 用 res.content 而不是 res.text

    # 3. 提取数据
    # 每本书的信息都在 <article class="product_pod"> 里
    list_node = soup.find("div", id="list")
    a_nodes = list_node.find_all("a")
    href_list = [a["href"] for a in a_nodes]

    # 4. 存储数据
    with open(f"./小说/连接目录.txt", "w", encoding="utf-8") as f:
        for href in href_list:
            f.write(href + "\n")

    # 5. 抓取章节
    for href in href_list:
        dl_chapter("https:" + href)
        time.sleep(2)  # 休眠2秒


def main():
    dl_list()


if __name__ == "__main__":
    main()
