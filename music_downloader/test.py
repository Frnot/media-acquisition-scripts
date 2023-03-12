import unittest

import autodownloader
import fix_music_tags
import tidal_downloader


class TestRequestFile(unittest.TestCase):
    def test_fileparser_regex(self):
        tests = [
            ("247590325", "247590325"),
            ("https://tidal.com/browse/track/251721594", "251721594"),
            ("https://listen.tidal.com/album/247590325", "247590325"),
            ("https://listen.tidal.com/album/195068515/track/195068523", "195068515"),
        ]

        for r, m in tests:
            self.assertEqual(autodownloader.parse_line(r), m)



class TestTidalDownloader(unittest.TestCase):
    def test_downloader(self):
        import os
        tests = [
            ("1867681", "1964 - Jazz Impressions Of Japan"),
            ("1867838", "1964 - Jazz Impressions Of Japan"),
            #("195068515", None), #assert doesnt like this
        ]

        for t,r in tests:
            path = tidal_downloader.download(t, None, dry_run=True)
            if r:
                path = os.path.basename(path)
                
            self.assertEqual(path, r)



class TestTagEditing(unittest.TestCase):
    def test_regex(self):
        tests = [
            ("Test Title (2009 Re-Mastered)", "Test Title"),
            ("Test (explicit)", "Test"),
            ("8 - Test Title (feat. Dude #1, Dude #2, & Dude #3) [2005 Remaster].flac", "8 - Test Title (feat. Dude #1, Dude #2, & Dude #3).flac"),
            ("Test (2005 Remaster)", "Test"),
            ("Test (Remastered 2011)", "Test"),
            ("Test (album version) [Explicit]", "Test"),
        ]

        for r, m in tests:
            self.assertEqual(fix_music_tags.clean(r), m)
        


class TestSearch(unittest.TestCase):
    def test_search(self):
        tests = [
            (("Somebody", "Natalie La Rose"), 38949955),
            (("Don't You Worry Child", "Swedish House Mafia"), 17271289),
            (("(When You Gonna) Give It Up To Me", "Sean Paul"), 2147347),
            (("Untitled (How Can This Happen To Me?)", "Simple Plan"), 268069),
            (("La La", "Ashlee Simpson"), 35730192),
            (("All Around The World", "Justin Bieber"), 15905168),
            (("Levels", "Avicii"), 9184436),
        ]

        for search_string, album_id in tests:
            result = tidal_downloader.search(*search_string)
            if result:
                result = result.album.id
            self.assertEqual(result, album_id)


if __name__ == "__main__":
    unittest.main()
