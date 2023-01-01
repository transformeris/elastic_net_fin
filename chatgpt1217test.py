import sys
from PyQt5.QtWidgets import QApplication,QLineEdit, QWidget, QPushButton, QStackedWidget, QVBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout1 = QVBoxLayout()
        # 创建两个小部件
        widget1 = QWidget()
        widget2 = QWidget()
        textbox = QLineEdit()
        widget1.setLayout(layout1)
        # 将文本框添加到小部件1中
        widget1.layout().addWidget(textbox)
        # 创建按钮
        button1 = QPushButton("跳转到小部件1")
        button2 = QPushButton("跳转到小部件2")

        # 创建QStackedWidget容器
        stack = QStackedWidget()
        stack.addWidget(widget1)
        stack.addWidget(widget2)

        # 将按钮与小部件关联
        button1.clicked.connect(lambda: stack.setCurrentWidget(widget1))
        button2.clicked.connect(lambda: stack.setCurrentWidget(widget2))

        # 创建布局并添加按钮和容器
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(stack)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
