import sys
from PyQt5 import QtWidgets, QtGui


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt Stacked Widget Example')

        # 创建一个垂直布局
        layout = QtWidgets.QVBoxLayout()

        # 创建一个按钮，用于在多重界面之间切换
        self.switch_button = QtWidgets.QPushButton('Switch')

        # 将按钮添加到布局中
        layout.addWidget(self.switch_button)

        # 创建一个多重界面
        self.stack = QtWidgets.QStackedWidget()

        # 创建两个普通界面
        self.page1 = QtWidgets.QWidget()
        self.page2 = QtWidgets.QWidget()

        # 在每个界面中添加一个标签
        label1 = QtWidgets.QLabel('This is page 1')
        label2 = QtWidgets.QLabel('This is page 2')
        self.page1.setLayout(QtWidgets.QVBoxLayout())
        self.page1.layout().addWidget(label1)
        self.page2.setLayout(QtWidgets.QVBoxLayout())
        self.page2.layout().addWidget(label2)

        # 将两个界面添加到多重界面中
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        # 将多重界面添加到布局中
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # 将切换按钮的点击信号与槽函数 switch_page() 绑定
        self.switch_button.clicked.connect(self.switch_page)

    def switch_page(self):
        # 获取当前界面的索引
        current_index = self.stack.currentIndex()
        # 如果当前是第一个界面，则切换到第二个界面
        # 否则，切换到第一个界面
        if current_index == 0:
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())