import csv
import asyncio
import os
import re

import aiotieba
from bs4 import BeautifulSoup
import requests

proxies = { "http": None, "https": None}
# 系统代理端口设置为None，避免Clash对Request造成影响
def remove_brackets_and_text(text):
    # 定义匹配【】及其中包含的文字的正则表达式
    pattern = r'\【[^\】]*\】'
    # 使用 sub 方法替换匹配的部分为空字符串
    result = re.sub(pattern, '', text)
    # 去除"_百度贴吧"
    result = result.replace("_百度贴吧", "")
    return result
def extract_id_from_url(url):
    # 定义匹配数字的正则表达式
    pattern = r'\d+'
    # 使用 findall 方法找到所有匹配的数字
    ids = re.findall(pattern, url)
    # 返回第一个匹配到的数字（即 ID）
    if ids:
        return ids[0]
    else:
        return None
def get_page_title_and_page_number(url):
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Referer': 'https://www.baidu.com/',  # 设置Referer，模拟从百度首页跳转过来
        'Accept-Language': 'en-US,en;q=0.9',  # 设置接受语言
    }

    # 设置Cookies，将键值对以字典形式传入
    cookies = {
        'BAIDUID': 'your_baiduid_cookie_value',
        'BDUSS': 'your_bduss_cookie_value',
        # 其他百度贴吧需要的Cookies
    }

    try:
        response = requests.get(url,headers=headers,cookies=cookies,proxies=proxies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # 获取页面标题
            title = soup.title.string.strip()
            print(title)
            # 获取尾页链接
            last_page_link = soup.find('a', string='尾页', href=re.compile(r'pn=(\d+)'))
            if last_page_link:
                match = re.search(r'pn=(\d+)', last_page_link['href'])
                if match:
                    page_number = int((int(match.group(1))+1)/2)
                    return title, page_number
                else:
                    print("Failed to extract page number from link.")
            else:
                print("Last page link not found.")
        else:
            print("Failed to fetch page:", response.status_code)
    except Exception as e:
        print("Error:", e)
async def extract_post_info(post):
    text_content = post.text
    user_name = post.user.user_name
    gender = post.user.gender
    agree = post.agree
    disagree = post.disagree
    ip_address = post.user.ip
    return text_content,user_name,gender,agree,disagree,ip_address
def extract_comments_info(comments):
    extracted_info = []
    for comment in comments:
        text_content = comment.text
        user_name = comment.user.user_name
        gender = comment.user.gender
        agree = comment.agree
        disagree = comment.disagree
        ip_address = comment.user.ip
        extracted_info.append((text_content, user_name, gender, agree, disagree, ip_address))
    return extracted_info


async def write_posts_to_csv(posts, filepath):
    # 检查文件是否存在，如果不存在则创建文件夹和文件
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode='w', encoding='utf-8-sig', newline='') as file:
            # 写入 CSV 文件的代码
            writer = csv.writer(file)
            writer.writerow(['Text','User Name','Gender', 'Agree','Disagree' ,'IP Address'])
    # 在追加模式下打开文件
    with open(filepath, mode='a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        for post in posts:
            text_post, user_name_post, gender_post, agree_post, disagree_post, ip_address_post = await extract_post_info(
                post)
            if text_post:  # 检查text内容是否为空
                writer.writerow([text_post, user_name_post, gender_post, agree_post, disagree_post, ip_address_post])

            # 处理post的comments
            comments_info = extract_comments_info(post.comments)
            for comment_info in comments_info:
                text_comment, user_name_comment, gender_comment, agree_comment, disagree_comment, ip_address_comment = comment_info
                if text_comment:  # 检查text内容是否为空
                    writer.writerow([text_comment, user_name_comment, gender_comment, agree_comment, disagree_comment,
                                     ip_address_comment])

async def get_data(url,title,page_number):
    tid = extract_id_from_url(url)
    print("正在爬取标题为"+title+"的帖子数据,一共有"+str(page_number)+"页")
    filename = f'{title}_{tid}.csv'  # 使用 tid 变量命名文件
    filepath = f'./TieBaData/{filename}'
    async with aiotieba.Client() as client:
        for page in range(1, page_number+1):
            posts = await client.get_posts(int(tid), rn=60, pn=page, with_comments=True)
            # print("已经获取第" + str(page) + "页")
            await write_posts_to_csv(posts, filepath)
    print("已经获取该帖子共" + str(page_number) + "页的数据")
async def main(url,title,page_number):
    await get_data(url,title,page_number)

def GetTiebaData(url):
    print(url)
    tid = extract_id_from_url(url)
    title, page_number = get_page_title_and_page_number(url)
    # title, page_number = "test",10
    filename = f'{title}_{tid}.csv'  # 使用 tid 变量命名文件
    filepath = f'./TieBaData/{filename}'
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(url,title,page_number))
    return filepath,title
if __name__ == "__main__":
    url = input("请输入要分析的贴吧网址")
    GetTiebaData(url)