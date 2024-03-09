import requests
from bs4 import BeautifulSoup

def crawl_post(url):
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        layers = soup.find_all('cc')
        if layers:
            with open('post_content.txt', 'w', encoding='utf-8') as f:
                for layer in layers:
                    content = layer.get_text(strip=True)
                    f.write(content + '\n')
                    f.write('####\n')
            print("内容已保存至 post_content.txt")
        else:
            print("未找到帖子内容")
    else:
        print("无法访问该网址")

if __name__ == "__main__":
    url = input("请输入要爬取的百度贴吧帖子链接: ")
    crawl_post(url)
