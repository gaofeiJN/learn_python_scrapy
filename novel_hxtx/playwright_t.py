import random
import pprint
from playwright.sync_api import sync_playwright


def scrape_fanqie_novel(novel_url: str, max_chapters: int = 10):
    """
    爬取番茄小说指定小说的目录和章节内容

    Args:
        novel_url: 小说详情页 URL
        max_chapters: 最大爬取章节数，防止无限爬取
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

        # ---------- 2.2 获取章节目录 ----------
        print(f"[*] 正在打开小说页面: {novel_url}")
        page.goto(novel_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(random.randint(2000, 4000))  # 随机等待，模拟真人

        # 等待目录区域加载完成
        try:
            page.wait_for_selector("div.volume", timeout=15000)
        except Exception:
            print("[!] 未找到目录容器，请检查页面结构是否变化")
            browser.close()
            return

        # 提取章节链接
        chapter_items = page.locator("div.volume ul.cf li a").all()
        if not chapter_items:
            print("[!] 未提取到章节链接")
            browser.close()
            return

        chapters = []
        for item in chapter_items[:max_chapters]:
            title = item.inner_text().strip()
            href = item.get_attribute("href")
            if href:
                chapters.append(
                    {"title": title, "url": f"https://www.hongxiu.com{href}"}
                )

        print(f"[+] 共获取到 {len(chapters)} 个章节")
        pprint.pprint(chapters)

        # ---------- 2.3 逐章爬取内容 ----------
        for idx, chapter in enumerate(chapters, start=1):
            print(f"[{idx}/{len(chapters)}] 正在爬取: {chapter['title']}")

            try:
                # 构建完整 URL（如果是相对路径）
                full_url = chapter["url"]
                if not full_url.startswith("http"):
                    full_url = f"https://www.hongxiu.com{full_url}"

                page.goto(full_url, wait_until="domcontentloaded", timeout=30000)
                # 模拟阅读行为：随机停留 1~3 秒
                page.wait_for_timeout(random.randint(1000, 3000))

                # 提取正文内容（CSS 选择器需根据实际页面调整）
                content_elements = page.locator("div.ywskythunderfont p").all()
                content = "\n".join([el.inner_text() for el in content_elements])

                if content:
                    # 保存到文件（可根据需要改为数据库存储）
                    filename = f"{idx:04d}_{chapter['title']}.txt"
                    # 清理文件名中的非法字符
                    filename = "".join(
                        c for c in filename if c.isalnum() or c in "._- "
                    )
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"{chapter['title']}\n\n{content}")
                    print(f"    [✓] 已保存: {filename} ({len(content)} 字)")
                else:
                    print(f"    [!] 未提取到正文内容，可能选择器需要更新")

            except Exception as e:
                print(f"    [✗] 爬取失败: {e}")
                continue

        print(f"\n[完成] 共成功爬取 {len(chapters)} 章")
        browser.close()


# ---------- 2.4 调用示例 ----------
if __name__ == "__main__":
    # 替换为任意番茄小说详情页 URL
    novel_page = "https://www.hongxiu.com/book/12394139504487203#Catalog"
    scrape_fanqie_novel(novel_page, max_chapters=15)
