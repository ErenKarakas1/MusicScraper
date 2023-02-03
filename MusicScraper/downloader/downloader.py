import re
import os
import csv
from utils import delay
from browser.browser import Browser
from playwright.sync_api import Playwright
from captcha_solver.captcha_solver import CaptchaSolver
from downloader.observer import Observer
from pathlib import Path


class Downloader:
    def __init__(
        self,
        playwright: Playwright,
        profile_dir: str,
        exec_path: str,
        folder_path: str,
        playlist_path: str,
        type: str,
    ):
        self.browser = Browser(profile_dir)
        self.context = self.browser.get_browser_instance(playwright, type, exec_path)
        self.csv_path = playlist_path
        self.folder_path = folder_path

    def download_playlist(self):
        lastSongPassed = False

        current_dir = Path(__file__).resolve()

        with open("../../Logs/last_song.txt", "r") as file:
            last_song = file.readline()

        if last_song != "":
            artist, song = last_song.split(" - ")
            song = song.split(" (")[0]

        with open(os.path.normpath(self.csv_path)) as exported_playlist:
            csv_reader = csv.DictReader(exported_playlist)

            for row in csv_reader:
                song_name = row["Track Name"].split(" - ")[0]
                if lastSongPassed or last_song == "":
                    self.download_song(song_name)

                elif (
                    artist != row["Artist Name(s)"]
                    and song.upper() in song_name.upper()
                ):
                    lastSongPassed = True
                    print("Artist name mismatch in the song " + song_name)

                elif (
                    artist == row["Artist Name(s)"]
                    and song.upper() in song_name.upper()
                ):
                    lastSongPassed = True

    def download_song(self, song_name: str):
        observer = Observer().get_observer(self.folder_path)
        observer.start()

        page = self.context.new_page()

        page.goto("https://free-mp3-download.net/")
        delay(page)

        page.get_by_label("Search using our VPN").click(force=True)
        delay(page)

        page.get_by_label("Search here...").type(song_name)
        delay(page)

        page.get_by_role("button", name=re.compile("search", re.IGNORECASE)).click()
        delay(page)

        page.get_by_role("button", name=re.compile("download", re.IGNORECASE)).nth(
            0
        ).click()
        delay(page)

        # TODO
        # locator = page.locator('label:has-text("FLAC")')
        # if expect(locator).to_be_enabled():

        # page.locator('label:has-text("FLAC")').click()
        # delay(page)

        try:
            captcha_solver = CaptchaSolver(page)
            captcha_solver.start()

            del captcha_solver

        except Exception as err:
            print(err)

        with page.expect_download(timeout=0) as download_info:
            page.get_by_role(
                "button", name=re.compile("download", re.IGNORECASE)
            ).click()

        download = download_info.value
        download.save_as(self.folder_path + song_name + ".flac")

        try:
            while observer.is_alive():
                # TODO
                if False:
                    observer.stop()
                    break

                observer.join(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()
