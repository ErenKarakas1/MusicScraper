import time
from playwright.sync_api import sync_playwright
from browser.Browser import Browser
from downloader.BaseUtils import BaseUtils


class TestDetection(BaseUtils):
    def init_context(self):
        locations = super().get_locations()

        profile_dir = locations[0]
        exec_path = locations[1]
        type = "chromium"

        self.browser = Browser(profile_dir)
        self.playwright = sync_playwright().start()

        context = self.browser.get_browser_instance(self.playwright, type, exec_path)
        return context

    # TODO take screenshots?
    def test_sannysoft(self):
        context = self.init_context()
        page = context.new_page()

        page.goto("https://bot.sannysoft.com/")
        time.sleep(15)

        self.playwright.stop()
        assert True

    def test_sannysoft_cdp(self):
        context = self.init_context()
        page = context.new_page()

        super().stealth(page)

        page.goto("https://bot.sannysoft.com/")
        time.sleep(15)

        self.playwright.stop()
        assert True

    # def test_cloudflare(self):
    #     context = self.init_context()
    #     page = context.new_page()

    #     page.goto("https://nowsecure.nl/")
    #     time.sleep(15)

    #     self.playwright.stop()
    #     assert True == True

    # def test_cloudflare_cdp(self):
    #     context = self.init_context()
    #     page = context.new_page()

    #     stealth(page)

    #     page.goto("https://nowsecure.nl/")
    #     time.sleep(15)

    #     self.playwright.stop()
    #     assert True == True
