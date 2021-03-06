# These are more than helpful!!
# https://python-pytube.readthedocs.io/en/latest/api.html
# https://python-pytube.readthedocs.io/en/latest/user/quickstart.html#downloading-a-video
# and tech with tim's pyqt5 playlist on yt

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
        self.comboBox.setGeometry(QtCore.QRect(10, 70, 300, 20))
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
        self.pushButton.clicked.connect(self.click_on_see_streams) # click event connected to click_on_select_stream()

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget) # this is the download button
        self.pushButton_2.setGeometry(QtCore.QRect(350, 60, 140, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.click_on_download)  # click event connected to click_on_download()

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

    def click_on_see_streams(self):
        global b
        b = create_backend_object()
        if b is not None:
            b.click_on_see_streams() # call a function of the same name from the backend; b --> backend class ka object

    def click_on_download(self):
        b.click_on_download() # call a function of the same name from the backend

    def already_in_combobox(self,text):
        # returns -1 if not in combobox; else returns index from 0 to n
        index = self.comboBox.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            return True
        else:
            return False

    def add_to_combobox(self, listy):
        for tup in listy:
            if not self.already_in_combobox(tup[1] + ' @ ' + str(tup[2]) + 'fps'): # why this check? --> if user click again on see streams button... then duplicate stream na aaye isliye...
                self.comboBox.addItem(tup[1] + ' @ ' + str(tup[2]) + 'fps')

    def return_selected_stream(self, listy):
        # See which item/ stream is selected in the combo box
        # returns itag of selected stream or returns None
        selection = self.comboBox.currentText() # of the format: 'xp @ yfps' or 'Select a stream to download'
        if selection == 'Select a stream to download':
            return None
        res, useless, fps = selection.split(' ')
        del useless
        fps = int(fps[0:2]) # '30fps' -->  '30'
        for tup in listy:
            if tup[1] == res and tup[2] == fps:
                return tup[0]


    def set_thumbnail(self, img_path):
        self.label_3.setPixmap(QtGui.QPixmap(img_path))

    def set_title(self, video_title):
        self.video_title_label.setText(video_title)

    def update_progress_bar(self, progress):
        self.progressBar.setProperty("value", progress)


class Backend():

    def __init__(self, url):
        self.yt = YouTube(url, on_progress_callback = self.return_download_progress) # 2nd arg? --> passed the reference of the function...
        self.video_title = self.yt.title
        self.listy = []  # will store the list of available streams to be shown to user; each element = tuple --> (itag, resolution, fps)

    def click_on_see_streams(self):

        # creating a downloads folder if it does not exist
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        # Clean video title
        self.clean_title()
        # Show video title to user
        f.set_title(self.video_title)
        # get and save and show thumbnail image (might take a few secs)
        self.get_and_save_and_set_thumbnail()
        # make a list of all available streams
        for i in self.yt.streams.all():
            if i.type == 'video' and i.resolution is not None:
                self.listy.append((i.itag, i.resolution, i.fps))
        # Add all streams to combo box
        f.add_to_combobox(self.listy)

    def clean_title(self):
        # now removing all characters that are not permitted by windows
        # replace(a,b) replaces all occurrences of a with b in string
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

    def get_and_save_and_set_thumbnail(self):
        img = Image.open(io.BytesIO(requests.get(self.yt.thumbnail_url, stream=True).content)).convert("RGB")
        img.save(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))
        if os.path.exists(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg')):
            f.set_thumbnail(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))
        else: # if user deletes thumbnail
            self.get_and_save_and_set_thumbnail()
        # now remove thumbnail
        os.remove(os.path.join('downloads', self.video_title + '-temp_thumbnail.jpeg'))

    def return_download_progress(self, stream = None, chunk=None, file_handle=None, remaining=None): # This is all gathered automatically by pytube and we don’t have to put any values in here.
        if remaining is None:
            remaining = 0
        progress = ((stream.filesize - remaining)/stream.filesize)*100
        f.update_progress_bar(progress)

    def click_on_download(self):
        # if the download button has been clicked once before, removing that progress and reseting it.
        f.update_progress_bar(0)
        # see which stream the user has selected
        itag = f.return_selected_stream(self.listy)
        if itag is None:
            # if user doesn't select a stream -> highest quality stream is selected
            stream = self.yt.streams.get_highest_resolution()
            if stream is None:
                # if for some reason highest quality stream cannot be selected, select the first stream
                stream = self.yt.streams.first()
        else:
            stream = self.yt.streams.get_by_itag(itag)
        # created a thread; now the process of download will be done on a separate thread...
        download_thread = threading.Thread(target = self.start_download_on_sep_thread, args = (stream,))
        # started that thread
        download_thread.start()

    def start_download_on_sep_thread(self, stream):
        # video will be downloaded to the downloads folder
        stream.download('downloads')


# ------- this is global stuff ---------

b = None # for backend object to remain global (as it is being declared in the f.click_on_see_streams()


def create_backend_object():
    """If user gives a non youtube urls or a url with youtube.com in it but that doesn't actually have a video on it...
    Here I read and  try to create a YouTube object, if no exception is raised => url is correct
    => a backend object can be created (Inside which another yt obj will be created, but that's none of this fun's
    business."""
    global b

    # read url given by user
    url_text = f.url.toPlainText()  # convert stuff in url (textEdit) to text
    url_text.strip()  # remove all leading and trailing spaces

    # return if the url is not of youtube
    if 'youtube.com' not in url_text:
        f.url.setPlainText("")  # clear the useless link
        f.show_popup('Not a YouTube link!')  # tell user that ain't a vaild url
        return None

    # return if no video exists at given url
    try:
        yt = YouTube(url_text)
    except exceptions.RegexMatchError:  # I observed that RegexMatchError is raised if url has no video on it...
        f.url.setPlainText("")  # clear the useless link
        f.show_popup('No video exists at given link!')
        del yt # to free up memory... (if exception is raised, delete it here)
        return None

    del yt  # to free up memory... (if no exception is raised, delete it here)

    b = Backend(url_text)
    return b


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    # frontend object ---> f
    f = Ui_MainWindow()
    f.setupUi(MainWindow)
    MainWindow.show()

    # where's backend object ---> b ? It's created in f.click_on_see_streams()

    sys.exit(app.exec_())