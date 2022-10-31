import gui
import sys
import downloader

helpStr = """
    Usage: wallpaper.sh [option] number
    
    Example:
    wallpaper.sh - without arguments starting gui
    wallpaper.sh -r 1024x800 5
    wallpaper.sh 2
    
    Number is amount of images that you need
    
    [option]
    -r , --resolution = set the resolution of image(default is resolution of your main monitor)
    -h , --help = display this help and exit
"""

if __name__ == '__main__':
    
    args = sys.argv
    
    if len(args) == 1:  # if no arguments then run gui
        print("[Wallpaper] The program must be in tray")   
        gui.run()
        
    else:
        for i, arg in enumerate(args):
            if arg == "--help" or arg == "-h":  # if args have help then show help and break
                print(helpStr)
                exit()
            elif arg == "--resolution" or arg == "-r":
                resolution  = args[i+1].split("x")  # saving resolution
                width=resolution[0]
                height=resolution[1]
                for i in range(0, int(args[-1])):
                    url, name = downloader.get_image_url(width, height)
                    downloader.image_download(url, name)
                    print(name)
                break
            else:
                for i in range(0, int(args[-1])):
                    url, name = downloader.get_image_url()
                    downloader.image_download(url, name)
                    print(name)
                break
                
        

        
