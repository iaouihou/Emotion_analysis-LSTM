from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMenu, \
    QDesktopWidget
import pandas as pd


class LoadCsvWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSV Viewer')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.setFixedSize(800, 600)  # 设置窗口大小
        self.center()  # 调用居中方法

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # 添加右键菜单
        self.table_widget.setContextMenuPolicy(3)  # 3 表示右键菜单策略
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

        # 设置常量csv_path
        self.csv_path = './results/results.csv'

        self.load_csv()  # 加载 CSV 文件

    def center(self):
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口的尺寸
        window_size = self.geometry()
        # 计算居中的位置
        x = int((screen.width() - window_size.width()) / 2)
        y = int((screen.height() - window_size.height()) / 2)
        # 设置窗口的位置
        self.move(x, y)

    def load_csv(self):
        try:
            # 读取 CSV 文件
            self.df = pd.read_csv(self.csv_path, encoding='gbk')

            # 设置表格的行数和列数
            self.table_widget.setRowCount(self.df.shape[0])
            self.table_widget.setColumnCount(self.df.shape[1])

            # 设置表头
            column_names = ['时间', '文本', '识别结果', '消极概率', '积极概率']
            self.table_widget.setHorizontalHeaderLabels(column_names)

            # 填充表格内容
            for i, row in self.df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(i, j, item)

            # 调整表格大小
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
        except Exception as e:
            print("An error occurred while loading CSV file:", e)

    def show_context_menu(self, pos):
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.table_widget.viewport().mapToGlobal(pos))
        if action == delete_action:
            selected_row = self.table_widget.currentRow()
            self.delete_row(selected_row)

    def delete_row(self, row_index):
        try:
            if row_index >= 0 and row_index < self.df.shape[0]:
                self.df = self.df.drop(self.df.index[row_index])
                self.df.to_csv(self.csv_path, index=False, encoding='gbk')
                self.table_widget.removeRow(row_index)
        except Exception as e:
            print("An error occurred while deleting row:", e)


if __name__ == "__main__":
    app = QApplication([])
    window = LoadCsvWindow()
    window.show()
    app.exec_()
