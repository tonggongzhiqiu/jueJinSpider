import json
import requests
from jueJin.db.dataManager import DataManager
import time

# 实例化数据库对象
db = DataManager()
# 这几个列表其实用处不大，只是在后边用了一下 link 做了一个去重
titleList = []
articleIdList = []
linkUrlList = []
userNameList = []
briefContentList = []


def getData(key, nextCursor="0"):
    # 请求中需要的值
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://juejin.im/search?query=" + key,
        "Content-Type": "application/json",
        "Origin": "https://juejin.im",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_93bbd335a208870aa1f296bcd6842e5e=1585649229,1587023263; gr_user_id=7ff105a2-c311-4b09-8e5c-863db5cd60e9; _ga=GA1.2.1122042631.1585649230; MONITOR_WEB_ID=2c1db46d-5304-448e-bc50-bf8468205920; _gid=GA1.2.922206982.1599204376; passport_auth_status=897f38c36d5cb93bb74a60a160e95ab4%2C; sid_guard=8484d7c1ac371660428a885a45eb3c65%7C1599207068%7C5184000%7CTue%2C+03-Nov-2020+08%3A11%3A08+GMT; uid_tt=0663d12bb072ab748608a59eabe192f3; uid_tt_ss=0663d12bb072ab748608a59eabe192f3; sid_tt=8484d7c1ac371660428a885a45eb3c65; sessionid=8484d7c1ac371660428a885a45eb3c65; sessionid_ss=8484d7c1ac371660428a885a45eb3c65",
        "TE": "Trailers",
    }
    payloadData = {
        "key_word": key,
        "id_type": 0,
        "cursor": nextCursor,
        "limit": 20,
        "search_type": 0
    }

    # 掘金在滚动条时发送的请求地址
    postUrl = "https://apinew.juejin.im/search_api/v1/search"
    timeout = 25
    dumpJsonData = json.dumps(payloadData)
    r = requests.post(postUrl, headers=header, data=dumpJsonData, timeout=timeout)
    data = json.loads(r.content.decode("utf-8"))
    contents = data['data']
    nextCursor = data['cursor']

    for i, content in enumerate(contents):
        resultType = content['result_type']
        if resultType == 2:
            # hasMore = data['has_more']
            title = content['result_model']['article_info']['title']
            linkUrl = content['result_model']['article_info']['link_url']
            userName = content['result_model']['author_user_info']['user_name']
            briefContent = content['result_model']['article_info']['brief_content']

            if linkUrl not in linkUrlList:
                print("title: ", title)
                print("userName: ", userName)
                print("briefContent: ", briefContent)
                print("link: ", linkUrl)
                titleList.append(title)
                userNameList.append(userName)
                briefContentList.append(briefContent)
                linkUrlList.append(linkUrl)

                data = (title, userName, briefContent, linkUrl)
                db.saveBriefInfo(data)
            else:
                print("Warning: ", title, "and ", linkUrl)
                # print("userName: ", userName)
                # print("content: ", briefContent)
    print("len(linkUrlList)", len(linkUrlList), "cursor", nextCursor)
    # return hasMore, nextCursor
    return nextCursor


def main():
    key = input("请输入要搜索的关键词")
    nextCursor = getData(key)
    # 这里建议使用 hasmore 来控制，爬取的内容少的话可以自行设置
    count = 2
    while count < 51:
        print('循环开始')
        nextCursor = getData(key, nextCursor)
        count = count + 1
        print("第", count, "次循环结束...")
        print("####################################")
        time.sleep(2)


if __name__ == '__main__':
    main()
