import os
from screeninfo import get_monitors
import platform


if platform.system == "Linux":
    pass

elif platform.system == "Windows":
    import win32.lib.win32con as win32con
    import ctypes
else:
    pass


def get_resolution(self):
    for m in get_monitors():
        return m.width, m.height

def set_wallpaper(self, path):
    if platform.system() == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    elif platform.system() == "Linux":
        if os.environ.get('DESKTOP_SESSION') == "gnome":
            os.system(f'/usr/bin/gsettings set org.gnome.desktop.background picture-uri "{path}"')

        elif os.environ.get('DESKTOP_SESSION') == "plasma":
            string = """dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string: var Desktops = desktops();for (i=0;i<Desktops.length;i++) { d = Desktops[i]; d.wallpaperPlugin = "org.kde.image"; d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General"); d.writeConfig("Image", "file:///%s");}'"""
            os.system(string % path)



def get_wallpaper(self):
    if platform.system() == "Windows":
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        name = os.path.basename(ubuf.value)
        name = os.path.splitext(name)[0]
        return name
    elif platform.system() == "Linux":
        if os.environ.get('DESKTOP_SESSION') == "gnome":
            pass
        elif os.environ.get('DESKTOP_SESSION') == "plasma":
            pass