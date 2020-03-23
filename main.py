# These 2 links are mote than helpful!!
# https://python-pytube.readthedocs.io/en/latest/api.html
# https://python-pytube.readthedocs.io/en/latest/user/quickstart.html#downloading-a-video
from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube, exceptions
from PIL import Image
import requests
import io, sys, time, os, threading

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 368)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.url = QtWidgets.QTextEdit(self.centralwidget)
        self.url.setGeometry(QtCore.QRect(130, 10, 241, 21))
        self.url.setObjectName("url")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 120, 441, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # all radio buttons start ----------------------------------------

        # self.b1 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b1.setGeometry(QtCore.QRect(10, 70, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b1.setFont(font)
        # self.b1.setObjectName("b1")
        #
        # self.b2 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b2.setGeometry(QtCore.QRect(90, 70, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b2.setFont(font)
        # self.b2.setObjectName("b2")
        #
        # self.b3 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b3.setGeometry(QtCore.QRect(160, 70, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b3.setFont(font)
        # self.b3.setObjectName("b3")
        #
        # self.b4 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b4.setGeometry(QtCore.QRect(240, 70, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b4.setFont(font)
        # self.b4.setObjectName("b4")
        #
        # self.b5 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b5.setGeometry(QtCore.QRect(310, 70, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b5.setFont(font)
        # self.b5.setObjectName("b5")
        #
        # self.b6 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b6.setGeometry(QtCore.QRect(10, 90, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b6.setFont(font)
        # self.b6.setObjectName("b6")
        #
        # self.b7 = QtWidgets.QRadioButton(self.centralwidget)
        # self.b7.setGeometry(QtCore.QRect(90, 90, 57, 16))
        # font = QtGui.QFont()
        # font.setPointSize(8)
        # self.b7.setFont(font)
        # self.b7.setObjectName("b7")

        # all radio buttons end ----------------------------------------

        # drop down menu
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 70, 57, 16))
        self.comboBox.setObjectName("comboBox")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 431, 171))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap('default_thumbnail.jpeg'))  # view thumbnail of video
        self.label_3.setObjectName("label_3")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)  # this is the download button
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 65, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click_on_download)  # connected 'click event' to 'click_on_download' function

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "URL of Youtube Video: "))
        self.label_2.setText(_translate("MainWindow", "Available Streams:"))
        # self.b1.setText(_translate("MainWindow", "1080p"))
        # self.b2.setText(_translate("MainWindow", "720p"))
        # self.b7.setText(_translate("MainWindow", "more "))
        # self.b3.setText(_translate("MainWindow", "360p"))
        # self.b6.setText(_translate("MainWindow", "audio only"))
        # self.b4.setText(_translate("MainWindow", "240p"))
        # self.b5.setText(_translate("MainWindow", "144p"))
        self.pushButton.setText(_translate("MainWindow", "Download!"))

    def set_thumbnail(self, thumbnail_image):
        """set thumbnail as per the video of given url"""
        self.label_3.setPixmap(QtGui.QPixmap(thumbnail_image))

    def update_progress_bar(self, stream = None, chunk = None, file_handle = None, remaining = None): # This is all gathered automatically by pytube and we don’t have to put any values in here.
        if remaining == None:
            remaining = 0
        progress = ((stream.filesize - remaining)/stream.filesize)*100
        self.progressBar.setProperty("value", progress)

    def download_video(self, stream, video_title):
        stream.download('downloads')  # video downloaded to the downloads folder
        os.remove(os.path.join('downloads', video_title + '-temp_thumbnail.jpeg'))  # remove thumbnail after video is downloaded.

    def click_on_download(self):

        # creating a downloads folder if it does not exist
        if not os.path.exists('downloads'):
            os.mkdir('downloads')

        url_text = self.url.toPlainText()  # convert stuff in url (textEdit) to text
        url_text.strip() # remove all leading and trailing spaces
        if 'youtube.com' not in url_text:
            self.url.setPlainText('Not a YouTube link!')  # tell user that ain't a vaild url
            return # just stop the execution of function man!

        try:
            yt = YouTube(url_text, on_complete_callback = self.update_progress_bar)
            # create YouTube object; 2nd arg? --> passed the reference of the function...
        except exceptions.RegexMatchError:
            self.url.setPlainText('No video exits at given link!')
            return # just stop the execution of function man!

        video_title = yt.title
        # now removing all characters that are not permitted by windows
        # replace(a,b) replaces all occourances of a with b in string
        if '\\' in video_title:
            video_title = video_title.replace('\\', '')
        if ':' in video_title:
            video_title = video_title.replace(':', '')
        if '<' in video_title:
            video_title = video_title.replace('<', '')
        if '>' in video_title:
            video_title = video_title.replace('>', '')
        if '|' in video_title:
            video_title = video_title.replace('|', '')
        if '*' in video_title:
            video_title = video_title.replace('*', '')
        if '"' in video_title:
            video_title = video_title.replace('"', '')
        if '?' in video_title:
            video_title = video_title.replace('?', '')

        self.url.setPlainText(video_title) # put title in place of url (user ko dikhane ke liye)

        # get and save thumbnail image (might take a few secs)
        img = Image.open(io.BytesIO(requests.get(yt.thumbnail_url, stream=True).content)).convert("RGB")
        img.save(os.path.join('downloads', video_title + '-temp_thumbnail.jpeg'))
        while True: # jab tak thumbnail download na ho jaye, wait...!
            if os.path.exists(os.path.join('downloads', video_title + '-temp_thumbnail.jpeg')):
                self.set_thumbnail(os.path.join('downloads', video_title + '-temp_thumbnail.jpeg'))
                break
            else:
                time.sleep(2)

        # Get all streams and modify values of radio buttons as per available streams...
        # all_streams = yt.streams.all()
        # for item in all_streams:
        #     if
        stream = yt.streams.first()


        # now the process of download will be done on a separate thread:
        download_thread = threading.Thread(target = self.download_video, args = (stream, video_title)) # created a thread
        download_thread.start() # started that thread


# self.textEdit.setPlainText(mytext)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())