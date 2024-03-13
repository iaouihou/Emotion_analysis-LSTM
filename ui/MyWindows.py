from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化窗口拖动相关变量
        self.m_flag = False
        self.m_Position = None
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def center(self):
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口的尺寸
        window_size = self.geometry()
        # 计算居中的位置
        x = (screen.width() - window_size.width()) / 2
        y = (screen.height() - window_size.height()) / 2
        # 设置窗口的位置
        self.move(x, y)
