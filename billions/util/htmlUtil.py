import datetime
import re


def imiao(htmlContent:str, wordCount:int=150)->str:

    #截取制定长度的字符串
    html =htmlContent[:wordCount]
    # 从右到左获取一段完整的句子
    if "。" in html:
        html = html[:html.rindex("。")+1]
    elif "!" in html:
        html = html[:html.rindex("!") + 1]
    elif "；" in html:
        html = html[:html.rindex("；") + 1]
    elif ";" in html:
        html = html[:html.rindex(";") + 1]
    # elif "，" in html:
    #     html = html[:html.rindex("，") + 1]
    # elif "," in html:
    #       html = html[:html.rindex(",") + 1]
    else:  # 如果实在没有标点符号，那么末尾添加省略号
        html = html+"……"
    return html

def splitHtmlBy5000(html:str) -> []:
    # f = open("F:/billions/quotes-1.html",encoding="utf-8")
    # html = f.read()
    # # print(html)
    # total = len(html)
    # print(total)
    strs = []
    if(len(html)<4900):
        strs.append(html)
        return strs

    while len(html) > 5000:
        words = imiao(html,4900)
        strs.append(words)
        html = html[len(words):]
    strs.append(html)
    return strs


def noHtml(htmlContent:str) -> str:
    # 对文章进行 nohtml 处理
    html_content = re.sub(r"<(.[^>]*)>", "", htmlContent)
    html_content = re.sub(r"\r", "", html_content)
    html_content = re.sub(r"\t", "", html_content)
    #
    # for i in range(20):
    #     html_content = re.sub(r"  ", " ", html_content)
    html_content = re.sub(r"\x20+","",html_content)
    return html_content


def getChineseWord(res):
    s = res.replace('%', r'\x')
    b = eval('b' + '\'' + s + '\'')
    word = b.decode('utf-8')
    return word


def getwjj():

    current_time = datetime.datetime.now()
    str_date_time = current_time.strftime("%Y%m%d%H%M%S%f")
    return str_date_time