import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem,QStackedWidget
from PyQt5.QtCore import Qt
# 创建三个小部件，分别代表三个页面
page1 = QWidget()
page2 = QWidget()
page3 = QWidget()

# 将这三个部件添加到 QStackedWidget 容器中
stacked_widget = QStackedWidget()
stacked_widget.addWidget(page1)
stacked_widget.addWidget(page2)
stacked_widget.addWidget(page3)

# 在这里添加代码以设置每个页面的内容

# 切换页面
stacked_widget.setCurrentIndex(1)  # 显示 page2
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建QListWidget
        self.list_widget = QListWidget()

        # 添加几个选项
        self.list_widget.addItem('选项1')
        self.list_widget.addItem('选项2')
        self.list_widget.addItem('选项3')
        self.list_widget.addItem('选项4')
        self.list_widget.addItem('选项5')

        # 绑定按键事件处





        self.list_widget.installEventFilter(self)


            # 添加QListWidget到布局
        layout.addWidget(self.list_widget)

    # 设置窗口的布局
        self.setLayout(layout)

    def eventFilter(self, source, event):
        if (event.type() == event.KeyPress and
            source is self.list_widget):
            key = event.key()
            if key == Qt.Key_Down:
                # 向下移动选中项
                current_row = self.list_widget.currentRow()
                if current_row < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(current_row + 1)
            elif key == Qt.Key_Up:
                # 向上移动选中项
                current_row = self.list_widget.currentRow()
                if current_row > 0:
                    self.list_widget.setCurrentRow(current_row - 1)
            elif key == Qt.Key_Return:
                # 回车键，确定选中的选项
                current_item = self.list_widget.currentItem()
                print('选中的选项：', 'current_item.text()')
        return super().eventFilter(source, event)
if __name__ =='__main__':
    app = QApplication(sys.argv)


    # 创建主窗口
    main_window = MainWindow()

    # 显示主窗口
    main_window.show()

    sys.exit(app.exec_())