# v2.1

# album dirname (expanded edition) ((anything with edition)) (.* version) (reissue)
# in title: (album version) (and remasters (add to comments))
# (explicit) inside album version, run the whole thing multiple times to catch permutations

# deluxe edition. deluxe version


## Directory name:
# save original year, edit album name to match cleaned tags


import os
import re
import unittest
from functools import cache

import music_tag

title_regex = [
    re.compile(r"\s*[({\[].*explicit.*[)}\]]", re.IGNORECASE),  # explicit, explicit version, .*explicit.*
    re.compile(r"\s*[({\[]\s*\d*\s*re[-]*master[ed]*\s*\d*\s*[)}\]]", re.IGNORECASE),  # remastered
    re.compile(r"\s*[({\[]\s*album\s+version\s*[)}\]]", re.IGNORECASE),  # "album version"
    re.compile(r"\s*[({\[].*edition\s*[)}\]]", re.IGNORECASE),  # ".*edition"
    re.compile(r"\s*[({\[].*release\s*[)}\]]", re.IGNORECASE),  # "US Release"
]

album_regex = [
    re.compile(r"\s*[({\[].*explicit.*[)}\]]", re.IGNORECASE),  # explicit, explicit version, .*explicit.*
    re.compile(r"\s*[({\[].*release\s*[)}\]]", re.IGNORECASE),  # "US Release"
]

filename_regex_list = [
    re.compile(r"[\d|\.]+\s+-\s+", re.IGNORECASE),  # N - filename
    re.compile(r"\.[\w|\d]{2,5}$", re.IGNORECASE),  # file extensions
    re.compile(r"\s*[({\[].*[)}\]]$", re.IGNORECASE),  # anything in parenthesis (at the end of the title)
]

def update_dir(dir_path, dry_run=False):
    root, dir = os.path.split(dir_path)
    for file in os.listdir(dir_path):
        filepath = os.path.join(dir_path, file)
        update(filepath, dry_run)

    # Check directory names
    old_dirname = dirname = dir
    if dirname := clean_album(dirname):
        print(f"Old directory name: \"{old_dirname}\" ||| New directory name: \"{dirname}\"")
        if not dry_run:
            new_dirpath = os.path.join(root, dirname)
            os.rename(dir_path, new_dirpath)


def update(filepath, dry_run=False):
    root,file = os.path.split(filepath)
    save_tags = False
    try:
        ftag = music_tag.load_file(filepath)
    except KeyboardInterrupt:
        print("Exiting")
        quit()
    except Exception as e:
        print(f"Error loading file for edit: {e}")
        return None
    
    # Check title
    original_title = title = ftag['title'].value
    if title := clean_title(title):
        ftag['title'] = title
        save_tags = True

    # Check Album tag
    album = ftag['album'].value
    if album := clean_album(album):
        ftag['album'] = album
        save_tags = True

    # Save tags if something has changed
    if save_tags:
        print(f"Old title: \"{original_title}\" ||| New title: \"{title}\"")
        print(filepath)
        if not dry_run:
            ftag.save()
        
    # Check filename
    old_filename = filename = file
    if filename := clean_title(filename):
        print(f"Old filename: \"{old_filename}\" ||| New filename: \"{filename}\"")
        if not dry_run:
            new_filepath = os.path.join(root, filename)
            os.rename(filepath, new_filepath)


def clean_title(string): 
    hits = 0
    for regex in title_regex:
        string, hit = regex.subn("", string)
        hits += hit

    return string.strip() if hits else None


def clean_album(string):
    hits = 0
    for regex in album_regex:
        string, hit = regex.subn("", string)
        hits += hit

    return string.strip() if hits else None

@cache
def scrub_filename(filename):
    for regex in filename_regex_list + album_regex:
        filename, hit = regex.subn("", filename)
    return filename.lower()



class Test(unittest.TestCase):
    def test_title_tagging(self):
        tests = [
            ("Test Title (2009 Re-Mastered)", "Test Title"),
            ("Test (explicit)", "Test"),
            ("8 - Test Title (feat. Dude #1, Dude #2, & Dude #3) [2005 Remaster].flac", "8 - Test Title (feat. Dude #1, Dude #2, & Dude #3).flac"),
            ("Test (2005 Remaster)", "Test"),
            ("Test (Remastered 2011)", "Test"),
            ("Test (album version) [Explicit]", "Test"),
            ("Test Title (US Domestic Release)", "Test Title"),
        ]

        for r, m in tests:
            self.assertEqual(clean(r), m)

    def test_filename(self):
        tests = [
            ("1973 - Body Talk (CTI Records 40th Anniversary Edition)", "1973 - Body Talk")
        ]











if __name__ == "__main__":
    path = r"C:\Users\Frnot\Desktop\QobuzDownloads"
    for dir in os.listdir(path):
        update_dir(os.path.join(path,dir))
    #Test().test_title_tagging()
