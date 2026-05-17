import httpx
import time

# from rich import print
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"

# headers = {
#     "User-Agent": USER_AGENT,
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "Referer": "http://music.163.com/",
#     "Origin": "https://music.163.com",
#     "X-Requested-With": "XMLHttpRequest",
#     "Origin": "http://m801.music.126.net/",
# }
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": "http://music.163.com/",
    "Origin": "https://music.163.com",
    "Cookie": "nts_mail_user=16605315936@163.com:-1:1; NTES_P_UTID=sI9oauoAJQWThBeWf5RPkLORbgmCsI1s|1776382105; NTES_PASSPORT=cju81Wa8R.s_BWdXSWjVoBM2TlOuFBZEjStqLAk6paSMpvFRpWZ9_i3AF_REdbSjWREaHKDiDYC5dniMdj7UsQ2fro8sFd18Mo8z5.LK0wq3BMCX0B9sTdG6sACN9U4xdt97gG6asu3TqWJMlmcdPI6W8bGNR2d6cyKf1Yk1a3VOLWJkOIBDwpyPyszvMkNfc; P_INFO=m16605315936@163.com|1776382105|1|mail163|00&99|shd&1773764669&mail163#shd&370100#10#0#0|166936&1||16605315936@163.com; NTES_CMT_USER_INFO=1233763192%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B19yrJU%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CbTE2NjA1MzE1OTM2QDE2My5jb20%3D; _ga=GA1.1.1392228544.1778508656; _clck=8kn45c%5E2%5Eg5y%5E0%5E2322; _ga_PTGVM6PCHS=GS2.1.s1778508656$o1$g0$t1778508670$j46$l0$h0; NMTID=00OrhfPgvoCqEkqGk9bqcKUFt9FpC8AAAGeJrtn9Q; JSESSIONID-WYYY=ECfau0S0w94mv0f%2BS3K%2Fa4qqGA5AU9I%2BaJS5xUoagcOkWg7%2BdQ6cHTvVpOZDunckGNPtCJ9ytV%2B1ynM0%5Cl4vxEgmmzmYnNZW1xCj8fGk2DXYgJutRCri%2BWDkNTyogQBKc7eEOvtmHw0KSyu36qNCV6nNwxVU5E4vzTEG6I4SubIUVkAH%3A1778771067222; _iuqxldmzr_=32; _ntes_nnid=379a9f25e50e5d617ca9194218788be5,1778769267289; _ntes_nuid=379a9f25e50e5d617ca9194218788be5; Hm_lvt_1483fb4774c02a30ffa6f0e2945e9b70=1778769267; HMACCOUNT=F81D6EB19BF3CB15; WEVNSM=1.0.0; WNMCID=enhqmv.1778769267627.01.0; __snaker__id=H4dFyfy6gVUTzOhR; ntes_utid=tid._.mlAX5c1H8BVAVhERAAeHuQg56NIWPF95._.0; WM_NI=5Q6gIc0EUwy2gapKCdJt9bQhADrs7GL8xfesFhXGR20vPxe%2BFWe7AHnM7fy2keCPA7lms%2Bcvt39qsPC0UXb70meqWQpDeqeEbZP%2B9IlZr%2FJMDYdgzhCleDwJ%2BHM53r6XNWU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee94b13c949aa5d2ef3bf48a8fb7d14a828e8bb0db7f96b5bd97cc6995919997b12af0fea7c3b92af78ffa88cc69f49b9b98fc3aa5bfc0acc2708aacf783d464839cbe94b64d90e8b887e87986b898a8d13af4aaa099e8218689abd8c444ae93f987fc3aa9bb8db1c43db0b3bdcce27eb8edf792f25c81f09bb9e13df4b3ab92d65bb49cab92e84fa286a0ccbc43b086bed0c9478887ac88f96481b4aba5f642e99883d6b27af68882b8d837e2a3; sDeviceId=YD-GOk2mArlqRNEAxRQAUbW6AhtqdIHLQpt; __csrf=3d2fd0d39da39156228a255bfd4d1067; MUSIC_U=0066CE2A823B14BFC995D0F6681E32E8A7D0B56AC79D902C55EF1AC31A68427853C75E798D189314EFB1F5C917C32564C08CB28E99D1266A5FC3C2192DC6C78FD1D00D1304DA756F7D823BE232507680046BDCB603B6178D7D3F35E37D729DC05E80B373BF7429685350BD550E360E551A054777EF8F932ABEAEDFC1F0E6D284752912137BC5AC16D587558C2D87A9BEC714CC37BFE8900727648E344CF7461EB2BECC4FF243CA68558FBE0B09C7179D8D713E2E7407AE8FEFE881EB22D8946B84FAF4FF13635FF2D27D63722369437D104B1B3226805CCAB3B6EC942673B1334942D72423E77F43E8DA05F4B09B37C414A261DD5E3554220ADCCC54F9FF239794B8464528E19800F8DB8AA71972AF55F2A3C3B702CF815559D48855DCF3D01F9F0A83B8F4B5CCCCCDDFFA032F21484400C0BDBEB46931B57F1E06862B3A213E407B0E7817346D506C6554D4278CEBB92B12E7E6014E5B5835F66FD91D10116FE42788EF919AA28FB2E64260E59930D6F0FF97A4769B555C5001AB06A9FA9E436234204822F8F8B29D0B86E713CE7C913E; ntes_kaola_ad=1; WM_TID=Gts35gKAUiZFUFFEBQfC%2BRw96MISZx%2Fl; gdxidpyhxdE=32PVRkwhcefQklpiV%5CyTe5U%5COAlu%5C9qHLETYHCIp6q%2FA550NGr%2BHeG9AV%5C9gmnm3dTM%2Fw%2Fhb95q%5CmdQrakRswdT0qETSoXAO8GHnUSAJ0mUYw5U1uw%2BET8XgBKZfVR4LZalXtHG%2BRvEVKKCyu51yoeiys1fTEn7%2Bh%5CSMUIH11n1KHIUq%3A1778771011461; Hm_lpvt_1483fb4774c02a30ffa6f0e2945e9b70=1778770946",
}


def dl_song(title: str, url: str) -> bool:
    # 返回值
    success = True

    # 尝试抓取
    try:
        # 下载速度较慢, 设置超时时间为20秒
        # 自动跟随重定向
        # res = httpx.get(
        #     url=url,
        #     headers=headers,
        #     params=parameters,
        #     timeout=20,
        #     follow_redirects=True,
        # )
        res = httpx.get(
            url=url,
            headers=headers,
            timeout=20,
            follow_redirects=True,
        )

        # 检查请求是否成功
        if res.status_code == 200:
            print(f"【dl_info】{url}页面获取成功！")
        else:
            print(f"【dl_info】{url}请求失败，状态码：{res.status_code}")
            success = False
            return success

    # 处理超时
    except httpx.ReadTimeout:
        print(f"【dl_info】{url} : 请求超时")
        success = False
        return success

    # 即使返回了状态码200, 仍要做其他检查
    # 检查 Content-Type，确保是音频
    content_type = res.headers.get("Content-Type", "")
    if "audio" not in content_type:
        print(f"【错误】响应非音频类型（{content_type}），可能被拦截")
        # 可选打印前200字节看具体错误信息
        print(res.text[:300])
        return False

    # 保存mp3文件
    file_name = f"{title}_{time.strftime('%H%M%S', time.localtime())}.mp3"
    file_path = Path(file_name)

    with open(file_path, "wb") as mp3:
        mp3.write(res.content)

    # 返回
    return success


def main():
    # dl_song(
    #     "outlaws of love_Adam Lambert",
    #     "http://music.163.com/song/media/outer/url",
    #     "16343629",
    # )
    # dl_song(
    #     "outlaws of love_Adam Lambert",
    #     "http://m801.music.126.net/20260514233241/037901d5aafc1caab4fc40c5e13e362b/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/36254441371/0750/4913/7e9b/8f299c29730a6c71689e38cc020a218f.mp3?vuutv=47dpTIoywq+d2S23XYDZVwRaaTZe/2kFWUTyYOOJT5ikvJFxRWBnFimNVv4PRWm0LqMACHR10E4rITLgdBtADOGdY1SmeGMrSXuqjGe5EH4=&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9zdGFuZGFyZA",
    #     "16343629",
    # )

    # 下载vip音乐失败，可以下载非vip音乐
    dl_song(
        "outlaws of love_Adam Lambert",
        "http://music.163.com/song/media/outer/url?id=2160311940.mp3",
        "16343629",
    )


if __name__ == "__main__":
    main()
