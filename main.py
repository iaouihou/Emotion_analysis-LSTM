import csv
import os
import sys
import time

from predict import predict_sentiment
from predict import get_sentiment_label
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QAction
from PyQt5.uic import loadUi
from LoadCsv import LoadCsvWindow
from ui.MyWindows import *

csv_path = './results/results.csv'


# 将读取的数据写入csv中保存
def write_to_csv(csv_path, current_time, input_text, negative, positive):
    # 获取识别结果
    sentiment_label = get_sentiment_label(negative, positive)
    # 检查CSV文件是否存在，如果不存在，则创建一个新文件并写入表头
    is_new_file = False
    if not os.path.exists(csv_path):
        is_new_file = True

    # 将数据写入CSV文件
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as csvfile:  # 注意这里使用了 utf-8-sig
        fieldnames = ['时间', '文本', '识别结果', '消极概率', '积极概率']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，需要重新写入表头
        if is_new_file:
            writer.writeheader()

        # 写入数据行
        writer.writerow({'时间': current_time, '文本': input_text, '识别结果': sentiment_label,'消极概率': negative,
                         '积极概率': positive})

class MainWindow(MyWindow):
    def __init__(self):
        super().__init__()
        loadUi('./ui/mainwindow.ui', self)  # 加载UI文件
        self.setWindowTitle('情感分析系统')
        self.setFixedSize(450, 750)  # 设置窗口大小
        self.center()  # 调用居中方法
        # 设置背景颜色为白色
        # self.setStyleSheet("background-color: white;")
        self.create_menu_bar()
        self.start_button.clicked.connect(self.analyze_sentiment)
        self.clear_button.clicked.connect(self.clear_input)
        self.load_button.clicked.connect(self.open_LoadCsv_window)
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        # 隐藏标题栏
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def create_menu_bar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('Help')
        about_action = QAction('查看帮助', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def open_LoadCsv_window(self):
        self.csv_window = LoadCsvWindow()  # 创建第二个窗口实例
        self.csv_window.show()  # 显示第二个窗口

    def show_about_dialog(self):
        about_dialog = QDialog()
        about_dialog.setWindowTitle('About')
        about_layout = QVBoxLayout()
        about_label = QLabel('在输入框中输入文字,按下开始即可分析情感倾向')
        about_layout.addWidget(about_label)
        about_dialog.setLayout(about_layout)
        about_dialog.exec()

    def analyze_sentiment(self):
        input_text = self.input_text_edit.toPlainText()
        negative, positive = predict_sentiment(input_text, pad_size=50)
        sentiment_label = get_sentiment_label(negative, positive)
        output_text = "应该为"+sentiment_label+"\n消极的概率:"+str(negative)+"\n积极的概率:"+str(positive)
        # 这里需要调用情感分析函数，并将结果更新到输出标签中
        # 现在仅将输入文本设置为输出结果
        self.output_news_label.setText(output_text)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        write_to_csv(csv_path, current_time, input_text, negative, positive)

    def clear_input(self):
        self.input_text_edit.clear()
        self.output_news_label.clear()


if __name__ == '__main__':
    # 进行情感预测
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
