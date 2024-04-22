import sys
from mycsv.csv import *

import requests
from bs4 import BeautifulSoup
import re
from spider.GetDataFromTieba import *
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QAction
from PyQt5.uic import loadUi

from ui.MyWindows import *

proxies = { "http": None, "https": None}
# 系统代理端口设置为None，避免Clash对Request造成影响
class Spider(MyWindow):
    def __init__(self):
        super().__init__()
        loadUi('./ui/spider.ui', self)  # 加载UI文件
        self.setStyleSheet("background-color: white;")
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        # 将 spider_tieba 函数与 tieba_button 的 clicked 信号绑定
        self.tieba_button.clicked.connect(self.spider_tieba)

    def spider_tieba(self):
        try:
            url = self.url_lineEdit.text()
            filepath,filename = GetTiebaData(url)
            texts, IPs = read_columns_from_csv(filepath, 'Text', 'IP Address')
            for text,ip in zip(texts,IPs):
                print(text+ip)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == '__main__':
    # 打开爬虫分析界面
    app = QApplication(sys.argv)
    window = Spider()
    window.show()
    sys.exit(app.exec_())