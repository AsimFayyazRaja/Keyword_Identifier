import unittest
import identify_keywords

def get_sentence_keywords():
    "returns keywords and sentence to test"

    given_keywords=["AI Algorithms", "Crazy Website", "MEAN website", "AI Hype", "AI", "My Crazy Website", "AI Module",
"New York", "Egg York", "Italian:Pizza", "French-Pizza", "Super_AI","The Dark Knight", "The Dark Knight Rises"]

    sentence="I want an Italian Pizza"

    return given_keywords,sentence    


class TestIdentifyKeywords(unittest.TestCase):

    def test_keywords(self):

        keys,sent=get_sentence_keywords()

        result=identify_keywords.identify_keywords(keys,sent)
        expected=["Italian:Pizza"]
        expected=set(expected)
        self.assertEqual(result,expected)