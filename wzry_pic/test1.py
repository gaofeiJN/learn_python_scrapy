from pathlib import Path
import pprint
from playwright.sync_api import sync_playwright
import random


def test1():
    folder = Path("./pictures")

    hero_set = set()
    for file in folder.iterdir():
        # pictures\上官婉儿_修竹墨客.jpg 上官婉儿_修竹墨客.jpg 上官婉儿_修竹墨客 .jpg
        # print(file, file.name, file.stem, file.suffix)
        # break
        hero_name = file.stem.split("_")[0]
        hero_set.add(hero_name)
    pprint.pprint(hero_set)


def scrape_wzry_pic(url: str):
    """
    爬取王者荣耀图片

    Args:
        url: 图片详情页 URL
    """
    with sync_playwright() as p:
        # ---------- 2.1 启动浏览器 ----------
        # 关键：关闭无头模式或添加反检测参数，降低被封风险
        browser = p.chromium.launch(
            headless=False,  # 调试阶段建议有头模式；稳定后可改为 True
            args=[
                "--disable-blink-features=AutomationControlled",  # 隐藏自动化标记
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        # 注入 JS 隐藏 webdriver 特征（关键反爬措施）
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        # 重新下载貂蝉图片
        print(f"正在爬取: {url}")

        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )
            # 模拟阅读行为：随机停留 1~3 秒
            page.wait_for_timeout(random.randint(1000, 3000))

            # 英雄名称提取（CSS 选择器需根据实际页面调整）
            hero_title = page.locator("div.cover h2.cover-name").inner_text().strip()

            # 提取图片链接（CSS 选择器需根据实际页面调整）
            pic_elements = page.locator("ul.pic-pf-list li i img").all()
            pics = [
                {
                    "pic_title": el.get_attribute("data-title"),
                    "pic_url": el.get_attribute("data-imgname"),
                }
                for el in pic_elements
            ]

            # 抓取图片
            for pic in pics:
                if not pic["pic_url"].startswith("http"):
                    pic["pic_url"] = f"https:{pic['pic_url']}"
                res = page.request.get(pic["pic_url"])
                if res.ok:
                    # 保存图片
                    filename = f"./pictures/{hero_title}_{pic['pic_title']}.jpg"
                    with open(filename, "wb") as f:
                        f.write(res.body())
                    print(f"图片已保存为: {filename}")
                else:
                    print(f"下载失败，状态码: {res.status}")

        except Exception as e:
            print(f"    [✗] 爬取失败: {e}")

        browser.close()


def main():
    # test1()
    # 重新下载貂蝉图片
    scrape_wzry_pic("https://pvp.qq.com/web201605/herodetail/diaochan.shtml")


if __name__ == "__main__":
    main()
