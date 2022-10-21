# Cross-platform libs
import platform
import threading
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication, QStyle
from bs4 import BeautifulSoup
import requests
import os
import sys

sys.path.append('src/')
import osHooks

imgList = []
imgFolder = os.getcwd()
if platform.system() == "Linux":
    imgFolder = imgFolder + "/imgs/"

elif platform.system() == "Windows":
    imgFolder = imgFolder + "\\imgs\\"
else:
    imgFolder = imgFolder + "/imgs/"

if not os.path.exists(imgFolder):
    os.mkdir(imgFolder)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Add current wallpaper to list
        name = osHooks.get_wallpaper(self)
        print(name)
        imgList.append(name)

        self.initUI()

    def initUI(self):
        # TrayIcon
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icons/ico.ico"))
        self.tray.setVisible(True)

        # trayMenu
        self.menu = QMenu(self)
        self.nextImage = QAction("Next image")
        self.prevImage = QAction("Previous image")
        self.quit = QAction("Quit")

        self.nextImage.setIcon(QIcon(QtGui.QIcon.fromTheme("go-next")))
        self.prevImage.setIcon(QIcon(QtGui.QIcon.fromTheme("go-previous")))
        self.quit.setIcon(QIcon(QtGui.QIcon.fromTheme("window-close")))

        self.nextImage.triggered.connect(Buttons.next_image)
        self.prevImage.triggered.connect(Buttons.prev_image)
        self.quit.triggered.connect(app.quit)

        self.menu.addAction(self.nextImage)
        self.menu.addAction(self.prevImage)
        self.menu.addAction(self.quit)

        self.tray.setContextMenu(self.menu)



class Buttons:
    def next_image(self):
        x = threading.Thread(target=Buttons.next_image_thread, args=(self,))
        x.start()

    def next_image_thread(self):
        url, name = Parsing.get_image_url(self)
        Parsing.image_download(self, url, name)
        osHooks.set_wallpaper(self, name + ".jpg")
        imgList.append(name+".jpg")
        print(imgList)

    def prev_image(self):
        if len(imgList) > 1:
            os.remove(imgList[-1])
            imgList.pop()
            if imgList[-1] != "None":
                osHooks.set_wallpaper(self, imgList[-1])
        print(imgList)

            


class Parsing:
    def image_download(self, url, name):
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

            width, height = osHooks.get_resolution(self)
            if int(parsed['data-wallpaper-width']) >= int(width) and int(parsed['data-wallpaper-height']) >= int(
                    height):
                return parsed["src"], imgFolder + parsed["alt"]

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
