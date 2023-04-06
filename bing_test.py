from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget(self)
        self.widget1 = QWidget()
        self.widget2 = QWidget()
        self.stack.addWidget(self.widget1)
        self.stack.addWidget(self.widget2)
        self.button = QPushButton('Next', self.widget1)
        self.button.move(100, 100)
        self.button.clicked.connect(self.nextPage)
        self.stack.setCurrentWidget(self.widget1)
        self.show()

    def nextPage(self):
        self.stack.setCurrentWidget(self.widget2)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.stack.currentWidget() == self.widget1:
                self.stack.setCurrentWidget(self.widget2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())