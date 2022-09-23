#v2.1

# TODO: add setup.py or something that will install from git with pip

import os
import re
import subprocess

from fix_music_tags import update_dir
from tidal_downloader import download

ignore = set()

def main():
    # TODO: make this an argument
    ssh_string = "acq@fileserver.lab.frnot.com"
    local_path = "/mnt/media/audio/Music"
    remote_path = "/vault/media/audio/Music"

    dif = os.path.commonpath([local_path[::-1], remote_path[::-1]])[::-1]
    path_translation = remote_path.replace(dif, ""), local_path.replace(dif, "")

    check(local_path)

    watch_changes(remote_path, path_translation, ssh_string)


def check(local_dir):
    for root,d_names,f_names in os.walk(local_dir, topdown=False):
        for file in f_names:
            if file != "get.txt":
                continue

            filepath = os.path.join(root, file)
            process_file(filepath)


def watch_changes(watch_dir, path_translation, ssh_string):
    cmd = f"ssh {ssh_string} 'inotifywait -mr -e close_write --format '%w%f' {watch_dir}'"
    process = subprocess.Popen(cmd, text=True, shell=True, stdout=subprocess.PIPE)
    try:
        while path := process.stdout.readline().rstrip():
            # Translate filepath from remote to local
            filepath = path.replace(*path_translation)

            # Check conditions
            if os.path.basename(filepath) != "get.txt":
                continue

            # Check if file still exists (potentiall large delay while requests are beign processed)
            if not os.path.exists(filepath):
                continue
            
            # Prevent runaway loop
            if filepath in ignore:
                ignore.remove(filepath)
                continue
            
            print(f"Processing file '{filepath}'")
            process_file(filepath)
    finally:
        # end inotifywait
        pass


def process_file(file):
    try:
        if os.path.getsize(file) == 0:
            print("empty file!")
            return
    except (OSError, TypeError):
        return
    
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
        with open(file, "w") as f:
            f.write(newfile)
        ignore.add(file)
    else:
        os.remove(file)

    

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
