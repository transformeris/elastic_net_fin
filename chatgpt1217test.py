import sys
from PyQt5.QtWidgets import QApplication,QLineEdit, QWidget, QPushButton, QStackedWidget, QVBoxLayout,QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout1 = QVBoxLayout()
        layout2=QGridLayout()
        # 创建两个小部件
        self.widget1 = QWidget()
        self.widget2 = QWidget()
        textbox = QLineEdit()
        self.widget1.setLayout(layout1)
        # 将文本框添加到小部件1中
        self.widget1.layout().addWidget(textbox)

        # 创建按钮
        self.button1 = QPushButton("跳转到小部件1")
        self.button2 = QPushButton("跳转到小部件2")
        self.button3 = QPushButton("跳转到小部件5")

        self.widget1.layout().addWidget(self.button1)
        self.widget2.setLayout(layout2)
        self.widget2.layout().addWidget(self.button3)
        self.widget2.layout().addWidget(self.button2)
        # 创建QStackedWidget容器
        self.stack = QStackedWidget()
        self.stack.addWidget(self.widget1)
        self.stack.addWidget(self.widget2)

        # 将按钮与小部件关联
        self.button1.clicked.connect(lambda: self.stack.setCurrentWidget(self.widget1))
        self.button2.clicked.connect(lambda: self.stack.setCurrentWidget(self.widget2))
        # button2.keyPressEvent()
        # 创建布局并添加按钮和容器
        layout = QGridLayout()
        # layout.addWidget(self.button1)
        # layout.addWidget(self.button2)
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.selected_button_idx = 0

        self.update_button_highlight()
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Return:
            if self.selected_button_idx == 0:
                self.stack.setCurrentWidget(self.widget1)
        elif key == Qt.Key_W:
            if self.selected_button_idx==1:
                self.selected_button_idx = self.selected_button_idx-1
                print('dangqian:',self.selected_button_idx )
        elif key == Qt.Key_S:
            if self.selected_button_idx==0:
                self.selected_button_idx =self.selected_button_idx+ 1
        else:
            super().keyPressEvent(event)
        self.update_button_highlight()

    def update_button_highlight(self):
        if self.selected_button_idx==0:
            self.button1.setStyleSheet("""
                                       QPushButton {
                                           background-color: transparent;  /* 设置背景颜色为透明 */
                                           border: none;                   /* 移除边框 */
                                           color: black;                   /* 设置文字颜色 */
                                       }
                                       QPushButton:hover {
                                           color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
                                       }
                                       QPushButton:pressed {
                                           color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
                                       }
                                   """)
            self.button2.setStyleSheet("background-color: lightblue")

        elif self.selected_button_idx==1:
            self.button2.setStyleSheet("""
                                       QPushButton {
                                           background-color: transparent;  /* 设置背景颜色为透明 */
                                           border: none;                   /* 移除边框 */
                                           color: black;                   /* 设置文字颜色 */
                                       }
                                       QPushButton:hover {
                                           color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
                                       }
                                       QPushButton:pressed {
                                           color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
                                       }
                                   """)
            self.button1.setStyleSheet("background-color: lightblue")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
