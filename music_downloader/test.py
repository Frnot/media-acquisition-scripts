import unittest

import autodownloader
import fix_music_tags
import tidal_downloader


class TestTotalIntegration(unittest.TestCase):
    # This isn't exactly a 'unit' test
    """def test_fileprocessor(self):
        with open("testfile1.txt", "w") as f:
            f.write("https://listen.tidal.com/album/247590325")
        with open("testfile2.txt", "w") as f:
            f.write("https://tidal.com/browse/track/92932818")

        autodownloader.process_files(["testfile1.txt", "testfile2.txt"])
    """



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
            ("195068515", None),
        ]

        for t,r in tests:
            path = tidal_downloader.download(t, dry_run=True)
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
        


if __name__ == "__main__":
    unittest.main()
