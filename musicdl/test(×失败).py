import httpx
import time
from pathlib import Path


def dl_song(title: str, song_id: str, save_dir: str = ".") -> bool:
    """
    下载网易云音乐单曲 MP3
    :param title: 歌曲标题，用于保存文件名
    :param song_id: 歌曲数字ID（如 '16343629'）
    :param save_dir: 保存目录，默认当前
    """
    base_url = "http://music.163.com/song/media/outer/url"

    # 关键：设置合法的来源头，模拟从官网播放页发起请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "http://music.163.com/",  # 必须存在
        "Cookie": "MUSIC_A_T=1502981628928; MUSIC_R_T=1502981672544; nts_mail_user=16605315936@163.com:-1:1; NTES_P_UTID=sI9oauoAJQWThBeWf5RPkLORbgmCsI1s|1776382105; NTES_PASSPORT=cju81Wa8R.s_BWdXSWjVoBM2TlOuFBZEjStqLAk6paSMpvFRpWZ9_i3AF_REdbSjWREaHKDiDYC5dniMdj7UsQ2fro8sFd18Mo8z5.LK0wq3BMCX0B9sTdG6sACN9U4xdt97gG6asu3TqWJMlmcdPI6W8bGNR2d6cyKf1Yk1a3VOLWJkOIBDwpyPyszvMkNfc; P_INFO=m16605315936@163.com|1776382105|1|mail163|00&99|shd&1773764669&mail163#shd&370100#10#0#0|166936&1||16605315936@163.com; NTES_CMT_USER_INFO=1233763192%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B19yrJU%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CbTE2NjA1MzE1OTM2QDE2My5jb20%3D; _ga=GA1.1.1392228544.1778508656; _clck=8kn45c%5E2%5Eg5y%5E0%5E2322; _ga_PTGVM6PCHS=GS2.1.s1778508656$o1$g0$t1778508670$j46$l0$h0; NMTID=00OrhfPgvoCqEkqGk9bqcKUFt9FpC8AAAGeJrtn9Q; _iuqxldmzr_=32; _ntes_nnid=379a9f25e50e5d617ca9194218788be5,1778769267289; _ntes_nuid=379a9f25e50e5d617ca9194218788be5; Hm_lvt_1483fb4774c02a30ffa6f0e2945e9b70=1778769267; HMACCOUNT=F81D6EB19BF3CB15; WEVNSM=1.0.0; WNMCID=enhqmv.1778769267627.01.0; sDeviceId=YD-GOk2mArlqRNEAxRQAUbW6AhtqdIHLQpt; __csrf=3d2fd0d39da39156228a255bfd4d1067; MUSIC_U=0066CE2A823B14BFC995D0F6681E32E8A7D0B56AC79D902C55EF1AC31A68427853C75E798D189314EFB1F5C917C32564C08CB28E99D1266A5FC3C2192DC6C78FD1D00D1304DA756F7D823BE232507680046BDCB603B6178D7D3F35E37D729DC05E80B373BF7429685350BD550E360E551A054777EF8F932ABEAEDFC1F0E6D284752912137BC5AC16D587558C2D87A9BEC714CC37BFE8900727648E344CF7461EB2BECC4FF243CA68558FBE0B09C7179D8D713E2E7407AE8FEFE881EB22D8946B84FAF4FF13635FF2D27D63722369437D104B1B3226805CCAB3B6EC942673B1334942D72423E77F43E8DA05F4B09B37C414A261DD5E3554220ADCCC54F9FF239794B8464528E19800F8DB8AA71972AF55F2A3C3B702CF815559D48855DCF3D01F9F0A83B8F4B5CCCCCDDFFA032F21484400C0BDBEB46931B57F1E06862B3A213E407B0E7817346D506C6554D4278CEBB92B12E7E6014E5B5835F66FD91D10116FE42788EF919AA28FB2E64260E59930D6F0FF97A4769B555C5001AB06A9FA9E436234204822F8F8B29D0B86E713CE7C913E; ntes_kaola_ad=1; JSESSIONID-WYYY=GqCIK%2ByajpFo0js%2Fx%5CDspN13Mz6qJl9Hg%2BTYlaW7KBcY0%2FyTRZG4TAg5ApMvvv7U9YV83o75KXFWlYv8heexf31eV%2F0xm%2FEB0X3Ejtz%2BrA%2B1Bs%2FvGjxsNp6hsMP373KHZ41k0fycOkWyKnBH7PAbKxwcntmS43O11ty3EeDuYNz%5CKsIq%3A1778772807246; Hm_lpvt_1483fb4774c02a30ffa6f0e2945e9b70=1778771247",
    }

    params = {"id": song_id}  # 只传纯数字 ID，不加 .mp3

    try:
        # 注意：这里直接 get 即可，follow_redirects 默认为 True（httpx 默认跟随）
        # stream 模式并非必须，小文件可直接读取全部内容
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            res = client.get(base_url, headers=headers, params=params)

        # 检查 HTTP 状态
        if res.status_code != 200:
            print(f"【错误】状态码异常：{res.status_code}")
            return False

        # 检查 Content-Type，确保是音频
        content_type = res.headers.get("Content-Type", "")
        if "audio" not in content_type:
            print(f"【错误】响应非音频类型（{content_type}），可能被拦截")
            # 可选打印前200字节看具体错误信息
            print(res.text[:200])
            return False

        # 保存文件
        timestamp = time.strftime("%H%M%S", time.localtime())
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "_", "-")
        ).strip()
        file_name = f"{safe_title}_{timestamp}.mp3"
        file_path = Path(save_dir) / file_name

        file_path.write_bytes(res.content)
        print(f"【成功】已保存至：{file_path}")
        return True

    except httpx.ReadTimeout:
        print("【错误】请求超时")
        return False
    except Exception as e:
        print(f"【错误】{e}")
        return False


if __name__ == "__main__":
    dl_song(title="Outlaws of Love - Adam Lambert", song_id="16343629")  # 注意：纯数字
