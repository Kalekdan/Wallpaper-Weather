import threading, ctypes
import weatherTimeUtils

def updateWallpaper(): # TODO Add linux/OSX support
    t = threading.Timer(2300.0, updateWallpaper)
    #t.daemon = True
    t.start()
    wallpaperPath = weatherTimeUtils.weatherTime.getWallpaper()
    print(wallpaperPath)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaperPath, 0)

updateWallpaper()