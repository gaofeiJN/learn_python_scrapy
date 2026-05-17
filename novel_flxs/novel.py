import httpx, parsel, re, traceback

# User-Agent池
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
# ]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

# 设置请求头
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

url = "https://b.faloo.com/html_701_701609/"


def dl_list():
    # 尝试抓取
    try:
        res = httpx.get(url=url, headers=headers, timeout=10)

        # 判断状态码
        if res.status_code == 200:
            print(f"【任务成功】{url}")
        else:
            print(f"【任务失败】状态码：{res.status_code}")

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【任务超时】{url}")

    # 其他异常
    except Exception:
        traceback.format_exc()

    # 解析返回内容
    selector = parsel.Selector(res.text)

    link_list = selector.xpath(
        '//div[@class="c_con_list"]//div[@class="c_con_li_detail_p"]/a/@href'
    ).getall()

    # 只下载第一个
    link = f"https:{link_list[0]}"
    # print(link)
    dl_chapter(link)


def dl_chapter(link: str):
    # 尝试抓取
    try:
        res = httpx.get(url=link, headers=headers, timeout=10)

        # 判断状态码
        if res.status_code == 200:
            print(f"【任务成功】{url}")
        else:
            print(f"【任务失败】状态码：{res.status_code}")

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【任务超时】{url}")

    # 其他异常
    except Exception:
        traceback.format_exc()

    text = res.text

    # 保存文件
    with open("html.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # 解析返回内容
    selector = parsel.Selector(text)

    html_text = selector.xpath('//div[@class="noveContent"]').get()
    # print(html_text)
    content = re.sub(r"</?div.*?>", "", html_text).strip()
    content = re.sub(r"</?p.*?>", "  ", content)
    # content = re.sub(r"</p>", "\n", content)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    # print(content)

    # # 保存文件
    with open("chaper.txt", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    dl_list()


if __name__ == "__main__":
    main()
