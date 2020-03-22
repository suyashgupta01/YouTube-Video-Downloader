from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pytube import YouTube

# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = Ui_MainWindow()
# ui.setupUi(MainWindow)
# MainWindow.show()

# url = ui.click_on_download()
url = 'https://www.youtube.com/watch?v=9bZkp7q19f0'
yt = YouTube(url)
print(yt.title)

# sys.exit(app.exec_())