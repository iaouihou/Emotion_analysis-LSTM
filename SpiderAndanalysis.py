import requests
from bs4 import BeautifulSoup
import re

proxies = { "http": None, "https": None}
# 系统代理端口设置为None，避免Clash对Request造成影响
def get_page_number(url):
    try:
        response = requests.get(url,proxies=proxies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            last_page_link = soup.find('a', string='尾页', href=re.compile(r'pn=(\d+)'))
            if last_page_link:
                match = re.search(r'pn=(\d+)', last_page_link['href'])
                if match:
                    return int(int(match.group(1))/2)
                else:
                    print("Failed to extract page number from link.")
            else:
                print("Last page link not found.")
        else:
            print("Failed to fetch page:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

# 示例使用：
url = "https://tieba.baidu.com/p/8929280685"  # 你的贴吧主题帖链接
page_number = get_page_number(url)
if page_number is not None:
    print("Page number:", page_number)
else:
    print("Failed to fetch page number.")
