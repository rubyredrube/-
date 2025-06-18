import unittest
from phonetic_analyzer import RussianPhoneticAnalyzer


class TestRussianPhoneticAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = RussianPhoneticAnalyzer()
    
    def test_basic_word_analysis(self):
        result = self.analyzer.analyze_word("кот")
        
        self.assertEqual(result['syllable_count'], 1)
        self.assertEqual(result['letter_count'], 3)
        self.assertEqual(result['sound_count'], 3)
        
        self.assertEqual(len(result['analysis']), 3)
        
        o_analysis = result['analysis'][1]
        self.assertEqual(o_analysis['letter'], 'о')
        self.assertEqual(o_analysis['transcription'], '[о]')
    
    def test_vowel_reduction(self):
        result = self.analyzer.analyze_word("молоко")
        
        first_o = result['analysis'][1]
        last_o = result['analysis'][5]
        
        self.assertEqual(first_o['transcription'], '[а]')
        
        self.assertEqual(last_o['transcription'], '[о]')
        
    def test_syllable_counting(self):
        """Test syllable counting works correctly"""
        self.assertEqual(self.analyzer.count_syllables("кот"), 1) 
        self.assertEqual(self.analyzer.count_syllables("мама"), 2) 
        self.assertEqual(self.analyzer.count_syllables("собака"), 3)
        self.assertEqual(self.analyzer.count_syllables(""), 0)      
    
    def test_empty_input(self):
        result = self.analyzer.analyze_word("")
        
        self.assertEqual(result['clean_word'], "")
        self.assertEqual(result['syllable_count'], 0)
        self.assertEqual(result['analysis'], [])


if __name__ == "__main__":
    unittest.main()