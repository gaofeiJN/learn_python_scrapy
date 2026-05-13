import parsel
from rich import print


def test1():
    with open("sample.html", "r", encoding="utf-8") as f:
        html_text = f.read()

    sel = parsel.Selector(html_text)

    # xpath(
    #   query: str,
    #   namespaces: Mapping[str, str] | None = None,
    #   **kwargs: Any)
    #   -> SelectorList[Selector]

    # xpath()返回的是SelectorList类型
    p1 = sel.xpath('//div[@class="son2"]/p[br]')
    # [<Selector query='//div[@class="son2"]/p[br]' data='<p>床前明月光，疑是地上霜。<br>举头望明月，低头思故乡。<br></p>'>]
    # print(p1)

    # get(default: None = None) -> (str | None)
    # 提取第一个匹配的文本（自动处理多个文本节点）
    # <p>床前明月光，疑是地上霜。<span>hello world</span><br>举头望明月，低头思故乡。<br></p>
    print(p1.get())

    # getall() -> list[str]
    # 返回列表
    p2 = sel.xpath("//div[@class='lright']/div")
    print(p2.getall())
    # [
    #     '<div style="width:25.742574257426%;" class="percent"></div>',
    #     '<div style="width:21.782178217822%;" class="percent"></div>',
    #     '<div style="width:5.9405940594059%;" class="percent"></div>',
    #     '<div style="width:7.9207920792079%;" class="percent"></div>',
    #     '<div style="width:38.613861386139%;" class="percent"></div>'
    # ]

    # text() 只提取直接子文本节点
    # ['床前明月光，疑是地上霜。', '举头望明月，低头思故乡。']
    p3 = sel.xpath('//div[@class="son2"]/p[br]/text()')
    print(p3.getall())

    # Selector对象
    s1 = sel.xpath('//div[@class="son2"]/p[br]')[0]
    # <p>床前明月光，疑是地上霜。<span>hello world</span><br>举头望明月，低头思故乡。<br></p>
    # print(s1)

    # <p>床前明月光，疑是地上霜。<span>hello world</span><br>举头望明月，低头思故乡。<br></p>
    # print(s1.get())

    # ['<p>床前明月光，疑是地上霜。<span>hello world</span><br>举头望明月，低头思故乡。<br></p>']
    # print(s1.getall())

    # [<Selector query='string()' data='床前明月光，疑是地上霜。hello world举头望明月，低头思故乡。'>]
    # print(s1.xpath("string()"))
    
    # ['床前明月光，疑是地上霜。hello world举头望明月，低头思故乡。']
    print(s1.xpath("string()").getall())


def main():
    test1()


if __name__ == "__main__":
    main()
