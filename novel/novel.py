import requests  # 第三方的模块
import parsel  # 第三方的模块
import os  # 内置模块 文件或文件夹


def main():
    filename = "./小说/"
    if not os.path.exists(filename):
        os.mkdir(filename)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }

    with open(filename + "聚宝仙盆.txt", mode="a", encoding="utf-8") as f:
        for ctr in range(1, 1745):
            # for ctr in range(1, 2):
            url = f"https://apibi.cc/api/chapter?id=192838&chapterid={ctr}"

            try:
                response = requests.get(url=url, headers=headers)
                res = response.json()
                # print(res)

                f.write(res["chaptername"] + "\n\n")
                f.write(res["txt"] + "\n\n")
                print("已下载章节:  ", res["chaptername"])
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
