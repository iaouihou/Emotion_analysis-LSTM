import sys
import time

from predict import predict_sentiment
from predict import get_sentiment_label
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QTextEdit, QPushButton, QVBoxLayout, QWidget, \
    QLabel, QDialog,QDesktopWidget
import csv
import os

csv_path = './results/results.csv'
# 将读取的数据写入csv中保存
def write_to_csv(csv_path, current_time, input_text, negative, positive):
    # 获取识别结果
    sentiment_label = get_sentiment_label(negative, positive)

    # 检查CSV文件是否存在，如果不存在，则创建一个新文件并写入表头
    is_new_file = False
    if not os.path.exists(csv_path):
        is_new_file = True
        # with open(csv_path, 'w', newline='') as csvfile:
        #     fieldnames = ['时间', '文本', '消极概率', '积极概率', '识别结果']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()

    # 将数据写入CSV文件
    with open(csv_path, 'a', newline='') as csvfile:
        fieldnames = ['时间', '文本', '识别结果','消极概率', '积极概率']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，需要重新写入表头
        if is_new_file:
            writer.writeheader()

        # 写入数据行
        writer.writerow({'时间': current_time, '文本': input_text, '识别结果': sentiment_label,'消极概率': negative,
                         '积极概率': positive,})


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output_news_label = None
        self.analysis_result_label = None
        self.input_text_edit = None
        self.start_button = None
        self.clear_button = None
        self.setWindowTitle('情感分析系统')
        self.setFixedSize(400, 600)  # 设置窗口大小
        self.center()  # 调用居中方法
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.create_menu_bar()
        self.create_widgets()

    def center(self):
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口的尺寸
        window_size = self.geometry()
        # 计算居中的位置
        x =int( (screen.width() - window_size.width()) / 2)
        y = int((screen.height() - window_size.height()) / 2)
        # 设置窗口的位置
        self.move(x, y)

    def create_menu_bar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About...', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_widgets(self):
        self.input_text_edit = QTextEdit()
        self.input_text_edit.setStyleSheet("font-size: 20px;")  # 设置字体大小为20像素
        self.layout.addWidget(self.input_text_edit)

        self.analysis_result_label = QLabel('分析结果：')
        self.analysis_result_label.setStyleSheet("font: 15pt Helvetica;")
        self.layout.addWidget(self.analysis_result_label)

        self.output_news_label = QLabel()
        self.output_news_label.setStyleSheet("font: 15pt Helvetica;")
        self.layout.addWidget(self.output_news_label)

        self.start_button = QPushButton('开始')
        self.start_button.setStyleSheet("font: 15pt Helvetica;")
        self.start_button.clicked.connect(self.analyze_sentiment)
        self.layout.addWidget(self.start_button)

        self.clear_button = QPushButton('清空')
        self.clear_button.setStyleSheet("font: 15pt Helvetica;")
        self.clear_button.clicked.connect(self.clear_input)
        self.layout.addWidget(self.clear_button)

    def show_about_dialog(self):
        about_dialog = QDialog()
        about_dialog.setWindowTitle('About')
        about_layout = QVBoxLayout()
        about_label = QLabel('你好')
        about_layout.addWidget(about_label)
        about_dialog.setLayout(about_layout)
        about_dialog.exec()

    def analyze_sentiment(self):
        input_text = self.input_text_edit.toPlainText()
        negative,positive = predict_sentiment(input_text, pad_size=50)
        output_text = "消极的概率:"+str(negative)+"\n积极的概率:"+str(positive)
        # 这里需要调用情感分析函数，并将结果更新到输出标签中
        # 现在仅将输入文本设置为输出结果
        self.output_news_label.setText(output_text)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        write_to_csv(csv_path,current_time,input_text,negative,positive)

    def clear_input(self):
        self.input_text_edit.clear()
        self.output_news_label.clear()

if __name__ == '__main__':
    # 进行情感预测
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())