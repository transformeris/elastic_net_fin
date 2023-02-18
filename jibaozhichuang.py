# # import sys
# # from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
# # from PyQt5.QtCore import Qt
# #
# #
# # class MyWidget(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Button Selection")
# #         self.setGeometry(100, 100, 300, 200)
# #         self.button1 = QPushButton("Button 1")
# #         self.button2 = QPushButton("Button 2")
# #         self.button3 = QPushButton("Button 3")
# #         self.button4 = QPushButton("Button 4")
# #         layout = QGridLayout()
# #         layout.addWidget(self.button1, 0, 0)
# #         layout.addWidget(self.button2, 0, 1)
# #         layout.addWidget(self.button3, 1, 0)
# #         layout.addWidget(self.button4, 1, 1)
# #         self.setLayout(layout)
# #         self.selected_button = self.button1
# #         # self.selected_button.setStyleSheet("background-color: yellow")
# #
# #     def keyPressEvent(self, event):
# #         if event.key() == Qt.Key_Up:
# #             if self.selected_button in [self.button3, self.button4]:
# #                 self.selected_button.setStyleSheet("")
# #                 self.selected_button = [self.button1, self.button2][
# #                     [self.button1, self.button2].index(self.selected_button) - 2]
# #                 self.selected_button.setStyleSheet("background-color: yellow")
# #         elif event.key() == Qt.Key_Down:
# #             if self.selected_button in [self.button1, self.button2]:
# #                 self.selected_button.setStyleSheet("")
# #                 self.selected_button = [self.button3, self.button4][
# #                     [self.button3, self.button4].index(self.selected_button) - 2]
# #                 self.selected_button.setStyleSheet("background-color: yellow")
# #         elif event.key() == Qt.Key_Left:
# #             if self.selected_button in [self.button2, self.button4]:
# #                 self.selected_button.setStyleSheet("")
# #                 self.selected_button = [self.button1, self.button3][
# #                     [self.button1, self.button3].index(self.selected_button) - 1]
# #                 self.selected_button.setStyleSheet("background-color: yellow")
# #         elif event.key() == Qt.Key_Right:
# #             if self.selected_button in [self.button1, self.button3]:
# #                 self.selected_button.setStyleSheet("")
# #                 self.selected_button = [self.button2, self.button4][
# #                     [self.button2, self.button4].index(self.selected_button) - 1]
# #                 self.selected_button.setStyleSheet("background-color: yellow")
# #
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     widget = MyWidget()
# #     widget.show()
# #     sys.exit(app.exec_())
#
#
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
# from PyQt5.QtCore import Qt
#
#
# class MyWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Button Selection")
#         self.setGeometry(100, 100, 300, 200)
#         self.button1 = QPushButton("Button 1")
#         self.button2 = QPushButton("Button 2")
#         self.button3 = QPushButton("Button 3")
#         self.button4 = QPushButton("Button 4")
#         layout = QGridLayout()
#         layout.addWidget(self.button1, 0, 0)
#         layout.addWidget(self.button2, 0, 1)
#         layout.addWidget(self.button3, 1, 0)
#         layout.addWidget(self.button4, 1, 1)
#         self.setLayout(layout)
#         self.selected_button = None
#
#     def select_button(self, button):
#         if self.selected_button:
#             self.selected_button.setStyleSheet("")
#         self.selected_button = button
#         self.selected_button.setStyleSheet("background-color: green")
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Up:
#             if self.selected_button in [self.button3, self.button4]:
#                 self.select_button(
#                     [self.button1, self.button2][[self.button1, self.button2].index(self.selected_button) - 2])
#         elif event.key() == Qt.Key_Down:
#             if self.selected_button in [self.button1, self.button2]:
#                 self.select_button(
#                     [self.button3, self.button4][[self.button3, self.button4].index(self.selected_button) - 2])
#         elif event.key() == Qt.Key_Left:
#             if self.selected_button in [self.button2, self.button4]:
#                 self.select_button(
#                     [self.button1, self.button3][[self.button1, self.button3].index(self.selected_button) - 1])
#         elif event.key() == Qt.Key_Right:
#             if self.selected_button in [self.button1, self.button3]:
#                 self.select_button(
#                     [self.button2, self.button4][[self.button2, self.button4].index(self.selected_button) - 1])
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = MyWidget()
#     widget.select_button(widget.button2)  # 默认选中第一个按钮
#     widget.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Selection")
        self.setGeometry(100, 100, 300, 200)
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton("Button 4")
        layout = QGridLayout()
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 0, 1)
        layout.addWidget(self.button3, 1, 0)
        layout.addWidget(self.button4, 1, 1)
        self.setLayout(layout)
        self.selected_button = None
        self.button3.setFocus()
        # self.selected_button(self.button3)

    # def select_button(self, button):
    #     if self.selected_button:
    #         self.selected_button.setStyleSheet("")
    #     self.selected_button = button
    #     self.selected_button.setStyleSheet("background-color: yellow")
    # def select_button(self, button):
    #     if self.selected_button:
    #         self.selected_button.setFocusPolicy(Qt.NoFocus)  # 取消原有的选中效果
    #     self.selected_button = button
    #     self.selected_button.setFocusPolicy(Qt.StrongFocus)  # 为新选中的按钮添加选中效果
    #     self.selected_button.setStyleSheet("background-color: yellow")
    def select_button(self, button):
        if self.selected_button:
            self.selected_button.setFocusPolicy(Qt.NoFocus)  # 取消原有的选中效果
            self.selected_button.setStyleSheet("")  # 取消原有的背景颜色
        self.selected_button = button
        self.selected_button.setFocusPolicy(Qt.StrongFocus)  # 为新选中的按钮添加选中效果
        self.selected_button.setStyleSheet("background-color: yellow")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            print('按下了上键')
            if self.selected_button ==self.button3:
                self.select_button(self.button1)
        elif event.key() == Qt.Key_S:
            print('按下了下键')
            if self.selected_button ==self.button1:
                self.select_button(self.button3)
            # if self.selected_button in [self.button1, self.button2]:
            #     self.select_button(
            #         [self.button3, self.button4])
        elif event.key() == Qt.Key_A:
            print('按下了左键')
            if self.selected_button in [self.button2, self.button4]:
                self.select_button(
                    [self.button1, self.button3][[self.button1, self.button3].index(self.selected_button) - 2])
        elif event.key() == Qt.Key_D:
            print('按下了右键')
            if self.selected_button in [self.button1, self.button3]:
                self.select_button(
                    [self.button2, self.button4][[self.button2, self.button4].index(self.selected_button) - 2])
        elif event.key() == Qt.Key_Return:
            if self.selected_button == self.button1:
                self.new_window()
        super().keyPressEvent(event)

    def new_window(self):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("New Window")
        self.new_window.setGeometry(200, 200, 200, 200)
        label = QLabel("G", self.new_window)
        label.setAlignment(Qt.AlignCenter)
        self.new_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.select_button(widget.button1)  # 默认选中第一个按钮
    widget.show()
    sys.exit(app.exec_())