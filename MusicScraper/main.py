from playwright.sync_api import sync_playwright
from downloader.downloader import Downloader
from utils import get_locations


if __name__ == "__main__":
    with sync_playwright() as playwright:
        locations = get_locations()

        profile_dir = locations[0]
        exec_path = locations[1]
        folder_path = locations[2]
        playlist_path = locations[3]
        type = "chromium"

        downloader = Downloader(
            playwright, profile_dir, exec_path, folder_path, playlist_path, type
        )

        downloader.download_playlist()
