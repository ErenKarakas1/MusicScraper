from utils import delay
import urllib.request
import os
import pydub
from speech_recognition import Recognizer, AudioFile
from playwright.sync_api import Page


class CaptchaSolver:
    def __init__(self, page: Page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    def presetup(self) -> bool:
        name = self.page.get_by_title("reCAPTCHA", exact=True).get_attribute("name")
        self.recaptcha = self.page.frame(name=name)

        if self.recaptcha is None:
            print("Could not find recaptcha frame")
            return False

        self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        delay(self.page)

        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if s.get_attribute("aria-checked") != "false":  # solved already
            return False

        name = self.page.get_by_title(
            "recaptcha challenge expires in two minutes", exact=True
        ).get_attribute("name")
        self.main_frame = self.page.frame(name=name)

        if self.main_frame is None:
            print("Could not find main_frame")
            return False

        return True

    def start(self):
        success = self.presetup()
        tries = 0

        if not success:
            print("presetup() returned " + str(success))
            return

        while tries <= 5:
            delay(self.page)
            try:
                self.solve_captcha()
            except Exception as e:
                print(e)
                self.main_frame.locator("id=recaptcha-reload-button").click()
            else:
                s = self.recaptcha.locator("id=recaptcha-anchor")
                if s.get_attribute("aria-checked") != "false":
                    self.page.locator("id=recaptcha-demo-submit").click()
                    delay(self.page)
                    break

            tries += 1

    def solve_captcha(self):
        self.main_frame.get_by_title("Get an audio challenge").click()
        delay(self.page)

        href = self.main_frame.get_by_title(
            "Alternatively, download audio as MP3"
        ).get_attribute("href")

        if href is None:
            print("Could not find download link")
            return

        with urllib.request.urlopen(href) as response, open(
            "audio.mp3", "wb"
        ) as output:
            data = response.read()
            output.write(data)

        sound = pydub.AudioSegment.from_mp3("audio.mp3").export(
            "audio.wav", format="wav"
        )

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")

        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        if type(text) is not str:
            print(text)
            print("Transcription is not string.")
            return

        print(text)
        delay(self.page)

        self.main_frame.fill("id=audio-response", text)
        self.main_frame.click("id=recaptcha-verify-button")

    def __del__(self):
        files = ["audio.mp3", "audio.wav"]

        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                print(file + " does not exist.")
