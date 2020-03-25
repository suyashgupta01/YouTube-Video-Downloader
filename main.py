# These 2 links are mote than helpful!!
# https://python-pytube.readthedocs.io/en/latest/api.html
# https://python-pytube.readthedocs.io/en/latest/user/quickstart.html#downloading-a-video
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pytube import YouTube, exceptions
from PIL import Image
import requests
import io, sys, time, os, threading

class Ui_MainWindow():

    # data members declared by me that are not related to the ui: stream, video_title

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)

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

        self.video_title_label = QtWidgets.QLabel(self.centralwidget)
        self.video_title_label.setGeometry(QtCore.QRect(10, 150, 431, 31))
        self.video_title_label.setObjectName("video_title_label")

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

        # drop down menu or combobox
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 70, 57, 16))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Select a stream to download")
        # set this as default selected item
        default_index = self.comboBox.findText("Select a stream to download", QtCore.Qt.MatchFixedString) # returns the index of the item in combobox
        self.comboBox.setCurrentIndex(default_index)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 190, 431, 171))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap('default_thumbnail.jpeg'))  # view thumbnail of video
        self.label_3.setObjectName("label_3")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)  # this is the select stream button....
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 100, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(b.click_on_select_stream) # click event connected to click_on_select_stream()

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget) # this is the download button
        self.pushButton_2.setGeometry(QtCore.QRect(250, 60, 161, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(b.click_on_download)  # click event connected to click_on_download()

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
        MainWindow.setWindowTitle(_translate("MainWindow", "Gupta's YT downloader"))
        self.label.setText(_translate("MainWindow", "URL of Youtube Video: "))
        self.label_2.setText(_translate("MainWindow", "Available Streams:"))
        self.pushButton.setText(_translate("MainWindow", "See streams!"))
        self.pushButton_2.setText(_translate("MainWindow", "Download!"))
        self.video_title_label.setText(_translate("MainWindow", ""))

    def show_popup(self, text_to_show):
        msg = QMessageBox()
        msg.setWindowTitle("Oye, watcha doin?")
        msg.setText(text_to_show)
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()  # this just shows the msg box -> don't ask TechWithTim how this works

    def set_thumbnail(self, thumbnail_image):
        """set thumbnail as per the video of given url"""
        Ui_MainWindow.label_3.setPixmap(QtGui.QPixmap(thumbnail_image))

class Backend():

    def __init__(self):

    def update_progress_bar(self, chunk = None, file_handle = None, remaining = None): # This is all gathered automatically by pytube and we don’t have to put any values in here.
        if remaining is None:
             remaining = 0
        progress = ((self.stream.filesize - remaining)/self.stream.filesize)*100
        self.progressBar.setProperty("value", progress)


    # def update_progress_bar(self, stream = None, chunk = None, file_handle = None, remaining = None): # This is all gathered automatically by pytube and we don’t have to put any values in here.
    #     if remaining is None:
    #         remaining = 0
    #     progress = ((stream.filesize - remaining)/stream.filesize)*100
    #     self.progressBar.setProperty("value", progress)


    def click_on_download(self):
        # remove thumbnail
        os.remove(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))
        # now the process of download will be done on a separate thread:
        download_thread = threading.Thread(target = self.start_download_on_sep_thread) # created a thread
        download_thread.start() # started that thread

    def start_download_on_sep_thread(self):
        # video will be downloaded to the downloads folder
        self.stream.download('downloads')

    def click_on_select_stream(self):

        # creating a downloads folder if it does not exist
        if not os.path.exists('downloads'):
            os.mkdir('downloads')

        # read url given by user
        url_text = Ui_MainWindow.url.toPlainText()  # convert stuff in url (textEdit) to text
        url_text.strip() # remove all leading and trailing spaces

        # return if the url is not of youtube
        if 'youtube.com' not in url_text:
            Ui_MainWindow.url.setPlainText("")  # clear the useless link
            Ui_MainWindow.show_popup('Not a YouTube link!') # tell user that ain't a vaild url
            return # just stop the execution of function man!

        # Create YouTube Object
        try:
            yt = YouTube(url_text, on_complete_callback = self.update_progress_bar)
            # 2nd arg? --> passed the reference of the function...
        except exceptions.RegexMatchError: # I observed that RegexMatchError is raised if url has no video on it...
            Ui_MainWindow.url.setPlainText("")  # clear the useless link
            Ui_MainWindow.show_popup('No video exists at given link!')
            return # just stop the execution of function man!

        # Get video title
        self.video_title = yt.title
        # now removing all characters that are not permitted by windows
        # replace(a,b) replaces all occourances of a with b in string
        if '\\' in self.video_title:
            self.video_title = self.video_title.replace('\\', '')
        if ':' in self.video_title:
            self.video_title = self.video_title.replace(':', '')
        if '<' in self.video_title:
            self.video_title = self.video_title.replace('<', '')
        if '>' in self.video_title:
            self.video_title = self.video_title.replace('>', '')
        if '|' in self.video_title:
            self.video_title = self.video_title.replace('|', '')
        if '*' in self.video_title:
            self.video_title = self.video_title.replace('*', '')
        if '"' in self.video_title:
            self.video_title = self.video_title.replace('"', '')
        if '?' in self.video_title:
            self.video_title = self.video_title.replace('?', '')

        # Show video title to user
        self.video_title_label.setText(self.video_title)

        # get and save thumbnail image (might take a few secs)
        img = Image.open(io.BytesIO(requests.get(yt.thumbnail_url, stream=True).content)).convert("RGB")
        img.save(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))
        while True: # jab tak thumbnail download na ho jaye, wait...!
            if os.path.exists(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg')):
                Ui_MainWindow.set_thumbnail(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))
                break
            else:
                time.sleep(2)

        # see the available streams and add items in combo box

        p144 = False
        p240 = False
        p360 = False
        p480 = False
        p720 = False
        p1080 = False
        p1440 = False
        p2160 = False

        all_streams = yt.streams.all()

        for i in all_streams:
            if i.resolution == '144p':
                p144 = True
            if i.resolution == '240p':
                p240 = True
            if i.resolution == '360p':
                p360 = True
            if i.resolution == '480p':
                p480 = True
            if i.resolution == '720p':
                p720 = True
            if i.resolution == '1080p':
                p1080 = True
            if i.resolution == '1440p':
                p1440 = True
            if i.resolution == '2160p':
                p2160 = True

        if p144: # returns None or Stream object (which is not None => True...)
            Ui_MainWindow.comboBox.addItem('144p')
        if p240:
            Ui_MainWindow.comboBox.addItem('240p')
        if p360:
            Ui_MainWindow.comboBox.addItem('360p')
        if p480:
            Ui_MainWindow.comboBox.addItem('480p')
        if p720:
            Ui_MainWindow.comboBox.addItem('780p')
        if p1080:
            Ui_MainWindow.comboBox.addItem('1080p')
        if p1440:
            Ui_MainWindow.comboBox.addItem('1440p | 2K')
        if p2160:
            Ui_MainWindow.comboBox.addItem('2160p | 4K')

        # See which item/ stream is selected in the combo box
        selected_stream = Ui_MainWindow.comboBox.currentText()
        if selected_stream == 'Select a stream to download':
            self.stream = yt.streams.first() # if user doesn't select a stream -> highest quality video is downloaded
        elif selected_stream == '144p':
            self.stream = yt.streams.get_by_resolution('144p')
        elif selected_stream == '240p':
            self.stream = yt.streams.get_by_resolution('240p')
        elif selected_stream == '360p':
            self.stream = yt.streams.get_by_resolution('360p')
        elif selected_stream == '480p':
            self.stream = yt.streams.get_by_resolution('480p')
        elif selected_stream == '720p':
            self.stream = yt.streams.get_by_resolution('720p')
        elif selected_stream == '1080p':
            self.stream = yt.streams.get_by_resolution('1080p')
        elif selected_stream == '1440p | 2K':
            self.stream = yt.streams.get_by_resolution('1440')
        elif selected_stream == '2160p | 4K':
            self.stream = yt.streams.get_by_resolution('2160p')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    # frontend object ---> ui
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # backend object ---> b
    b = Backend()

    sys.exit(app.exec_())