import httpx
import traceback
from rich import print

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"

headers = {
    "x-requested-with": "XMLHttpRequest",
}

url = "https://musicjx.com/"


def dl_info(song: str, page: int = 1) -> tuple[bool, list[dict]]:
    # 返回值
    success = True
    info = []

    # 尝试抓取
    try:
        data = {}
        data["input"] = song
        data["filter"] = "name"
        data["type"] = "netease"
        data["page"] = page

        # 下载速度较慢, 设置超时时间为20秒
        res = httpx.post(url=url, headers=headers, data=data, timeout=20)

        # 检查请求是否成功
        if res.status_code == 200:
            print(f"【dl_info】{url}页面获取成功！")
        else:
            print(f"【dl_info】{url}请求失败，状态码：{res.status_code}")
            success = False
            return success, info

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【dl_info】{url} : 请求超时")
        success = False
        return success, info

    # 其他异常
    except Exception:
        traceback.format_exc()
        success = False
        return success, info

    # 解析返回的json字符串
    result = res.json()

    # 返回值中有 code, error 字段, 此处再做一次检查
    if result["code"] != 200 or result["error"] != "":
        print(
            f"【dl_info】{url} : 检测到抓取结果发生错误， code = {result['code']}, error = {result['error']}"
        )
        success = False
        return success, info

    # 解析返回值中的 data
    for item in result["data"]:
        d = {}
        d["title"] = item["title"]
        d["author"] = item["author"]
        d["url"] = item["url"]
        info.append(d)
        print(d)

    # 返回
    return success, info


def main():
    dl_info("outlaws of love")


if __name__ == "__main__":
    main()
