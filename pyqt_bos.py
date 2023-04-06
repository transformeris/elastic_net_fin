import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

button = QPushButton("点击我")
button.setStyleSheet("""
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

layout.addWidget(button)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())