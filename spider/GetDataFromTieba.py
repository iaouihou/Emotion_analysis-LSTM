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
    try:
        response = requests.get(url,proxies=proxies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # 获取页面标题
            title = soup.title.string.strip()
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
    userid = post.user.user_id
    user_name = post.user.user_name
    nick_name_new = post.user.nick_name_new
    ip_address = post.user.ip
    return text_content, userid, user_name, nick_name_new,ip_address



async def write_posts_to_csv(posts, filepath):
    # 检查文件是否存在，如果不存在则创建文件夹和文件
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode='w', encoding='utf-8-sig', newline='') as file:
            # 写入 CSV 文件的代码
            writer = csv.writer(file)
            writer.writerow(['Text', 'User ID', 'User Name', 'Nick Name New', 'IP Address'])
    # 在追加模式下打开文件
    with open(filepath, mode='a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        for post in posts:
            text, user_id, user_name, nick_name_new, ip_address = await extract_post_info(post)
            if text:  # 检查text内容是否为空
                writer.writerow([text, user_id, user_name, nick_name_new, ip_address])

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
async def main(url):
    title, page_number = get_page_title_and_page_number(url)
    await get_data(url,title,page_number)

def GetTiebaData(url):
    print(url)
    tid = extract_id_from_url(url)
    title, page_number = get_page_title_and_page_number(url)
    filename = f'{title}_{tid}.csv'  # 使用 tid 变量命名文件
    filepath = f'./TieBaData/{filename}'
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(url))
    return filepath,title
if __name__ == "__main__":
    url = input("请输入要分析的贴吧网址")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(url))
