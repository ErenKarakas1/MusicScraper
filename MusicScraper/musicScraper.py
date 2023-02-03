# SOON DEPRECATED FOR MAIN.PY


import os
import watchdog
import csv
import time
import undetected_chromedriver as uc
from pyvirtualdisplay import Display
from screeninfo import get_monitors
from selenium.common.exceptions import (
    NoSuchElementException,
    UnexpectedAlertPresentException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, observer):
        self.observer = observer
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, patterns=["*.flac"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        """
        Notifies the program about download starting.
        Logs the successfully downloaded song's artist and name.
        @param event: Watchdog event
        """
        print("Download started - % s." % event.src_path)

        global fileReceived
        fileReceived = True

        lastSongFile = open(cwd + "last_song.txt", "w")
        words = event.src_path.split("/")
        lastSongFile.write(words[4][0:-5])
        lastSongFile.close()

        self.observer.stop()
        # Event is created, you can process it now

    def on_modified(self, event):
        print("Download finished - % s." % event.src_path)
        # Event is modified, you can process it now


def createBrowserInstance():
    """
    Creates a Firefox instance for the Selenium bot.
    Imports the user's Firefox profile.
    @return: Browser instance
    """

    options = uc.ChromeOptions()

    prefFile = lines[0]
    chromiumLocation = lines[1]

    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--password-store=basic")
    options.add_argument("user-data-dir:" + os.path.normpath(prefFile))
    options.add_argument("--start-maximized")
    options.binary_location = os.path.normpath(chromiumLocation)

    browser = uc.Chrome(
        options=options,
        driver_executable_path=os.path.normpath(
            (os.getcwd() + "/webdriver/chromedriver")
        ),
        browser_executable_path=os.path.normpath(
            chromiumLocation,
        ),
    )

    browser.implicitly_wait(10)

    return browser


def downloadParamSong(songName, artistName, browser):
    """
    Downloads the song that was passed as the parameter.
    @param songName: Song name
    @param artistName: Artist(s) name
    @param browser: Browser instance
    """

    downloadsFolder = lines[2]
    src_path = os.path.normpath(downloadsFolder)
    observer = watchdog.observers.Observer()
    event_handler = Handler(observer)
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()

    global fileReceived
    global fileFailed
    fileReceived = False
    fileFailed = False

    browser.get("https://free-mp3-download.net/")

    musicSearchbar = browser.find_element(By.XPATH, '//*[@id="q"]')
    time.sleep(1)

    browser.save_screenshot("photo.png")
    vpnButton = browser.find_element(
        By.XPATH, "/html/body/main/div/div[1]/form/div[3]/label"
    )
    vpnButton.click()

    time.sleep(1)
    musicSearchbar.send_keys(songName.split(" - ")[0])
    musicSearchbar.submit()

    time.sleep(3)
    download = browser.find_element(
        By.XPATH, "/html/body/main/div/div[2]/div/table/tbody/tr[1]/td[3]/a/button"
    )
    download.click()

    time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)
    flacButton = browser.find_element(
        By.XPATH, "/html/body/main/div/div/div/div/div[3]/div[1]/div[2]/p/label"
    )
    flacButton.click()

    try:
        time.sleep(3)
        frame = browser.find_element(
            By.XPATH, "/html/body/main/div/div/div/div/div[3]/div[2]/div/div/div/iframe"
        )
        browser.switch_to.frame(frame)

        time.sleep(2)
        captchaBox = browser.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"
        )
        captchaBox.click()

        browser.switch_to.default_content()
        time.sleep(2)

        try:
            captchaFrame = browser.find_element(
                By.XPATH, "/html/body/div[3]/div[4]/iframe"
            )
            browser.switch_to.frame(captchaFrame)

            time.sleep(1)
            browser.find_element(
                By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]"
            ).click()

            browser.switch_to.default_content()
            time.sleep(10)

        except NoSuchElementException:
            time.sleep(3)

    except NoSuchElementException:
        time.sleep(1.5)

    errorNum = 0
    for p in range(2):
        try:
            downloadButton = browser.find_element(
                By.XPATH, "/html/body/main/div/div/div/div/div[3]/button"
            )
            downloadButton.click()

        except NoSuchElementException:
            errorNum += 1

        except UnexpectedAlertPresentException:
            errorNum += 1

        except ElementClickInterceptedException:
            errorNum += 1

    if errorNum == 3:
        downloadError(artistName, songName)

    try:
        while not fileReceived:
            if fileFailed:
                observer.stop()
                break

            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def downloadError(artistName, songName):
    print("Download failed - Saving the song name...")

    failedSongFile = open(cwd + "failedSongs.csv", "a")
    filewriter = csv.writer(failedSongFile, dialect="excel")
    filewriter.writerow([songName, artistName])
    failedSongFile.close()

    global fileFailed
    fileFailed = True


def downloadThePlaylist(browser):
    """
    Downloads the given playlist.
    Remembers the last downloaded song and skips if the download was unsuccessful.
    @param browser: Browser instance
    """
    global fileReceived
    lastSongPassed = False

    lastSongFile = open(cwd + "last_song.txt")
    songName = lastSongFile.readline()
    lastSongFile.close()

    if songName != "":
        group = songName.split(" - ")
        song = group[1].split(" (")

    songsCSV = lines[3]
    exportedPlaylist = open(os.path.normpath(songsCSV))
    nameReader = csv.DictReader(exportedPlaylist)

    for row in nameReader:
        name = row["Track Name"].split(" - ")[0]
        if lastSongPassed or songName == "":
            downloadParamSong(name, row["Artist Name(s)"], browser)

        elif group[0] != row["Artist Name(s)"] and song[0].upper() in name.upper():
            lastSongPassed = True
            print("Artist name mismatch in the song " + name)

        elif group[0] == row["Artist Name(s)"] and song[0].upper() in name.upper():
            lastSongPassed = True

    exportedPlaylist.close()


if __name__ == "__main__":
    # Notifies the program whether the download was received or not
    fileReceived = False
    fileFailed = False

    path = os.getcwd()
    cwd = os.path.dirname(path) + "/Logs/"

    paths = []
    pathsFile = open(cwd + "paths.txt", "r")
    lines = pathsFile.readlines()

    for i in range(4):
        lines[i] = lines[i].rstrip("\n")

    pathsFile.close()

    width, height = get_monitors()[0].width, get_monitors()[0].height
    display = Display(visible=False, size=(width, height))
    display.start()

    browserInstance = createBrowserInstance()

    try:
        downloadThePlaylist(browserInstance)
    except:
        display.stop()

    display.stop()
