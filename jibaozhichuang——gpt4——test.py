# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
# from PyQt5.QtCore import Qt
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('PyQt Key Navigation Example')
#
#         grid = QGridLayout()
#
#         self.buttons = [
#             QPushButton('Button 1'),
#             QPushButton('Button 2'),
#             QPushButton('Button 3'),
#             QPushButton('Button 4')
#         ]
#
#         positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
#
#         for button, pos in zip(self.buttons, positions):
#             grid.addWidget(button, *pos)
#
#         self.setLayout(grid)
#
#         # Initialize the selected button index
#         self.selected_button_idx = 0
#         self.update_button_focus()
#
#     def keyPressEvent(self, event):
#         key = event.key()
#
#         if key == Qt.Key_Up:
#             if self.selected_button_idx in [2, 3]:
#                 self.selected_button_idx -= 2
#         elif key == Qt.Key_Down:
#             if self.selected_button_idx in [0, 1]:
#                 self.selected_button_idx += 2
#         elif key == Qt.Key_Left:
#             if self.selected_button_idx in [1, 3]:
#                 self.selected_button_idx -= 1
#         elif key == Qt.Key_Right:
#             if self.selected_button_idx in [0, 2]:
#                 self.selected_button_idx += 1
#         else:
#             super().keyPressEvent(event)
#
#         self.update_button_focus()
#
#     def update_button_focus(self):
#         for idx, button in enumerate(self.buttons):
#             button.setFocus() if idx == self.selected_button_idx else button.clearFocus()
#
# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     main()

# button.setStyleSheet("""
#     QPushButton {
#         background-color: rgb(240, 240, 240);     /* 设置背景颜色 */
#         border: 1px solid rgb(150, 150, 150);    /* 设置边框 */
#         border-radius: 4px;                      /* 设置边框圆角 */
#         padding: 5px;                            /* 设置内边距 */
#         color: rgb(0, 0, 0);                     /* 设置文字颜色 */
#         font: bold 12px;                         /* 设置字体样式 */
#         text-align: center;                      /* 设置文字对齐方式 */
#     }
#     QPushButton:hover {
#         background-color: rgb(200, 200, 200);     /* 鼠标悬停时，设置背景颜色 */
#         border: 1px solid rgb(120, 120, 120);    /* 鼠标悬停时，设置边框 */
#         color: rgb(0, 0, 255);                   /* 鼠标悬停时，设置文字颜色 */
#     }
#     QPushButton:pressed {
#         background-color: rgb(180, 180, 180);     /* 鼠标按下时，设置背景颜色 */
#         border: 1px solid rgb(100, 100, 100);    /* 鼠标按下时，设置边框 */
#         color: rgb(255, 0, 0);                   /* 鼠标按下时，设置文字颜色 */
#     }
#     QPushButton:disabled {
#         background-color: rgb(220, 220, 220);     /* 禁用时，设置背景颜色 */
#         border: 1px solid rgb(150, 150, 150);    /* 禁用时，设置边框 */
#         color: rgb(150, 150, 150);               /* 禁用时，设置文字颜色 */
#     }
# """)
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout,QStackedWidget,QSizePolicy
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt Key Navigation Example with Button Highlight')




        grid = QGridLayout()
        grid.setHorizontalSpacing(0)  # 设置水平间距为 10 像素
        grid.setVerticalSpacing(0)  # 设置垂直间距为 20 像素
        self.buttons = [
            QPushButton('Button 1'),
            QPushButton('Button 2'),
            QPushButton('Button 3'),
            QPushButton('Button 4'),
            QPushButton('Button 5')
        ]
        for button in self.buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.buttons[0].setStyleSheet("""
                                        QPushButton {
                                            margin: 0px;          /* 设置外边距为 0 */
                                            padding: 0px;         /* 设置内边距为 0 */
                                            background-color: transparent;  /* 设置背景颜色为透明 */
                                            border: 1px solid rgb(150, 150, 150);                   /* 移除边框 */
                                            color: black;                   /* 设置文字颜色 */
                                        }
                                        QPushButton:hover {
                                            color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
                                        }
                                        QPushButton:pressed {
                                            color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
                                        }
                                    """)
        positions = [(0, 0), (0, 1), (1, 0), (1, 1),(2,0)]

        for button, pos in zip(self.buttons, positions):
            grid.addWidget(button, *pos)

        self.setLayout(grid)

        # Initialize the selected button index
        self.selected_button_idx = 0

        self.update_button_highlight()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_W:
            if self.selected_button_idx in [2, 3]:
                self.selected_button_idx -= 2
        elif key == Qt.Key_S:
            if self.selected_button_idx in [0, 1]:
                self.selected_button_idx += 2
        elif key == Qt.Key_A:
            if self.selected_button_idx in [1, 3]:
                self.selected_button_idx -= 1
        elif key == Qt.Key_D:
            if self.selected_button_idx in [0, 2]:
                self.selected_button_idx += 1
        else:
            super().keyPressEvent(event)

        self.update_button_highlight()

    def update_button_highlight(self):  # 定义一个方法用于更新按钮的高亮状态
        for idx, button in enumerate(self.buttons):
            if idx == self.selected_button_idx:  # 如果是选中的按钮
                button.setStyleSheet("""
                                        QPushButton {
                                            margin: 0px;          /* 设置外边距为 0 */
                                            padding: 0px;         /* 设置内边距为 0 */
                                            background-color: lightblue;    /* 设置背景颜色为浅蓝色 */
                                            border: 1px solid rgb(150, 150, 150);                   /* 移除边框 */
                                            color: black;                   /* 设置文字颜色 */
                                        }
                                        QPushButton:hover {
                                            color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
                                        }
                                        QPushButton:pressed {
                                            color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
                                        }
                                    """)
            else:
                # 如果按钮未被选中，设置按钮的样式表
                button.setStyleSheet("""
                                        QPushButton {
                                            margin: 0px;          /* 设置外边距为 0 */
                                            padding: 0px;         /* 设置内边距为 0 */
                                            background-color: transparent;  /* 设置背景颜色为透明 */
                                            border: 1px solid rgb(150, 150, 150);                   /* 移除边框 */
                                            color: blue;                   /* 设置文字颜色 */
                                        }
                                        
                                        QPushButton:hover {
                                            color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
                                        }
                                        QPushButton:pressed {
                                            color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
                                        }
                                    """)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()