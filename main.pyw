# Cross-platform libs
import threading
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool
from PyQt6.QtGui import QIcon, QAction, QMovie
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QVBoxLayout, QLabel, QWidget, QApplication
from bs4 import BeautifulSoup
from screeninfo import get_monitors
import requests
import os
import sys
# Only windows
import win32.lib.win32con as win32con
import ctypes



# imgFolder = os.getenv("temp")
# imgFolder = imgFolder + "\\Wallpapers\\"

imgList = []
imgFolder = os.getcwd()
imgFolder = imgFolder + "\\imgs\\"
if not os.path.exists(imgFolder):
    os.mkdir(imgFolder)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Add current wallpaper to list
        name = SysFuncs.get_wallpaper(self)
        imgList.append(name)
        self.initUI()


    def initUI(self):
        # Setting a dark theme
        #self.setStyleSheet(qdarktheme.load_stylesheet())



        # TrayIcon
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icons/ico.ico"))
        self.tray.setVisible(True)

        # trayMenu
        self.menu = QMenu(self)
        self.nextImage = QAction("Next image")
        self.prevImage = QAction("Previous image")
        self.quit = QAction("Quit")

        self.nextImage.setIcon(QIcon("icons/arrow_forward.svg"))
        self.prevImage.setIcon(QIcon("icons/arrow_back.svg"))
        self.quit.setIcon(QIcon("icons/close.svg"))

        self.nextImage.triggered.connect(Buttons.next_image)
        self.prevImage.triggered.connect(Buttons.prev_image)
        self.quit.triggered.connect(app.quit)

        self.menu.addAction(self.nextImage)
        self.menu.addAction(self.prevImage)
        self.menu.addAction(self.quit)

        self.tray.setContextMenu(self.menu)

        #Debug window

        # layout = QVBoxLayout()
        # self.label = QLabel()
        # self.movie = QMovie("gif.gif")
        # self.label.setMovie(self.movie)
        # self.movie.start()
        # layout.addWidget(self.label)
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        # self.show()



class Buttons:
    def next_image(self):
        url, name = Parsing.get_image_url(self)
        Parsing.image_download(self, url, name)

        # parse = Parsing(url, name)
        # # QThreadPool takes ownership and deletes 'hello' automatically
        # QThreadPool.globalInstance().start(parse)

        SysFuncs.set_wallpaper(self, imgFolder + name + ".jpg")
        imgList.append(name)


    def prev_image(self):
        if len(imgList) > 1:
            os.remove("imgs/" + imgList[-1] + ".jpg")
            imgList.pop()
            SysFuncs.set_wallpaper(self, imgFolder + imgList[-1] + ".jpg")



class Parsing(QRunnable):
    # Trying to add multi-threading
    # def __init__(self, fn, *args, **kwargs):
    #     super(Parsing, self).__init__()
    #     # Store constructor arguments (re-used for processing)
    #     self.fn = fn
    #     self.args = args
    #     self.kwargs = kwargs
    #
    # @pyqtSlot()
    # def run(self):
    #     '''
    #     Initialise the runner function with passed args, kwargs.
    #     '''
    #     self.fn(*self.args, **self.kwargs)


    def image_download(self, url, name):
        print("downloaded")
        response = requests.get(url)
        file = open(imgFolder + os.path.basename(name) + ".jpg", "wb")
        file.write(response.content)
        file.close()

    def get_image_url(self):
        url = "https://wallhaven.cc/search?q=id:37&sorting=random&ref=fp"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('a', class_="preview")

        for i in quotes:
            url = requests.get(i['href'])
            soup = BeautifulSoup(url.text, 'lxml')
            parsed = soup.find('img', id="wallpaper")

            width, height = SysFuncs.get_resolution(self)
            if int(parsed['data-wallpaper-width']) >= int(width) and int(parsed['data-wallpaper-height']) >= int(
                    height):
                return parsed["src"], parsed["alt"]



class SysFuncs:
    def get_resolution(self):
        for m in get_monitors():
            return m.width, m.height

    def set_wallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    def get_wallpaper(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        name = os.path.basename(ubuf.value)
        name = os.path.splitext(name)[0]
        return name

    def check_net(self):
        try:
            requests.get("http://www.google.com")
            return True
        except requests.ConnectionError:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    sys.exit(app.exec())
