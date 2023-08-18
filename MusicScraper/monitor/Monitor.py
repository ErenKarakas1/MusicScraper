import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path


class PatternObserver:
    def get_observer(self, folder_path):
        src_path = os.path.normpath(folder_path)

        observer = Observer()
        event_handler = Handler(observer)

        observer.schedule(event_handler, path=src_path, recursive=True)
        return observer


class Handler(PatternMatchingEventHandler):
    def __init__(self, observer):
        self.observer = observer
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(
            self, patterns=["*.flac"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        """
        Notifies the program about download starting.
        Logs the successfully downloaded song's artist and name.
        @param event: Watchdog event
        """
        print("Download started - % s." % event.src_path)

        current_dir = Path()
        relative_path = "../Logs/last_song.txt"
        last_song = (current_dir / relative_path).resolve()

        with open(last_song, "w") as file:
            words = event.src_path.split("/")
            file.write(words[4][0:-5])

        self.observer.stop()
        # Event is created, you can process it now

    def on_modified(self, event):
        print("Download finished - % s." % event.src_path)
        # Event is modified, you can process it now
