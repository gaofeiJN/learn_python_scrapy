import httpx
import random
import re
import parsel
import time

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

url = "https://www.qykdxh.org/read/642532/"


def dl_chapter(url):
    global headers
    try:
        res = httpx.get(url, headers=headers)

        # 检查请求是否成功
        if res.status_code == 200:
            print(f"【dl_chapter】{url}页面获取成功！")
        else:
            print(f"【dl_chapter】{url}请求失败，状态码：{res.status_code}")
            # exit()
            return

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【dl_chapter】{url} : 请求超时")
        # exit()
        return

    # 2. 用 parsel 解析 HTML 内容
    # parsel.Selector(
    #   text: str | None = None,
    # type: str | None = None,
    #   body: bytes | bytearray = b"",
    #   encoding: str = "utf-8",
    #   namespaces: Mapping[str, str] | None = None,
    #   root: Any | None = _NOT_SET,
    #   base_url: str | None = None,
    #   _expr: str | None = None,
    #   huge_tree: bool = LXML_SUPPORTS_HUGE_TREE)
    #   -> Selector

    # 应该使用res.text
    # sel = parsel.Selector(res.content)
    sel = parsel.Selector(res.text)

    # 3. 提取数据（观察网页结构，找到每本书的容器）
    # 章节名
    chapter_name = sel.xpath("//div[@class='bookname']/h1/text()").get()

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
    content = sel.xpath("//div[@id='content']").get()
    content = re.sub(r"</?div.*?>", "", content)
    content = re.sub(r"<p>", "  ", content)
    content = re.sub(r"</p>", "\n", content)
    content = "  " + content.strip()

    # 4. 存储数据
    with open(f"./小说/{chapter_name}.txt", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{chapter_name} 下载完成")


def dl_list():
    global headers
    global url

    try:
        print("---开始抓取---")
        res = httpx.get(url=url, headers=headers)

        # 检查请求是否成功
        if res.status_code == 200:
            print("【dl_list】页面获取成功！")
        else:
            print(f"【dl_list】请求失败，状态码：{res.status_code}")
            exit()

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【dl_list】{url} : 请求超时")
        # exit()
        return

    # 2. 用 parsel 解析 HTML 内容
    sel = parsel.Selector(res.text)

    # 3. 提取数据
    href_list = sel.xpath('//div[@id="list"]//a/@href').getall()

    # 4. 存储数据
    with open(f"./小说/连接目录.txt", "w", encoding="utf-8") as f:
        for href in href_list:
            f.write(href + "\n")

    # 5. 抓取章节
    for href in href_list:
        dl_chapter("https:" + href)
        time.sleep(5)  # 休眠5秒


def dl_list2():
    """
    重新抓取未成功的章节
    """
    global headers
    global url

    print("---开始抓取---")
    res = httpx.get(url=url, headers=headers)

    # 检查请求是否成功
    if res.status_code == 200:
        print("【dl_list】页面获取成功！")
    else:
        print(f"【dl_list】请求失败，状态码：{res.status_code}")
        exit()

    # 2. 用 parsel 解析 HTML 内容
    sel = parsel.Selector(res.text)

    # 3. 提取a元素
    a_list = sel.xpath('//div[@id="list"]//a')

    # 4. 抓取指定章节
    target_list = [
        "103",
        "109",
        "234",
        "247",
        "280",
        "285",
        "411",
        "418",
        "432",
        "472",
        "547",
        "550",
        "551",
        "576",
        "674",
        "686",
        "694",
        "718",
    ]
    for a in a_list:
        title = a.xpath("text()").get()
        title_num = re.search(r"第(\d+)章", title)[1]
        if title_num in target_list:
            href = a.xpath("@href").get()
            dl_chapter("https:" + href)
            time.sleep(5)  # 休眠5秒


def test():
    hh = "第12章"
    rr = re.search(r"第(\d+)章", hh)[1]
    print(rr)


def main():
    # dl_list()
    # dl_chapter("https://www.qykdxh.org/read/642532/30241948.html")
    test()
    dl_list2()


if __name__ == "__main__":
    main()
