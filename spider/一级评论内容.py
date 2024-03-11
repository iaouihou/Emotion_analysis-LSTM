import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import json

# 设置为自己的cookies
cookies = {
    'SINAGLOBAL': '1278126679099.0298.1694199077980',
    'SCF': 'ApDYB6ZQHU_wHU8ItPHSso29Xu0ZRSkOOiFTBeXETNm7k7YlpnahLGVhB90-mk0xFNznyCVsjyu9-7-Hk0jRULM.',
    'SUB': '_2A25IaC_CDeRhGeFO61AY8i_NwzyIHXVrBC0KrDV8PUNbmtAGLVLckW9NQYCXlpjzhYwtC8sDM7giaMcMNIlWSlP6',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mzQcPEhHvorRG-l7.BSsy5JpX5KzhUgL.FoM7ehz4eo2p1h52dJLoI0qLxK-LBKBLBKMLxKnL1--L1heLxKnL1-qLBo.LxK-L1KeL1KzLxK-L1KeL1KzLxK-L1KeL1Kzt',
    'ALF': '1733137172',
    '_s_tentry': 'weibo.com',
    'Apache': '435019984104.0236.1701606621998',
    'ULV': '1701606622040:13:2:2:435019984104.0236.1701606621998:1701601199048',
}

# 开始页码，不用修改
page_num = 0


def get_content_1(uid, mid, the_first=True, max_id=None):
    headers = {
        'authority': 'weibo.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'client-version': 'v2.43.30',
        'referer': 'https://weibo.com/1762257041/NiSAxfmbZ',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'server-version': 'v2023.09.08.4',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'F2EEQZrINBfzB2HPPxqTMQJ_',
    }

    params = {
        'is_reload': '1',
        'id': f'{mid}',
        'is_show_bulletin': '2',
        'is_mix': '0',
        'count': '20',
        'uid': f'{uid}',
        'fetch_level': '0',
        'locale': 'zh-CN',
    }

    if not the_first:
        params['flow'] = 0
        params['max_id'] = max_id
    else:
        pass
    response = requests.get('https://weibo.com/ajax/statuses/buildComments', params=params, cookies=cookies,
                            headers=headers)
    return response


def get_content_2(get_content_1_url):
    headers = {
        'authority': 'weibo.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryNs1Toe4Mbr8n1qXm',
        'origin': 'https://weibo.com',
        'referer': 'https://weibo.com/1762257041/NiSAxfmbZ',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'x-xsrf-token': 'F2EEQZrINBfzB2HPPxqTMQJ_',
    }

    s = '{"name":"https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4944997453660231&is_show_bulletin=2&is_mix=0&max_id=139282732792325&count=20&uid=1762257041&fetch_level=0&locale=zh-CN","entryType":"resource","startTime":20639.80000001192,"duration":563,"initiatorType":"xmlhttprequest","nextHopProtocol":"h2","renderBlockingStatus":"non-blocking","workerStart":0,"redirectStart":0,"redirectEnd":0,"fetchStart":20639.80000001192,"domainLookupStart":20639.80000001192,"domainLookupEnd":20639.80000001192,"connectStart":20639.80000001192,"secureConnectionStart":20639.80000001192,"connectEnd":20639.80000001192,"requestStart":20641.600000023842,"responseStart":21198.600000023842,"firstInterimResponseStart":0,"responseEnd":21202.80000001192,"transferSize":7374,"encodedBodySize":7074,"decodedBodySize":42581,"responseStatus":200,"serverTiming":[],"dns":0,"tcp":0,"ttfb":557,"pathname":"https://weibo.com/ajax/statuses/buildComments","speed":0}'
    s = json.loads(s)
    s['name'] = get_content_1_url
    s = json.dumps(s)
    data = f'------WebKitFormBoundaryNs1Toe4Mbr8n1qXm\r\nContent-Disposition: form-data; name="entry"\r\n\r\n{s}\r\n------WebKitFormBoundaryNs1Toe4Mbr8n1qXm\r\nContent-Disposition: form-data; name="request_id"\r\n\r\n\r\n------WebKitFormBoundaryNs1Toe4Mbr8n1qXm--\r\n'
    response = requests.post('https://weibo.com/ajax/log/rum', cookies=cookies, headers=headers, data=data)
    return response.text


def get_once_data(uid, mid, the_first=True, max_id=None):
    respones_1 = get_content_1(uid, mid, the_first, max_id)
    url = respones_1.url
    response_2 = get_content_2(url)
    df = pd.DataFrame(respones_1.json()['data'])
    max_id = respones_1.json()['max_id']
    return max_id, df


if __name__ == '__main__':
    # 先在上面设置cookies
    # 设置好了再进行操作

    # 自定义
    name = '#邹振东诚邀张雪峰来厦门请你吃沙茶面#'
    uid = '2610806555'
    mid = '4914095331742409'
    page = 100

    # 初始化
    df_list = []
    max_id = ''

    for i in range(page):
        if i == 0:
            max_id, df = get_once_data(uid=uid, mid=mid)
        else:
            max_id, df = get_once_data(uid=uid, mid=mid, the_first=False, max_id=max_id)
        if df.shape[0] == 0 or max_id == 0:
            break
        else:
            df_list.append(df)
            print(f'第{i}页解析完毕！max_id:{max_id}')

    df = pd.concat(df_list).astype(str).drop_duplicates()
    df.to_csv(f'{name}.csv', index=False)