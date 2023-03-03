import re


def imiao(htmlContent:str, wordCount:int=150)->str:

    #截取制定长度的字符串
    html =htmlContent[:wordCount]
    # 从右到左获取一段完整的句子
    if "。" in html:
        html = html[:html.rindex("。")+1]
    elif "." in html:
        html = html[:html.rindex(".") + 1]
    elif "!" in html:
        html = html[:html.rindex("!") + 1]
    elif "；" in html:
        html = html[:html.rindex("；") + 1]
    elif ";" in html:
        html = html[:html.rindex(";") + 1]
    elif "，" in html:
        html = html[:html.rindex("，") + 1]
    elif "," in html:
          html = html[:html.rindex(",") + 1]
    else:  # 如果实在没有标点符号，那么末尾添加省略号
        html = html+"……"
    return html


def noHtml(htmlContent:str) -> str:
    # 对文章进行 nohtml 处理
    html_content = re.sub(r"<(.[^>]*)>", "", htmlContent)
    html_content = re.sub(r"\r", "", html_content)
    html_content = re.sub(r"\t", "", html_content)

    for i in range(20):
        html_content = re.sub(r"  ", " ", html_content)
    return html_content










