import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout,QStackedWidget,QSizePolicy
from PyQt5.QtCore import Qt
# class Window1(QWidget):
#     def initUI(self):
#         grid = QGridLayout()
#         grid.setHorizontalSpacing(0)  # 设置水平间距为 10 像素
#         grid.setVerticalSpacing(0)  # 设置垂直间距为 20 像素
#         self.buttons = [
#             QPushButton('按键 1'),
#             QPushButton('按键 2'),
#             QPushButton('按键 3'),
#             QPushButton('按键 4'),
#         ]
#         for button in self.buttons:
#             button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#
#
#         positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
#         for button, pos in zip(self.buttons, positions):
#             grid.addWidget(button, *pos)
#
#
#         self.setLayout(grid)
#
#         # Initialize the selected button index
#         self.selected_button_idx = 0
#
#         self.update_button_highlight()
#
#     def keyPressEvent(self, event):
#         key = event.key()
#
#         if key == Qt.Key_W:
#             if self.selected_button_idx in [2, 3]:
#                 self.selected_button_idx -= 2
#         elif key == Qt.Key_S:
#             if self.selected_button_idx in [0, 1]:
#                 self.selected_button_idx += 2
#         elif key == Qt.Key_A:
#             if self.selected_button_idx in [1, 3]:
#                 self.selected_button_idx -= 1
#         elif key == Qt.Key_D:
#             if self.selected_button_idx in [0, 2]:
#                 self.selected_button_idx += 1
#         else:
#             super().keyPressEvent(event)
#
#         self.update_button_highlight()
#
#     def update_button_highlight(self):  # 定义一个方法用于更新按钮的高亮状态
#         for idx, button in enumerate(self.buttons):
#             if idx == self.selected_button_idx:  # 如果是选中的按钮
#                 button.setStyleSheet("""
#                                         QPushButton {
#                                             margin: 0px;          /* 设置外边距为 0 */
#                                             padding: 0px;         /* 设置内边距为 0 */
#                                             background-color: lightblue;    /* 设置背景颜色为浅蓝色 */
#                                             border: 1px solid rgb(150, 150, 150);                   /* 移除边框 */
#                                             color: black;                   /* 设置文字颜色 */
#                                         }
#                                         QPushButton:hover {
#                                             color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
#                                         }
#                                         QPushButton:pressed {
#                                             color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
#                                         }
#                                     """)
#             else:
#                 # 如果按钮未被选中，设置按钮的样式表
#                 button.setStyleSheet("""
#                                         QPushButton {
#                                             margin: 0px;          /* 设置外边距为 0 */
#                                             padding: 0px;         /* 设置内边距为 0 */
#                                             background-color: transparent;  /* 设置背景颜色为透明 */
#                                             border: 1px solid rgb(150, 150, 150);                   /* 移除边框 */
#                                             color: blue;                   /* 设置文字颜色 */
#                                         }
#
#                                         QPushButton:hover {
#                                             color: blue;                    /* 鼠标悬停时，设置文字颜色为蓝色 */
#                                         }
#                                         QPushButton:pressed {
#                                             color: red;                     /* 鼠标按下时，设置文字颜色为红色 */
#                                         }
#                                     """)


class Window1(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    def initUI(self):

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)  # 设置水平间距为 10 像素
        grid.setVerticalSpacing(0)  # 设置垂直间距为 20 像素
        self.buttons = [

            QPushButton('按键 1'),
            QPushButton('按键 2'),
            QPushButton('按键 3'),
            QPushButton('按键 4'),
        ]
        for button in self.buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for button, pos in zip(self.buttons, positions):
            grid.addWidget(button, *pos)




        # Initialize the selected button index
        # self.selected_button_idx = 0
        self.selected_row = 0
        self.selected_col = 0
        self.m=2
        self.n=2
        self.update_button_highlight()
        self.setLayout(grid)
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_W and self.selected_row > 0:
            self.selected_row -= 1
        elif key == Qt.Key_S and self.selected_row < self.n - 1:
            self.selected_row += 1
        elif key == Qt.Key_A and self.selected_col > 0:
            self.selected_col -= 1
        elif key == Qt.Key_D and self.selected_col < self.m - 1:
            self.selected_col += 1
        else:
            super().keyPressEvent(event)

        self.update_button_highlight()


    def update_button_highlight(self):
        for i in range(self.n):
            for j in range(self.m):
                button = self.buttons[i][j]
                if i == self.selected_row and j == self.selected_col:
                    # 设置选中按钮的样式
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
                    # 设置未选中按钮的样式
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window1()
    window.show()
    sys.exit(app.exec_())


