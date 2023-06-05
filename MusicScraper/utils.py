import random
from playwright.sync_api import Page


def delay(page: Page) -> None:
    page.wait_for_timeout(random.randint(1, 3) * 1000)


def stealth(page: Page):
    with open("stealth.min.js", "r") as file:
        js = file.read()

    page.add_init_script(js)


def get_locations():
    with open("../Logs/paths.txt", "r") as file:
        lines = file.read().splitlines()

    return lines
