import json
from jueJin.db.dataManager import DataManager
import re
import requests

# 实例化对象
db = DataManager()


def getContent(link):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": link,
        "Content-Type": "application/json",
        "Origin": "https://juejin.im",
        "Connection": "keep-alive",
        "TE": "Trailers"
    }
    # 需要传入一个 article_id 进去，这个很重要
    payloadData = {
        "article_id": link.split("/")[-1]
    }
    postUrl = "https://apinew.juejin.im/content_api/v1/article/detail"
    dumpJsonData = json.dumps(payloadData)
    r = requests.post(postUrl, headers=header, data=dumpJsonData, timeout=25)
    data = json.loads(r.content.decode("utf-8"))['data']
    title = data['article_info']['title']
    content = data['article_info']['content']

    dataDB = (title, content)
    db.saveContent(dataDB)


def main():
    linkUrlList = db.getData()
    # linkUrlList 格式如下：linkUrlList = [["https://juejin.im/post/6844904144533192717"]]
    count = 1
    for i in range(len(linkUrlList)):
        link = linkUrlList[i][0]
        # 通过正则表达式筛选出一些不标准的 url
        # 标准 url 例如 https://juejin.im/post/6844904144533192717
        result = re.search(pattern='https://juejin.im/post/[0-9]+', string=link)
        if result is not None:
            print("正在进行第", count, "个 link")
            count = count + 1
            getContent(link)


if __name__ == '__main__':
    main()
