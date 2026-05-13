"""
爬取豆瓣电影信息
"""

import httpx
import time
import pandas as pd
from rich import print

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

# 设置请求头
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://m.douban.com/movie/",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://m.douban.com",
}

# url
url = "https://m.douban.com/rexxar/api/v2/subject/recent_hot/movie"


def get_info(
    start: int = 0, limit: int = 20, category: str = "豆瓣高分", type: str = "华语"
) -> list[tuple[str, str, float]] | None:
    parameters = {
        "start": str(start),
        "limit": str(limit),
        "category": category,
        "type": type,
    }

    # 发送请求
    res = httpx.get(url=url, headers=headers, params=parameters)

    # 检查请求是否成功
    if res.status_code == 200:
        print(f"{url}页面获取成功！")
    else:
        print(f"{url}请求失败，状态码：{res.status_code}, 响应内容: {res.json()}")
        exit()

    # 返回的json字符串中有键值"items",而"items"也是字典的内置方法,
    # 使用res.json().items时,解释器会尝试调用字典的items()方法,从而报错
    # print(res.json().items) # <built-in method items of dict object at 0x000001FE9A91D400>

    # res_json = res.json()
    # print(res_json)

    results = []
    # 应当使用res.json()["items"]语法
    for item in res.json()["items"]:
        results.append(
            [item["title"], item["card_subtitle"], float(item["rating"]["value"])]
        )

    return results


def test1():
    results = []
    for x in range(0, 141, 20):
        results.extend(get_info(x, 20))
        time.sleep(5)

    with open("./movie_list.txt", "w", encoding="utf-8") as f:
        for movie in results:
            # print(movie)
            f.write(f"{movie[0]},{movie[1]},{movie[2]} \n")

    df = pd.DataFrame(results, columns=["电影", "详细信息", "评分"])
    df.to_excel("movies.xlsx", index=True, engine="openpyxl")

    print("抓取完毕")


def main():
    test1()


if __name__ == "__main__":
    main()
