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


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt Key Navigation Example with Button Highlight')

        grid = QGridLayout()

        self.buttons = [
            QPushButton('Button 1'),
            QPushButton('Button 2'),
            QPushButton('Button 3'),
            QPushButton('Button 4')
        ]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

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

    def update_button_highlight(self):
        for idx, button in enumerate(self.buttons):
            if idx == self.selected_button_idx:
                button.setStyleSheet("background-color: lightblue")
            else:
                button.setStyleSheet("")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()