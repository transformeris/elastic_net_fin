import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt List Widget')

        # 创建一个列表框
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItem('Item 1')
        self.list_widget.addItem('Item 2')
        self.list_widget.addItem('Item 3')
        self.list_widget.addItem('Item 4')
        self.list_widget.addItem('Item 5')

        # 创建一个布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        # 检查键盘按键编码
        if event.key() == QtCore.Qt.Key_Up:
            # 获取当前选中项目的索引
            index = self.list_widget.currentRow()
            if index > 0:
                # 将当前选中项目的背

                item = self.list_widget.item(index)
                item.setBackground(QtGui.QColor('#ffffff'))

                # 将上一个项目设为当前选中项目
                self.list_widget.setCurrentRow(index - 1)

                # 将新的当前选中项目的背景色更改为黄色
                item = self.list_widget.item(index - 1)
                item.setBackground(QtGui.QColor('yellow'))
        elif event.key() == QtCore.Qt.Key_Down:
            index = self.list_widget.currentRow()
            if index < self.list_widget.count() - 1:
                item = self.list_widget.item(index)
                item.setBackground(QtGui.QColor('#ffffff'))
                self.list_widget.setCurrentRow(index + 1)
                item = self.list_widget.item(index + 1)
                item.setBackground(QtGui.QC0olor('yellow'))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())