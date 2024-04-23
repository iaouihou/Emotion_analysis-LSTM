import sys
from spider.GetDataFromTieba import *
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QAction, QFileDialog, QMessageBox
from PyQt5.uic import loadUi

from ui.MyWindows import *
from Analysis import *
import os

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
        self.select_file_button.clicked.connect(self.select_file)

    def select_file(self):
        import os
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取当前脚本的目录，然后计算相对路径
        base_dir = os.path.dirname(__file__)  # 获取当前文件的目录
        initial_dir = os.path.join(base_dir, 'TiebaAnalysis')  # 假设有一个名为 'data' 的文件夹与脚本在同一目录
        file_filter = "PDF Files (*.csv)"  # 仅允许选择 PDF 文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", initial_dir,
                                                   file_filter, options=options)
        if file_path:
            # 设置表头
            column_names = ['时间', '文本', '识别结果', '消极概率', '积极概率','IP属地']
            self.csv_window = LoadCsvWindow(file_path)  # 创建第二个窗口实例
            self.csv_window.load_csv(column_names)
            self.csv_window.show()  # 显示第二个窗口

    def spider_tieba(self):
        try:
            url = self.url_lineEdit.text()
            # 从输入框获取url链接
            filepath, filename = GetTiebaData(url)
            column1_name = "Text"
            column2_name = "IP Address"
            print("开始分析")
            newfilepath = Analysis_tieba(filepath, filename, column1_name, column2_name)
            print(newfilepath)

            # 分析完成后显示消息框
            QMessageBox.information(self, f" {filename} 爬取分析已完成.")

        except Exception as e:
            print("An error occurred:", e)
            QMessageBox.critical(self, 'Error', 'An error occurred during the analysis.')

if __name__ == '__main__':
    # 打开爬虫分析界面
    app = QApplication(sys.argv)
    window = Spider()
    window.show()
    sys.exit(app.exec_())