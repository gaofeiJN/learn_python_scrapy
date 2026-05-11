import requests
import random
import lxml
import time
from bs4 import BeautifulSoup

# User-Agent池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
]

# 设置请求头
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

url = "https://books.toscrape.com/"


def test2():
    # 1. 创建一个 Session 对象
    session = requests.Session()

    # 2. （可选）为 Session 设置默认的请求头，所有请求都会带上
    session.headers.update(headers)

    # 3. 假设这是一个登录接口（实际 URL 和参数以目标网站为准）
    login_url = "https://example.com/login"
    login_data = {"username": "your_username", "password": "your_password"}

    # 发送 POST 登录请求
    login_resp = session.post(login_url, data=login_data)
    print("登录状态码：", login_resp.status_code)

    # 4. 登录成功后，使用同一个 Session 访问需要登录才能看到的页面
    time.sleep(2)  # 每隔2秒发送一次请求
    profile_url = "https://example.com/user/profile"
    profile_resp = session.get(profile_url)

    # 此时的响应已经包含了登录后的内容（因为 Session 自动携带了登录后的 Cookie）
    print("个人资料页长度：", len(profile_resp.text))

    # 5. 可以继续用同一个 Session 发起更多请求，所有 Cookies 都会自动维持
    time.sleep(2)  # 每隔2秒发送一次请求
    another_url = "https://example.com/dashboard"
    dashboard_resp = session.get(another_url)


def main():
    test2()


if __name__ == "__main__":
    main()
