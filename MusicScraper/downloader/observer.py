import watchdog.events
import watchdog.observers
import os


class Observer:
    def get_observer(self, folder_path):
        src_path = os.path.normpath(folder_path)
        observer = watchdog.observers.Observer()

        event_handler = Handler(observer)

        observer.schedule(event_handler, path=src_path, recursive=True)
        return observer


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, observer):
        self.observer = observer
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, patterns=["*.flac"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        """
        Notifies the program about download starting.
        Logs the successfully downloaded song's artist and name.
        @param event: Watchdog event
        """
        print("Download started - % s." % event.src_path)

        with open("last_song.txt", "w") as file:
            words = event.src_path.split("/")
            file.write(words[4][0:-5])

        self.observer.stop()
        # Event is created, you can process it now

    def on_modified(self, event):
        print("Download finished - % s." % event.src_path)
        # Event is modified, you can process it now
