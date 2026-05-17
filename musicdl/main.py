from PySide6.QtWidgets import QApplication, QWidget
import sys
import re

from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QMessageBox,
)


class Ui_Form(object):

    def setupUi(self, Form):
        """setupUi"""
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(703, 639)
        font = QFont()
        font.setBold(False)
        Form.setFont(font)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        font1 = QFont()
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.line_edit = QLineEdit(Form)
        self.line_edit.setObjectName("lineEdit")

        self.horizontalLayout.addWidget(self.line_edit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_srch = QPushButton(Form)
        self.btn_srch.setObjectName("btn_srch")
        self.btn_srch.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_srch)

        self.btn_nextpg = QPushButton(Form)
        self.btn_nextpg.setObjectName("btn_nextpg")
        self.btn_nextpg.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_nextpg)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_clear = QPushButton(Form)
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_clear)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        """
        retranslateUi
        在此连接控件和槽函数
        """
        Form.setWindowTitle(
            QCoreApplication.translate("Form", "\u97f3\u4e50\u4e0b\u8f7d\u5668", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "Form", "\u8bf7\u8f93\u5165\u8981\u4e0b\u8f7d\u7684\u97f3\u4e50", None
            )
        )

        # 文本输入框
        self.line_edit.returnPressed.connect(Form.search)

        # ListWidget
        # itemDoubleClicked事件, 自动将被双击的item对象传递给槽函数
        self.listWidget.itemDoubleClicked.connect(Form.download)

        # 搜索按钮
        self.btn_srch.setText(QCoreApplication.translate("Form", "\u641c\u7d22", None))
        self.btn_srch.clicked.connect(Form.search)

        # 下一页按钮
        self.btn_nextpg.setText(
            QCoreApplication.translate("Form", "\u4e0b\u4e00\u9875", None)
        )
        self.btn_nextpg.clicked.connect(Form.next_page)

        # 清空按钮
        self.btn_clear.setText(QCoreApplication.translate("Form", "\u6e05\u7a7a", None))
        self.btn_clear.clicked.connect(Form.clear)


class MyWindow(QWidget):
    """
    创建一个窗口类,该类继承自QWidget
    """

    # 创建UI
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 歌名, 页数
        self.song_name = ""
        self.page_no = 1

    # 搜索按钮的槽函数
    def search(self):
        # 禁用按钮
        self.ui.btn_srch.setDisabled(True)
        self.ui.btn_nextpg.setDisabled(True)
        self.ui.btn_clear.setDisabled(True)

        # 获取文本框的输入
        song_name = self.ui.line_edit.text().strip()

        # 继续搜索同一首歌时, 自动加载下一页; 否则, 重新搜索
        if song_name == self.song_name:
            self.page_no += 1
        else:
            self.song_name = song_name
            self.page_no = 1

            # 清空ListWidget的内容
            self.ui.listWidget.clear()

        # 调用爬虫
        from get_info import dl_info

        success, info = dl_info(self.song_name, self.page_no)

        if success:
            for item in info:
                item_info = f"{item['title']} -- {item['author']} -- {item['url']}"

                # ListWidget添加元素
                self.ui.listWidget.addItem(item_info)
        else:
            QMessageBox.information(self, "提示", "未搜索到歌曲信息！")

        # 启用按钮
        self.ui.btn_srch.setEnabled(True)
        self.ui.btn_nextpg.setEnabled(True)
        self.ui.btn_clear.setEnabled(True)

    # 下一页按钮的槽函数
    def next_page(self):
        # 禁用按钮
        self.ui.btn_srch.setDisabled(True)
        self.ui.btn_nextpg.setDisabled(True)
        self.ui.btn_clear.setDisabled(True)

        self.page_no += 1

        # 调用爬虫
        from get_info import dl_info

        success, info = dl_info(self.song_name, self.page_no)

        if success:
            for item in info:
                item_info = f"{item['title']} -- {item['author']} -- {item['url']}"

                # ListWidget添加元素
                self.ui.listWidget.addItem(item_info)
        else:
            QMessageBox.information(self, "提示", "未搜索到歌曲信息！")

        # 启用按钮
        self.ui.btn_srch.setEnabled(True)
        self.ui.btn_nextpg.setEnabled(True)
        self.ui.btn_clear.setEnabled(True)

    # 清空按钮的槽函数
    def clear(self):
        # 禁用按钮
        self.ui.btn_srch.setDisabled(True)
        self.ui.btn_nextpg.setDisabled(True)
        self.ui.btn_clear.setDisabled(True)

        self.song_name = ""
        self.page_no = 1

        # 文本框
        self.ui.line_edit.setText("")

        # 清空ListWidget的内容
        self.ui.listWidget.clear()

        # 启用按钮
        self.ui.btn_srch.setEnabled(True)
        self.ui.btn_nextpg.setEnabled(True)
        self.ui.btn_clear.setEnabled(True)

    # ListWidget的 itemDoubleClicked 槽函数
    # 接收被双击的item对象作为参数
    def download(self, item):
        # 取得双击对象的信息
        text = item.text()
        lst = str.split(text, "--")
        dl_title = f"{lst[0].strip()}_{lst[1].strip()}"
        dl_url = lst[2].strip()
        # print(dl_title, dl_url)

        # 下载前弹窗进行确认
        reply = QMessageBox.question(
            self,
            "下载确认",
            "确定要下载该歌曲吗?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        # if reply == QMessageBox.Yes:
        #     QMessageBox.information(self, "提示", "reply \n 下载爬虫开发中,敬请期待！")

        # 调用爬虫
        from download_song import dl_song

        success = dl_song(dl_title, dl_url)

        if success:
            QMessageBox.information(self, "下载成功", "歌曲下载成功")
        else:
            QMessageBox.information(
                self, "下载失败", "歌曲下载失败,请确认是否有网易VIP"
            )


def main():
    # 创建应用
    app = QApplication(sys.argv)

    # 创建窗口并显示
    window = MyWindow()
    window.show()

    # 启动应用循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
