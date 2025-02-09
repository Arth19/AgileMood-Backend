import unittest
import emotions_data_structure


class TestEmotion(unittest.TestCase):
    def test_is_valid_emotion(self):
        valid_emotion = "Happy"
        self.assertTrue(emotions.is_valid_emotion(valid_emotion))

    def test_is_not_valid_emotion(self):
        valid_emotion = "Hungry"
        self.assertFalse(emotions.is_valid_emotion(valid_emotion))
