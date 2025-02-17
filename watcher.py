import sys
import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, script):
        self.script = script
        self.process = None

    def run(self):
        event_handler = Handler(self)
        observer = Observer()
        observer.schedule(event_handler, ".", recursive=True)
        observer.start()
        self.start_script()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def start_script(self):
        if self.process:
            self.process.terminate()
        self.clear_terminal()
        print("Recompilando e reiniciando o script...")
        self.process = subprocess.Popen([sys.executable, self.script])

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class Handler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            self.watcher.start_script()

if __name__ == "__main__":
    script = "main.py"
    watcher = Watcher(script)
    watcher.run()