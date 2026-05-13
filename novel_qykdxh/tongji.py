from pathlib import Path


def main():
    novels = Path("./小说")

    print(f"{novels} is a directory : {novels.is_dir()}")

    # 遍历文件夹
    with open("./小说/list.txt", "w", encoding="utf-8") as f:
        for p in novels.iterdir():
            if p.is_file():
                f.write(f"{p} \n")


main()
