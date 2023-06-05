from utils import delay
import urllib.request
import os
import pydub
from speech_recognition import Recognizer, AudioFile
from playwright.sync_api import Page
from typing import Literal
from pathlib import Path


class CaptchaSolver:
    def __init__(self, page: Page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None


    status = Literal["FAILED", "COMPLETED", "SOLVED"]

    def presetup(self) -> status:
        locator = self.page.get_by_title("reCAPTCHA", exact=True)
        locator.scroll_into_view_if_needed()
        name = locator.get_attribute("name")
        self.recaptcha = self.page.frame(name=name)

        if self.recaptcha is None:
            print("Could not find recaptcha frame")
            return "FAILED"

        self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        delay(self.page)

        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if s.get_attribute("aria-checked") != "false":  # solved already
            return "SOLVED"

        name = self.page.get_by_title(
            "recaptcha challenge expires in two minutes", exact=True
        ).get_attribute("name")
        self.main_frame = self.page.frame(name=name)

        if self.main_frame is None:
            print("Could not find main_frame")
            return "FAILED"

        return "COMPLETED"


    def start(self):
        status_type = self.presetup()
        tries = 0

        if status_type == "FAILED":
            print("presetup() failed.")
            return False
        elif status_type == "SOLVED":
            print("Captcha solved in presetup().")
            return True

        #TODO improve the logic
        while tries <= 5:
            delay(self.page)
            try:
                self.solve_captcha()
            except Exception as e:
                print("Could not solve captcha. " + e)
                self.main_frame.locator("id=recaptcha-reload-button").click()
            else:
                s = self.recaptcha.locator("id=recaptcha-anchor")
                if s.get_attribute("aria-checked") != "false":
                    self.page.locator("id=recaptcha-demo-submit").click()
                    delay(self.page)
                    break

            tries += 1

        return tries <= 5


    def solve_captcha(self):
        self.main_frame.get_by_title("Get an audio challenge").click()
        delay(self.page)

        href = self.main_frame.get_by_title(
            "Alternatively, download audio as MP3"
        ).get_attribute("href")

        if href is None:
            raise ValueError("Could not find download link.")

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

        print(text) #TODO debug print

        if type(text) is not str:
            raise TypeError("Transcription is not a string.")

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
