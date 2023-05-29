import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QLabel
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
            QPushButton('Button 4'),
            QPushButton('返回')
        ]
        self.buttons[0].setStyleSheet("""
                                        QPushButton {
                                            position: fixed;  /* 将按钮固定在页面上 */
                                            pointer-events: none; /* 禁用按钮的交互 */
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
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]

        for button, pos in zip(self.buttons, positions):
            grid.addWidget(button, *pos)

        self.setLayout(grid)

        # Initialize the selected button index
        self.selected_button_idx = 0

        self.update_button_highlight()

        # Add a new widget to the layout
        self.line_edit = QLineEdit()
        grid.addWidget(self.line_edit, 3, 0, 1, 2)

        # Connect the returnPressed signal of the line edit to a slot
        self.buttons[0].clicked.connect(self.add_new_widget)
        self.buttons[4].clicked.connect(self.return_to_previous_page)

    def add_new_widget(self):
        self.new_widget = QLabel('New Widget')
        self.layout().addWidget(self.new_widget, 3, 0, 1, 2)
        self.buttons[0].clicked.disconnect()
        self.buttons[0].clicked.connect(self.new_widget.setFocus)

    def return_to_previous_page(self):
        self.layout().removeWidget(self.new_widget)
        self.new_widget.deleteLater()
        self.buttons[0].clicked.connect(self.add_new_widget)

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
        elif key == Qt.Key_Return:
            if self.selected_button_idx == 0:
                self.add_new_widget()
            elif self.selected_button_idx == 4:
                self.return_to_previous_page()
        else:
            super().keyPressEvent(event)

        self.update_button_highlight()

    def update_button_highlight(self):
        for idx, button in enumerate(self.buttons):
            if idx == self.selected_button_idx:
                button.setStyleSheet("background-color: lightblue")
            else:
                button.setStyleSheet("""
                                        QPushButton {
                                            position: fixed;  /* 将按钮固定在页面上 */
                                            pointer-events: none; /* 禁用按钮的交互 */
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()