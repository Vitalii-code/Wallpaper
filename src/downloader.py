from os.path import basename
from bs4 import BeautifulSoup
import requests
import osHooks
from os import getcwd, path, mkdir
from platform import system
import socket

imgFolder = getcwd()
if system() == "Linux":
    imgFolder = imgFolder + "/imgs/"

elif system() == "Windows":
    imgFolder = imgFolder + "\\imgs\\"
else:
    imgFolder = imgFolder + "/imgs/"

if not path.exists(imgFolder):
    mkdir(imgFolder)


def image_download(url, name):
    response = requests.get(url)
    file = open(imgFolder + basename(name) + ".jpg", "wb")
    file.write(response.content)
    file.close()


def get_image_url(width=osHooks.get_resolution.width(), height=osHooks.get_resolution.height()):
    url = "https://wallhaven.cc/search?q=id:37&sorting=random&ref=fp"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_="preview")

    for i in quotes:
        url = requests.get(i['href'])
        soup = BeautifulSoup(url.text, 'lxml')
        parsed = soup.find('img', id="wallpaper")

        if int(parsed['data-wallpaper-width']) >= int(width) and int(parsed['data-wallpaper-height']) >= int(
                height):
            return parsed["src"], imgFolder + parsed["alt"]


def check_net():
    try:
        host = socket.gethostbyname("1.1.1.1")
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass
    return False

