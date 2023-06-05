from playwright.sync_api import Playwright, BrowserContext


class Browser:
    def __init__(self, profile_dir: str):
        self.profile_dir = profile_dir
        self.extensions = self.get_extensions()


    def get_extensions(self) -> list:
        path_to_adblock = (
            "/home/eren/Downloads/uBlock0.chromium"  # TODO better extension management
        )
        path_to_buster = (
            "/home/eren/Downloads/buster_captcha_solver_for_humans-1.3.2-chrome"
        )

        extensions = [path_to_adblock, path_to_buster]

        return extensions


    def get_browser_instance(
        self, playwright: Playwright, type: str, exec_path: str
    ) -> BrowserContext:
        extensions = self.extensions
        print(exec_path)

        if type == "chromium":
            browser = playwright.chromium.launch_persistent_context(
                self.profile_dir,
                executable_path="/usr/bin/chromium",
                headless=False,
                no_viewport=True,
                args=[
                    f"--disable-extensions-except={extensions[0]},{extensions[1]}",
                    f"--load-extension={extensions[0]},{extensions[1]}",
                    "--start-maximized",
                    "--no-first-run",
                    "--no-service-autorun",
                    "--password-store=basic",
                ],
            )

        else:
            raise Exception("Currently only Chromium is supported.")

        return browser
