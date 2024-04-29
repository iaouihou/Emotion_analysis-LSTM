import sys

from PyQt5.QtCore import QTimer

from LoadCsv import LoadCsvWindow
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
        self.setFixedSize(450, 750)
        # self.setStyleSheet("background-color: white;")
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        self.create_menu_bar()
        # 将 spider_tieba 函数与 tieba_button 的 clicked 信号绑定
        self.tieba_button.clicked.connect(self.spider_tieba)
        self.select_file_button.clicked.connect(self.results)
        self.visualize_button.clicked.connect(self.visualize)

    def select_file(self):
        import os
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取当前脚本的目录，然后计算相对路径
        base_dir = os.path.dirname(__file__)  # 获取当前文件的目录
        initial_dir = os.path.join(base_dir, 'TiebaAnalysis')  # 假设有一个名为 'data' 的文件夹与脚本在同一目录
        file_filter = "PDF Files (*.csv)"  # 仅允许选择 csv 文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", initial_dir,
                                                   file_filter, options=options)
        return file_path
    def results(self):
        file_path = self.select_file()
        if file_path:
            # 设置表头
            column_names = ['文本', '识别结果', '消极概率', '积极概率','支持','反对','ip属地','性别']
            self.csv_window = LoadCsvWindow(file_path)  # 创建第二个窗口实例
            self.csv_window.load_csv(column_names)
            self.csv_window.show()  # 显示第二个窗口
    def visualize(self):
     file_path = self.select_file()
     if file_path:
         visualize_sentiments(file_path)

    from PyQt5.QtWidgets import QMessageBox

    def spider_tieba(self):
        try:
            url = self.url_lineEdit.text()
            # 从输入框获取url链接
            filepath, filename = GetTiebaData(url)
            column1_name = "Text"
            column2_name = "IP Address"
            column3_name = "Agree"
            column4_name = "Disagree"
            column5_name = "Gender"
            print("开始分析")
            newfilepath = Analysis_tieba(filepath, filename, column1_name, column2_name, column3_name, column4_name,
                                         column5_name)
            # 分析完成后显示消息框
            QMessageBox.information(self, "成功", f"成功爬取 {filename}")
            print(newfilepath)
        except Exception as e:
            print("An error occurred:", e)
            QMessageBox.information(self, "错误", "发生错误，请检查URL和网络连接")

    def create_menu_bar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('Help')
        about_action = QAction('查看帮助', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        about_dialog = QDialog()
        about_dialog.setWindowTitle('About')
        about_layout = QVBoxLayout()
        about_label = QLabel('在输入框中输入文字,按下开始即可分析情感倾向')
        about_layout.addWidget(about_label)
        about_dialog.setLayout(about_layout)
        about_dialog.exec()


if __name__ == '__main__':
    # 打开爬虫分析界面
    app = QApplication(sys.argv)
    window = Spider()
    window.show()
    sys.exit(app.exec_())