#v1.0

# TODO: add setup.py or something that will install from git with pip

import os
import re
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from watchdog.observers.polling import PollingObserver

from fix_music_tags import update_dir
from tidal_downloader import download

# Files that have been modified and should be checked
files_to_check = set()

def main():

    # TODO: make this an argument
    watch_directory = "/mnt/media/audio/Music"

    observer = PollingObserver()
    event_handler = Handler()

    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    try:
        print(f"Watching for changes in {watch_directory}")
        while True:
            process_files(files_to_check)
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()



class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        # Give user time to add IDs to getfile
        time.sleep(5)
        filepath = event.src_path
        if event.is_directory or os.path.basename(filepath) != "get.txt":
            return 
        if filepath in files_to_check:
            return
            
        # Check if file still exists (large delay on event trigger)
        if os.path.exists(filepath):
            print(f"Watchdog received 'modified' event: {filepath}")
            files_to_check.add(filepath)



def process_files(files):
    for file in files:
        newfile = ""
        with open(file, "r") as f:
            for line in f.readlines():
                if not (line := line.strip()):
                    continue
                if id := parse_line(line):
                    download_target = os.path.dirname(file)
                    stat = download(id, download_target)
                    if not stat:
                        newfile += f"Error: could not download '{line}'\n"
                    else:
                        update_dir(stat)
                else:
                    newfile += f"Error: could not interpret '{line}'\n"
        
        if newfile:
            fout = open(file, "w")
            fout.write(newfile)
            fout.close()
        else:
            os.remove(file)

    # clear filename set
    files.clear()
    


def parse_line(line):
    # TODO: make regex more robust
    tidal_regex = re.compile(r"\s*(\d+)\s*", re.IGNORECASE)
    regex_match = re.search(tidal_regex, line)
    if regex_match:
        return regex_match.group(1)
    else:
        return None


if __name__ == "__main__":
    main()
