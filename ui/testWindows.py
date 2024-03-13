from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsBlurEffect, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blur Effect Example')

        # 创建一个布局并设置为窗口部件的主布局
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # 创建一个标签部件并添加到布局中
        self.label = QLabel('This is a blurred label')
        layout.addWidget(self.label)

        # 创建一个QGraphicsBlurEffect对象并设置模糊半径
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)  # 设置模糊半径为5

        # 将QGraphicsBlurEffect应用于标签部件
        self.label.setGraphicsEffect(blur_effect)
        self.setGraphicsEffect(blur_effect)
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
