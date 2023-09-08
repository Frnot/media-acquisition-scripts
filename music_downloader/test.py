import unittest

#import autodownloader
#import fix_music_tags
#import tidal_downloader
import qobuz_dl.metadata


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
            ("Test Title (US Domestic Release)", "Test Title"),
        ]

        for r, m in tests:
            self.assertEqual(fix_music_tags.clean(r), m)
        


class TestSearch(unittest.TestCase):
    def test_search(self):
        tests = [
            (("7 Things","Miley Cyrus"), 36771409),
            (("Prisoner","Miley Cyrus"), 163342283),
            (("Decode","Paramore"), 188828408),
            (("Mr. Brightside", "The Killers"), 150850050),
            (("Levels", "Avicii"), 9184436),
            (("My Last","Big Sean"), 10607206),
            (("Swan Song","Dua Lipa"), 102645401),
            (("Somebody", "Natalie La Rose"), 38949955),
            (("Don't You Worry Child", "Swedish House Mafia"), 17271289),
            (("(When You Gonna) Give It Up To Me", "Sean Paul"), 2147347),
            (("Untitled (How Can This Happen To Me?)", "Simple Plan"), 268069),
            (("La La", "Ashlee Simpson"), 35730192),
            (("All Around The World", "Justin Bieber"), 15905168),
        ]

        for search_string, album_id in tests:
            result = tidal_downloader.search(*search_string)
            if result:
                result = result.album.id
            self.assertEqual(result, album_id)
"""

class TestQobuzFeaturedArtistTag(unittest.TestCase):
    def test_tagging(self):
        tests = [
            ("", []),
            ("Zara Larsson, Associated Performer, Composer, Lyricist, Main Artist - Wizkid, Associated Performer, Featured Artist - Zara Larsson feat. WizKid, Associated Performer - Ammar Malik, Composer, Lyricist - Phil Shaouy, Composer, Lyricist, Producer - StarGate, Producer - Brian 'Peoples' Garcia, Producer - Jacob Kasher Hindlin, Composer, Lyricist - Mikkel Eriksen, Composer, Lyricist - Phil Tan, Mixing Engineer - Bill Zimmerman, Engineer - Michelle Mancini, Mastering Engineer - Tor Hermansen, Composer, Lyricist - Ayodeji Ibrahim Balogun, Composer, Lyricist - Brian Garcia, Composer, Lyricist", ["Zara Larsson", "Wizkid"]),
            ("Ramirez, MainArtist - Ivan Ramirez, Composer - Rocci, FeaturedArtist", ["Ramirez", "Rocci"]),
            ("Tijs Verwest, Writer - Tiesto, Producer, Performed by, MainArtist - Gina Tucci, A&R Direction - Tom Norris, Mixer - Lostboy, Producer - Sarah Blanchard, Writer - Pablo Bowman, Writer - Peter Rycroft, Writer - Ava Max, Performed by, MainArtist - Amanda Ava Koci, Writer - Claudia Valentina, Writer", ["Tiësto", "Ava Max"]),
            ('Joe LaPorta, Mastering Engineer - Travis Scott, FeaturedArtist, AssociatedPerformer, Vocal - Leland Wayne, Composer, Lyricist - Jacques Webster, Composer, Lyricist - Offset, MainArtist, AssociatedPerformer, Vocal - Metro Boomin, Producer, Programmer, All Instruments, MainArtist, AssociatedPerformer, Vocal - Kiari Cephus, Composer, Lyricist - Ethan Stevens, Mixing Engineer - 21 Savage, MainArtist, AssociatedPerformer, Vocal - Shayaa Joseph, Composer, Lyricist - 21 Savage, Offset & Metro Boomin feat. Travis Scott, AssociatedPerformer', ["21 Savage", "Offset", "Metro Boomin", "Travis Scott"]),
            ("Train, Associated Performer, Main Artist - Priscilla Renea, Associated Performer, Composer, Featured Artist, Lyricist - Train feat. Priscilla Renea, Associated Performer - Pat Monahan, Composer, Lyricist - Neff U, Producer - Jake Sinclair, Producer - Suzy Shinn, Recording Engineer - Mark Endert, Mixing Engineer - Theron Feemster, Composer, Lyricist - Doug Johnson, Assistant Engineer - Ted Jensen, Mastering Engineer",["Train", "Priscilla Renea"]),
            ("Akil \"O'Neal\" Brown, Coordinator - Leslie Braithwaite, Mixing Engineer - Debra Killings, Background Vocal - C. Harris, Composer - C. Harris, Lyricist - Carlton Lynn, Recording Engineer - Dallas Austin, Composer - Dallas Austin, Lyricist - Dallas Austin, Producer - Jasper Cameron, Composer - Jasper Cameron, Lyricist - Jasper Cameron, Background Vocal - T.I., Rap Performed By - Rick Sheppard, Engineer - Herbie Powers Jr., Mastering Engineer - Toya, Background Vocal - Toya Featuring T.I., Performer", ["Toya", "T.I."]),
            ("The Heavy, Primary - The Dap-Kings Horns, Featuring",["The Heavy", "The Dap-Kings Horns"]),
            ("The Chainsmokers, Associated Performer, Main Artist, Producer - Coldplay, Associated Performer, Main Artist - The Chainsmokers & Coldplay, Associated Performer - Andrew Taggart, Composer, Lyricist - Christopher Martin, Composer, Lyricist - Jordan \"DJ Swivel\" Young, Mixing Engineer, Producer - Emily Lazar, Mastering Engineer - Guy Berryman, Composer, Lyricist - Adam Alpert, Executive Producer - Chris Allgood, Assistant Engineer - Alex Pall, Executive Producer - Jonny Buckland, Composer, Lyricist - Will Champion, Composer, Lyricist",["The Chainsmokers", "Coldplay"]),
            ("Sia, Associated Performer, Main Artist - Kendrick Lamar, Associated Performer, Composer, Featured Artist, Lyricist - Sia feat. Kendrick Lamar, Associated Performer - Sia Furler, Composer, Lyricist - Greg Kurstin, Composer, Engineer, Lyricist, Producer - alex pasco, Engineer - Julian Burg, Engineer - Serban Ghenea, Mixing Engineer - John Hanes, Engineer",["Sia", "Kendrick Lamar"]),
            ("Copyright Control, MusicPublisher - Spock, Producer, MainArtist - Pouya, MainArtist - Songtrust BLVD, MusicPublisher - Kevin Pouya, Composer - Garrett Spach, Composer - Boobie Lootaveli, MainArtist - Habib Suz, Composer",["Pouya", "Spock", "Boobie Lootaveli"]),
            ("Etterlene Jordan, ComposerLyricist - Eldra DeBarge, ComposerLyricist - William DeBarge, ComposerLyricist - Cornell Haynes, Jr., ComposerLyricist - Jason Epperson, Producer, ComposerLyricist - City Spud, Producer, MainArtist, FeaturedArtist - Levell Webb, ComposerLyricist",["Nelly", "City Spud"]),


        ]

        for test_string, expected_result in tests:
            test_dict = {"performers" : test_string}
            artists = [expected_result[0]] if expected_result else []
            qobuz_dl.metadata._get_featured_artists(artists, test_dict)
            self.assertEqual(artists, expected_result)


if __name__ == "__main__":
    try:
        unittest.main()
    except Exception:
        pass
