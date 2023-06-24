import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout,QLabel,QSizePolicy, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

QWidget.QShortcut = QShortcut
class Widget1(QWidget):
    def __init__(self):
        super().__init__()

        # 在 QWidget 中添加按钮和标签
        self.button1 = QPushButton('Go to 零序保护定值', self)
        self.button2 = QPushButton('Go to 距离保护定值', self)
        self.label = QLabel('差动保护定值', self)

        # 设置标签的对齐方式为居中
        self.label.setAlignment(Qt.AlignCenter)

        # 设置按钮的大小策略为 QSizePolicy.Expanding
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 为每个按钮添加点击事件
        self.button1.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(1))
        self.button2.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(2))

        # 创建一个 QVBoxLayout，并将标签和按钮添加到其中
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        self.setLayout(vbox)

        # 创建 QShortcut 对象，将上下箭头键绑定到按钮上
        shortcut_up = QShortcut(QKeySequence(Qt.Key_Up), self)
        shortcut_down = QShortcut(QKeySequence(Qt.Key_Down), self)
        shortcut_up.activated.connect(self.button1.click)
        shortcut_down.activated.connect(self.button2.click)

    def resizeEvent(self, event):
        # 在窗口大小改变时重新计算按钮字体的大小
        font_size = self.button1.width() // 10
        self.button1.setStyleSheet(f'font-size: {font_size}px;')
        font_size = self.button2.width() // 10
        self.button2.setStyleSheet(f'font-size: {font_size}px;')

        # 在窗口大小改变时重新计算标签字体的大小
        font_size = self.label.width() // 10
        self.label.setStyleSheet(f'font-size: {font_size}px; text-align: center;')

class Widget2(QWidget):
    def __init__(self):
        super().__init__()

        # 在 QWidget 中添加按钮和标签
        self.button1 = QPushButton('Go to 差动保护定值', self)
        self.button2 = QPushButton('Go to 距离保护定值', self)
        self.label = QLabel('零序保护定值', self)

        # 设置标签的对齐方式为居中
        self.label.setAlignment(Qt.AlignCenter)

        # 为每个按钮添加点击事件
        self.button1.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(0))
        self.button2.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(2))

        # 创建一个 QVBoxLayout，并将标签和按钮添加到其中
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        self.setLayout(vbox)

        # 创建 QShortcut 对象，将上下箭头键绑定到按钮上
        shortcut_up = QShortcut(QKeySequence(Qt.Key_Up), self)
        shortcut_down = QShortcut(QKeySequence(Qt.Key_Down), self)
        shortcut_up.activated.connect(self.button1.click)
        shortcut_down.activated.connect(self.button2.click)

    def resizeEvent(self, event):
        # 在窗口大小改变时重新计算按钮字体的大小
        font_size = self.button1.width() // 10
        self.button1.setStyleSheet(f'font-size: {font_size}px;')
        font_size = self.button2.width() // 10
        self.button2.setStyleSheet(f'font-size: {font_size}px;')

        # 在窗口大小改变时重新计算标签字体的大小
        font_size = self.label.width() // 10
        self.label.setStyleSheet(f'font-size: {font_size}px; text-align: center;')

class Widget3(QWidget):
    def __init__(self):
        super().__init__()

        # 在 QWidget 中添加按钮和标签
        self.button1 = QPushButton('Go to 差动保护定值', self)
        self.button2 = QPushButton('Go to 零序保护定值', self)
        self.label = QLabel('距离保护定值', self)

        # 设置标签的对齐方式为居中
        self.label.setAlignment(Qt.AlignCenter)

        # 为每个按钮添加点击事件
        self.button1.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(0))
        self.button2.clicked.connect(lambda: self.parent().stacked_layout.setCurrentIndex(1))

        # 创建一个 QVBoxLayout，并将标签和按钮添加到其中
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        self.setLayout(vbox)

        # 创建 QShortcut 对象，将上下箭头键绑定到按钮上
        shortcut_up = QShortcut(QKeySequence(Qt.Key_Up), self)
        shortcut_down = QShortcut(QKeySequence(Qt.Key_Down), self)
        shortcut_up.activated.connect(self.button1.click)
        shortcut_down.activated.connect(self.button2.click)

    def resizeEvent(self, event):
        # 在窗口大小改变时重新计算按钮字体的大小
        font_size = self.button1.width() // 10
        self.button1.setStyleSheet(f'font-size: {font_size}px;')
        font_size = self.button2.width() // 10
        self.button2.setStyleSheet(f'font-size: {font_size}px;')

        # 在窗口大小改变时重新计算标签字体的大小
        font_size = self.label.width() // 10
        self.label.setStyleSheet(f'font-size: {font_size}px; text-align: center;')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建多个 QWidget
        self.widget1 = Widget1()
        self.widget2 = Widget2()
        self.widget3 = Widget3()

        # 创建一个 QStackedLayout，并将 QWidget 添加到其中
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.widget1)
        self.stacked_layout.addWidget(self.widget2)
        self.stacked_layout.addWidget(self.widget3)

        # 创建一个 QHBoxLayout，并将 QStackedLayout 添加到其中
        hbox = QHBoxLayout()
        hbox.addLayout(self.stacked_layout)

        # 设置主窗口的布局
        self.setLayout(hbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())