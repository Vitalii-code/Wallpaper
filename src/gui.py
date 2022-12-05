# Cross-platform libs
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication, QMessageBox
from notifypy import Notify
# Python libs
import os
import sys
from os.path import basename
from configparser import ConfigParser
import threading
# custom libs
sys.path.append('src/')
import osHooks
import downloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        imgList = []
        # Add current wallpaper to list
        name = osHooks.get_wallpaper()
        imgList.append(name)
        self.initUI(imgList)

    def initUI(self, imgList):
        self.setWindowIcon(QIcon("icons/ico.ico"))
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

        self.nextImage.triggered.connect(
            lambda: threading.Thread(target=Buttons.next_image, args=(self, imgList)).start())
        self.prevImage.triggered.connect(lambda: Buttons.prev_image(self, imgList))
        self.quit.triggered.connect(QApplication.quit)

        self.menu.addAction(self.nextImage)
        self.menu.addAction(self.prevImage)
        self.menu.addAction(self.quit)

        self.tray.setContextMenu(self.menu)

        # creating start dialog
        config = ConfigParser()
        config.read('config.ini')
        if config.has_section('settings') and config['settings']['startup_dialog'] == "False":
            pass
        else:
            message = QMessageBox.information(self, "Wallpaper", "The program must be in tray")
            if message.Ok:
                self.tray.showMessage("Wallpaper", "I'm here!", QIcon("icons/ico.ico"), 5000)
                if not config.has_section("settings"):
                    config.add_section("settings")
                config.set("settings", "startup_dialog", "False")
                with open("config.ini", 'w') as configfile:
                    config.write(configfile)


class Buttons:
    def next_image(self, imgList):
        if downloader.check_net():
            url, name = downloader.get_image_url()
            downloader.image_download(url, name)
            osHooks.set_wallpaper(name + ".jpg")
            imgList.append(name + ".jpg")
            Notify("Wallpaper", basename(name), default_notification_icon="icons/ico.ico").send()
        else:
            QMessageBox.critical(self, "Wallpaper", "No internet connection")

    def prev_image(self, imgList):
        if len(imgList) > 1:
            os.remove(imgList[-1])
            imgList.pop()
            if imgList[-1] != "None":
                osHooks.set_wallpaper(imgList[-1])
                Notify("Wallpaper", basename(imgList[-1]),
                       default_notification_icon="icons/ico.ico").send()


def run():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    sys.exit(app.exec())
