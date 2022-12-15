# Cross-platform libs
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication, QMessageBox
from notifypy import Notify
# Python libs
import sys
from os.path import basename
from configparser import ConfigParser
import threading
# custom libs
sys.path.append('src/')
import osHooks
import downloader


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Add current wallpaper to list
        img_list = []
        name = osHooks.get_wallpaper()
        img_list.append(name)

        # init tray, window and startup dialog
        self.init_tray(img_list)
        #self.init_window()
        self.startup_dialog()

    def init_window(self):
        # Main Window settings 
        self.setWindowIcon(QIcon("icons/ico.ico"))
        self.setWindowTitle("Wallpaper")
        self.resize(1000, 500)

        self.show()

    def init_tray(self, img_list):
        # TrayIcon
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icons/ico.ico"))
        self.tray.setVisible(True)

        # trayMenu
        self.menu = QMenu(self)
        self.next_image_action = QAction("Next image")
        self.prev_image_action = QAction("Previous image")
        #self.browse_images_action = QAction("Browse Images")
        self.quit_action = QAction("Quit")

        # set icons
        self.next_image_action.setIcon(QIcon(QtGui.QIcon.fromTheme("go-next")))
        self.prev_image_action.setIcon(QIcon(QtGui.QIcon.fromTheme("go-previous")))
        #self.browse_images_action.setIcon(QIcon(QtGui.QIcon.fromTheme("format-justify-fill")))
        self.quit_action.setIcon(QIcon(QtGui.QIcon.fromTheme("window-close")))

        # bind buttons to functions
        self.next_image_action.triggered.connect(lambda: Buttons.next_image(self, img_list))
        self.prev_image_action.triggered.connect(lambda: Buttons.prev_image(self, img_list))
        #self.browse_images_action.triggered.connect(lambda: self.show())
        self.quit_action.triggered.connect(QApplication.quit)

        self.menu.addAction(self.next_image_action)
        self.menu.addAction(self.prev_image_action)
        #self.menu.addAction(self.browse_images_action)
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)

    def startup_dialog(self):
        # creating startup dialog if it's needed
        config = ConfigParser()
        config.read('config.ini')
        if config.has_section('settings') and config['settings']['startup_dialog'] == "False":
            pass
        else:
            message = QMessageBox.information(self, "Wallpaper", "The program must be in tray")
            if message.Ok:
                if not config.has_section("settings"):
                    config.add_section("settings")
                config.set("settings", "startup_dialog", "False")
                with open("config.ini", 'w') as configfile:
                    config.write(configfile)


class Buttons:
    current_img = 0
    def next_image(self, img_list):
        if downloader.check_net():
            threading.Thread(target=Buttons.next_image_thread, args=(self, img_list)).start()
        else:
            QMessageBox.critical(self, "Wallpaper", "No internet connection")

    def next_image_thread(self, img_list):
        Buttons.current_img += 1
        try:
            img_list[Buttons.current_img]

        except IndexError:
            url, name = downloader.get_image_url()
            downloader.image_download(url, name)
            img_list.append(name + ".jpg")

        osHooks.set_wallpaper(img_list[Buttons.current_img])
        Notify("Wallpaper", basename(img_list[Buttons.current_img]), default_notification_icon="icons/ico.ico").send()

    def prev_image(self, img_list):
        if len(img_list) > 1 and Buttons.current_img != 0:
            Buttons.current_img -= 1
            osHooks.set_wallpaper(img_list[Buttons.current_img])
            Notify("Wallpaper", basename(img_list[Buttons.current_img]),
                   default_notification_icon="icons/ico.ico").send()


def run():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    UI()
    sys.exit(app.exec())
