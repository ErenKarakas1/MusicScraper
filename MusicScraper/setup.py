# Greatly inspired from  AmmeySaini / Edu-Mail-Generator repo


import csv
import subprocess
import sys
import os


def install():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"]
    )


def get_platform_architecture_chrome():
    if sys.platform.startswith("linux") and sys.maxsize > 2**32:
        platform = "linux"
        architecture = "64"
    # TODO lookup if mac works with XQuartz
    # TODO may add Windows
    else:
        raise RuntimeError("Sorry, this program only supports Linux (for now).")
    return platform, architecture


def get_chrome_version():
    platform, _ = get_platform_architecture_chrome()
    if platform == "linux":
        try:
            with subprocess.Popen(
                ["google-chrome", "--version"], stdout=subprocess.PIPE
            ) as proc:
                version = (
                    proc.stdout.read().decode("utf-8").replace("Chromium", "").strip()
                )
                version = version.replace("Google Chrome", "").strip()
        except:
            try:
                with subprocess.Popen(
                    ["chromium", "--version"], stdout=subprocess.PIPE
                ) as proc:
                    version = proc.stdout.read().decode("utf-8").split(" ")[1]
                    return version
            except:
                return None

    # elif platform == "mac":
    #     try:
    #         process = subprocess.Popen(
    #             [
    #                 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    #                 "--version",
    #             ],
    #             stdout=subprocess.PIPE,
    #         )
    #         version = (
    #             process.communicate()[0]
    #             .decode("UTF-8")
    #             .replace("Google Chrome", "")
    #             .strip()
    #         )
    #     except:
    #         return None

    # elif platform == "win":
    #     try:
    #         process = subprocess.Popen(
    #             [
    #                 "reg",
    #                 "query",
    #                 "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon",
    #                 "/v",
    #                 "version",
    #             ],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.DEVNULL,
    #             stdin=subprocess.DEVNULL,
    #         )
    #         version = process.communicate()[0].decode("UTF-8").strip().split()[-1]
    #     except:
    #         return None

    else:
        return

    try:
        version = version.split(" ")[0]
    except:
        pass

    return version


def main():
    install()

    chrome_ver = get_chrome_version()

    if chrome_ver is None:
        print("A Chromium based browser isn't installed")
        print(
            "Error - Setup installation failed.\n"
            + "Reason - Please install a Chromium based browser to complete setup process."
        )
        exit()

    try:
        os.makedirs("../Logs")
        os.chdir("../Logs")

        songNamesFile = open("last_song.txt", "a")
        songNamesFile.close()

        failedSongs = open("failedSongs.csv", "w")
        filewriter = csv.writer(
            failedSongs, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(["Track Name", "Artist Name(s)"])
        failedSongs.close()

        pathsFile = open("paths.txt", "a")

        prefFileLocation = input(
            "Your chrome user profile's path?\n"
            "(Linux Default: /home/USERNAME/.config/chromium/Default/Preferences): "
        )
        pathsFile.write(prefFileLocation + "\n")

        chromiumLocation = input(
            "Your chromium file's location?\n" "(Linux Default: /usr/bin/chromium): "
        )
        pathsFile.write(chromiumLocation + "\n")

        downloadLocation = input(
            "The folder your music will be downloaded to?\n"
            "(Linux Default: /home/USERNAME/Downloads): "
        )
        pathsFile.write(downloadLocation + "\n")

        playlistLocation = input(
            "Your spotify playlist CSV location?\n"
            "(Example: /home/USERNAME/Downloads/PLAYLISTNAME.csv): "
        )
        pathsFile.write(playlistLocation + "\n")

    except FileExistsError:
        print("\nSkipping creating Logs folder as necessary files already exist.")


if __name__ == "__main__":
    main()
