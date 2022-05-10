# Greatly inspired from  AmmeySaini / Edu-Mail-Generator repo


import csv
from downloadWebdriver import *


def install(name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


def main():
    my_packages = ['watchdog', 'undetected_chromedriver', 'selenium', 'pyvirtualdisplay', 'clint', 'screeninfo']

    installed_pr = []

    for package in my_packages:
        install(package)
        print('\n')

    print('\nChrome')
    chrome_ver = get_chrome_version()

    if chrome_ver is not None:
        is_chrome_there = 1
        installed_pr.append('Chrome')
        installed_pr.append('chrome_undetected (For easy captcha)')
        setup_Chrome(chrome_ver)
    else:
        is_chrome_there = 0
        print('Chrome isn\'t installed')

    if is_chrome_there == 0:
        print(
            'Error - Setup installation failed \nReason - Please install Chrome browser to complete setup process')
        exit()

    try:
        os.makedirs("../Logs")
        os.chdir("../Logs")

        songNamesFile = open('last_song.txt', 'a')
        songNamesFile.close()

        failedSongs = open('failedSongs.csv', 'w')
        filewriter = csv.writer(failedSongs, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Track Name', 'Artist Name(s)'])
        failedSongs.close()

        pathsFile = open('paths.txt', 'a')

        prefFileLocation = input("Your chrome user profile's path?\n"
                                 "(Linux Default: /home/eren/.config/chromium/Default/Preferences): ")
        pathsFile.write(prefFileLocation + "\n")

        chromiumLocation = input("Your chromium file's location?\n"
                                 "(Linux Default: /usr/bin/chromium): ")
        pathsFile.write(chromiumLocation + "\n")

        downloadLocation = input("The folder your music will be downloaded to?\n"
                                 "(Linux Default: /home/eren/Downloads): ")
        pathsFile.write(downloadLocation + "\n")

        playlistLocation = input("Your spotify playlist CSV location?\n"
                                 "(My Linux Default: /home/eren/Downloads/metal_rock.csv): ")
        pathsFile.write(playlistLocation + "\n")

    except FileExistsError:
        pass


if __name__ == '__main__':
    main()
