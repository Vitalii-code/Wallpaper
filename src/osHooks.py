import os
import subprocess
from screeninfo import get_monitors
import platform

if platform.system() == "Linux":
    pass

elif platform.system() == "Windows":
    import win32.lib.win32con as win32con
    import ctypes
else:
    pass


def get_resolution():
    for m in get_monitors():
        return m.width, m.height


def set_wallpaper(path):
    if platform.system() == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    elif platform.system() == "Linux":
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            os.system(f'gsettings set org.gnome.desktop.background picture-uri "{path}"')
            os.system(f'gsettings set org.gnome.desktop.background picture-uri-dark "{path}"')

        elif os.environ.get('KDE_FULL_SESSION') == 'true':
            command = """dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string: var Desktops = desktops();for (i=0;i<Desktops.length;i++) { d = Desktops[i]; d.wallpaperPlugin = "org.kde.image"; d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General"); d.writeConfig("Image", "%s");}'"""
            os.system(command % path)


        elif os.environ.get('DESKTOP_SESSION') == "xfce":
            os.system(f'xfconf-query -c xfce4-desktop -p  /backdrop/screen0/monitor0/workspace0/last-image -s "{path}"')


def get_wallpaper():
    if platform.system() == "Windows":
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        name = ubuf.value
        name = os.path.splitext(name)[0]
        name = name + ".jpg"
        return name

    elif platform.system() == "Linux":
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            name = subprocess.check_output(["gsettings get org.gnome.desktop.background picture-uri"], shell=True)
            return decode_string_from_terminal(name)


        elif os.environ.get('KDE_FULL_SESSION') == 'true':
            name = subprocess.check_output(["""kreadconfig5 --file "$HOME/.config/plasma-org.kde.plasma.desktop
                                               -appletsrc" --group 'Containments' --group '1' --group 'Wallpaper' 
                                               --group 'org.kde.image' --group 'General' --key 'Image'"""],
                                           shell=True)
            return decode_string_from_terminal(name)

        # xfce - "xfconf-query -c xfce4-desktop -p insert_property_here -s path/image"
        # macos - "osascript -e ‘tell application “Finder” to set desktop image to POSIX file “~ / Desktop / cabo-san-lucas.jpg”‘"


def decode_string_from_terminal(name):
    try:
        name = name.decode(encoding='UTF-8')
        name = name.replace("%20", " ")
        name = name.replace("'", "")
        name = name.rstrip('\n')
        name = name.split('file://')[1]
    except:
        pass
    return name
