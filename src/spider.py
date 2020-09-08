# Author:山楂树下的小笨蛋
# -*- codeing = utf-8 -*-
# @Time :2020/4/21 16:56
# @Site :
# @File :spider.py
# @Software: PyCharm
import code

import bs4  # 网页解析 获取数据
import re  # 正则表达式 进行文字匹配
import urllib.request, urllib.error  # 制定URL 获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行sqlite数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="  # 路径
    # 1,爬取网页
    datalist = getData(baseurl)
    # 2,逐一解析数据
    savapath = ".\\豆瓣电影top250.xls"
    saveData(datalist, savapath)
    # 3,保存数据  放在MySQL 或者 excel


findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象， 表示规则(字符串得模式)
findimg = re.compile(r'<img.*src="(.*?)"', re.S)  # 忽略换行符
findtitle = re.compile(r'<span class="title">(.*)</span>')  # 头
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 多少人评价
findInq = re.compile(r'<span class="inq">(.*)</span>')  # 简介
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    # 2,逐一解析数据
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', "item"):
            # print(item) # 测试 ：查看电影中得item全部信息
            data = []  # 保存一部电影得所有得信息
            item = str(item)

            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定得字符串
            data.append(link)
            print(link)

            imgSrc = re.findall(findimg, item)[0]
            data.append(imgSrc)

            titles = re.findall(findtitle, item)
            if len(titles) == 2:
                castle = titles[0]
                data.append(castle)
                odille = titles[1].replace("/", " ")
                data.append(odille)
            else:
                data.append(titles[0])
                data.append(' ')  # 空也要留着

            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", " ")  # 去掉句号
                data.append(inq)
            else:
                data.append("  ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())  # 去掉前后的空格
            # print("data=======================================================================================================")
            datalist.append(data)
            # print(data)
            # print(len(datalist))
    print(len(datalist))
    return datalist


# 专门得到指定一个url的网页信息
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e, code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 3,保存数据  放在MySQL 或者 excel
def saveData(datalist, savapath):
    print("===============================================================================")
    book = xlwt.Workbook(encoding="utf-8")  # 文件
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情连接", "图片连接", "影片中文名", "影片英文名", "评价数", "评分", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % i)
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])

    book.save(savapath)


if __name__ == "__main__":
    main()
    print('爬取完成')
