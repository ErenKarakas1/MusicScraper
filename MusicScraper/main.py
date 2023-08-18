from playwright.sync_api import sync_playwright
from downloader.Downloader import Downloader
from downloader.BaseUtils import BaseUtils


if __name__ == "__main__":
    with sync_playwright() as playwright:
        locations = BaseUtils().get_locations()

        profile_dir = locations[0]
        exec_path = locations[1]
        folder_path = locations[2]
        playlist_path = locations[3]
        type = "chromium"

        downloader = Downloader(
            playwright, profile_dir, exec_path, folder_path, playlist_path, type
        )

        downloader.download_playlist()
