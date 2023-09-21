import unittest
from src.main.engine.search_engine import format_links

class SearchEngineTest(unittest.TestCase):
    
    def test_link_formatting(self):
        links = [("Season 1", 'https://aniwatch.to/kaguya-sama-love-is-war-123'), ("Season 2", 'https://aniwatch.to/kaguya-sama-love-is-war-season-2-23'), ("Season 3", 'https://aniwatch.to/kaguya-sama-love-is-war-ultra-romantic-17224')]
        expected_result = [("Season 1", 'https://aniwatch.to/watch/kaguya-sama-love-is-war-123'), ("Season 2", 'https://aniwatch.to/watch/kaguya-sama-love-is-war-season-2-23'), ("Season 3", 'https://aniwatch.to/watch/kaguya-sama-love-is-war-ultra-romantic-17224')]
        self.assertEquals(format_links(links), expected_result)
    
if __name__ == "__main__":
    unittest.main()