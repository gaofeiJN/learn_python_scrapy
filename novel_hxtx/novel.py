import httpx, parsel, re, traceback
import pprint

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

url = "https://www.hongxiu.com/book/12394139504487203"


def dl_list():
    # 尝试抓取
    try:
        with httpx.Client() as client:
            client.headers.update(headers)
            client.timeout = 10
            res = client.get(url=url)

            # 判断状态码
            if res.status_code == 200:
                print(f"【任务成功】{url}")
                # with open("list.html", "w", encoding="utf-8") as f:
                #     f.write(res.text)
            else:
                print(f"【任务失败】状态码：{res.status_code}")
                pprint.pprint(res.text)

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【任务超时】{url}")

    # 其他异常
    except Exception:
        traceback.format_exc()

    # 解析返回内容
    selector = parsel.Selector(res.text)

    chapter_list = []
    for sel in selector.xpath('//div[@class="volume"]/ul[@class="cf"]/li/a'):
        chapter_list.append(
            {
                "title": sel.xpath("./text()").get(),
                "link": f"https://www.hongxiu.com{sel.xpath('./@href').get()}",
            }
        )

    # pprint.pprint(chapter_list)
    dl_chapter(chapter_list[0]["title"], chapter_list[0]["link"])


def dl_chapter(title: str, link: str):
    # 尝试抓取
    try:
        with httpx.Client() as client:
            client.headers.update(headers)
            client.timeout = 10
            res = client.get(url=link)

            # 判断状态码
            if res.status_code == 200:
                print(f"【任务成功】{link}")
            else:
                print(f"【任务失败】状态码：{res.status_code}")
                pprint.pprint(res.text)

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【任务超时】{link}")

    # 其他异常
    except Exception:
        traceback.format_exc()

    # 解析返回内容
    tt = res.text

    with open(f"{title}.html", "w", encoding="utf-8") as f:
        f.write(tt)
    selector = parsel.Selector(tt)

    p_list = selector.xpath('//div[@class="ywskythunderfont"]//p/text()').getall()
    content = "\n".join(p_list)

    # # 保存文件
    with open(f"{title}.txt", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    # dl_list()

    # 免费章节
    dl_chapter(
        "第一章 刚出生，是炼丹炉",
        "https://www.hongxiu.com/chapter/12394139504487203/62333079024358583",
    )

    # VIP章节
    dl_chapter(
        "第七十二章 阵法核心",
        "https://www.hongxiu.com/chapter/12394139504487203/63362040445592277",
    )


if __name__ == "__main__":
    main()
