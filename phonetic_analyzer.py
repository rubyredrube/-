import re
import unicodedata


class RussianPhoneticAnalyzer:
    
    def __init__(self):
        self.vowels = 'аеёиоуыэюя'
        self.consonants = 'бвгджзйклмнпрстфхцчшщ'
        
        self.voiced_pairs = {
            'б': 'п', 'п': 'б', 'в': 'ф', 'ф': 'в',
            'г': 'к', 'к': 'г', 'д': 'т', 'т': 'д',
            'ж': 'ш', 'ш': 'ж', 'з': 'с', 'с': 'з'
        }
        
        self.always_voiced = 'лмнрй'
        self.always_unvoiced = 'хцчщ'
        
        self.voiced = self.always_voiced + 'бвгджз'
        self.unvoiced = self.always_unvoiced + 'пфктшс'
        
        self.always_soft = 'йчщ'
        self.always_hard = 'жшц'
        self.soft_vowels = 'еёиюя'
        self.soft_sign = 'ь'
        self.hard_sign = 'ъ'
        
        self.stress_dictionary = {
            'дом': 0, 'кот': 0, 'сон': 0, 'лес': 0, 'мир': 0, 'день': 0, 'ночь': 0,
            'стол': 0, 'стул': 0, 'хлеб': 0, 'снег': 0, 'дождь': 0, 'ветер': 0,
            'мама': 0, 'папа': 0, 'баба': 0, 'дядя': 0, 'тётя': 0, 'дети': 0,
            'кошка': 0, 'мышка': 0, 'птица': 0, 'рыба': 0, 'книга': 0, 'ручка': 0,
            'школа': 0, 'парта': 0, 'доска': 0, 'окна': 0, 'двери': 0, 'стены': 0,
            'утром': 0, 'летом': 0, 'зимой': 0, 'осень': 0, 'лето': 0, 'слово': 0,
            'вода': 1, 'река': 1, 'гора': 1, 'нога': 1, 'рука': 1, 'спина': 1,
            'окно': 1, 'село': 1, 'число': 1, 'письмо': 1, 'весна': 1, 'зима': 1,
            'собака': 1, 'корова': 1, 'лошадь': 1, 'машина': 1, 'работа': 1,
            'тетрадь': 1, 'учебник': 1, 'портфель': 1, 'линейка': 1, 'резинка': 1,
            'учитель': 1, 'директор': 1, 'доктор': 1, 'повар': 1, 'шофёр': 1,
            'сегодня': 1, 'вчера': 1, 'завтра': 1, 'всегда': 1, 'никогда': 1,
            'язык': 1, 'урок': 1, 'народ': 1, 'город': 1, 'завод': 1,
            'голова': 2, 'человек': 2, 'ребёнок': 2, 'девочка': 1, 'мальчик': 0,
            'карандаш': 2, 'учительница': 2, 'ученица': 2, 'ученик': 2,
            'молоко': 2, 'хорошо': 2, 'плохо': 0, 'быстро': 0, 'медленно': 1,
            'красиво': 1, 'умница': 0, 'солнышко': 0, 'дедушка': 1, 'бабушка': 0,
            'котёнок': 2, 'щенок': 1, 'цыплёнок': 2, 'телёнок': 2,
            'морковка': 1, 'картошка': 1, 'капуста': 1, 'помидор': 2,
            'магазин': 2, 'больница': 2, 'аптека': 1, 'библиотека': 3,
            'телефон': 2, 'компьютер': 2, 'телевизор': 3, 'холодильник': 3,
        }
        
        self.stress_rules = {
            'stressed_suffixes': ['ист', 'изм', 'ант', 'ент', 'ость', 'ение', 'ание'],
            'unstressed_prefixes': ['про', 'пере', 'при', 'под', 'над', 'об', 'от'],
        }
    
    def sanitize_input(self, text):
        if not text:
            return ''
        
        text = unicodedata.normalize('NFKC', text)
        text = ''.join(char for char in text if char.isprintable())
        text = re.sub(r'\s+', ' ', text).strip()
        
        valid_chars = set(self.vowels + self.consonants + self.soft_sign + self.hard_sign + ' -')
        return ''.join(char.lower() for char in text if char.lower() in valid_chars)
    
    def count_syllables(self, word):
        return sum(1 for char in word.lower() if char in self.vowels)
    
    def determine_stress_position(self, word):
        clean_word = word.lower().strip()
        
        if clean_word in self.stress_dictionary:
            return self.stress_dictionary[clean_word]
        
        syllable_count = self.count_syllables(clean_word)
        if syllable_count <= 1:
            return 0
        
        stress_pos = self._apply_stress_rules(clean_word, syllable_count)
        if stress_pos is not None:
            return stress_pos
        
        return None
        
    def _apply_stress_rules(self, word, syllable_count):
        if word.endswith('ость') and syllable_count >= 2:
            return syllable_count - 2
        
        if word.endswith(('ение', 'ание')) and syllable_count >= 2:
            return syllable_count - 2
        
        if word.endswith('ка') and syllable_count >= 2:
            return syllable_count - 2
        
        if syllable_count == 2:
            return 0
        
        if syllable_count >= 3:
            return syllable_count - 2
        
        return None
    
    def get_vowel_positions(self, word):
        return [i for i, char in enumerate(word) if char.lower() in self.vowels]
    
    def is_stressed_vowel(self, position, word, stress_vowel_index=None):
        if word[position].lower() not in self.vowels:
            return False
        
        vowel_positions = self.get_vowel_positions(word)
        if not vowel_positions:
            return False
        
        if stress_vowel_index is not None:
            if 0 <= stress_vowel_index < len(vowel_positions):
                return position == vowel_positions[stress_vowel_index]
        
        auto_stress = self.determine_stress_position(word)
        if auto_stress is not None and 0 <= auto_stress < len(vowel_positions):
            return position == vowel_positions[auto_stress]
        
        return position == vowel_positions[0]
    
    def apply_vowel_reduction(self, vowel, is_stressed):
        if is_stressed:
            return vowel
        
        vowel = vowel.lower()
        if vowel in 'оа':
            return 'а'
        elif vowel in 'ея':
            return 'и'
        
        return vowel
    
    def determine_consonant_voicing(self, consonant, position, word):
        consonant = consonant.lower()
        
        if consonant in self.always_voiced:
            return True
        
        if consonant in self.always_unvoiced:
            return False
        
        if position == len(word) - 1:
            if consonant in self.voiced:
                return False
        
        if position < len(word) - 1:
            next_char = word[position + 1].lower()
            if next_char in self.consonants:
                if consonant in self.voiced and next_char in self.unvoiced:
                    return False
                if (consonant in self.unvoiced and 
                    next_char in self.voiced and 
                    next_char not in self.always_voiced):
                    return True
        
        return consonant in self.voiced
    
    def determine_consonant_softness(self, consonant, position, word):
        consonant = consonant.lower()
        
        if consonant in self.always_soft:
            return True
        
        if consonant in self.always_hard:
            return False
        
        if position < len(word) - 1 and word[position + 1] == self.soft_sign:
            return True
        
        if position < len(word) - 1 and word[position + 1].lower() in self.soft_vowels:
            return True
        
        return False
    
    def get_consonant_transcription(self, consonant, is_voiced, is_soft):
        consonant = consonant.lower()
        
        if consonant in self.voiced_pairs:
            original_voicing = consonant in self.voiced
            if original_voicing != is_voiced:
                consonant = self.voiced_pairs[consonant]
        
        if is_soft and consonant not in self.always_soft:
            consonant += "'"
        
        return consonant
    
    def get_consonant_description(self, consonant, is_voiced, is_soft):
        consonant = consonant.lower()
        properties = ["согл."]
        
        if consonant in self.always_soft:
            properties.append("мяг.")
        elif consonant in self.always_hard:
            properties.append("твёр.")
        else:
            properties.append("мяг." if is_soft else "твёр.")
        
        if consonant in self.always_voiced:
            properties.append("звон.")
            properties.append("сонор.")
        elif consonant in self.always_unvoiced:
            properties.append("глух.")
        else:
            properties.append("звон." if is_voiced else "глух.")
        
        if consonant in self.voiced_pairs or consonant in self.voiced_pairs.values():
            properties.append("пар.")
        else:
            properties.append("непар.")
        
        return ", ".join(properties)
    
    def analyze_character(self, char, position, word, stress_vowel_index=None):
        char_lower = char.lower()
        
        if char_lower in self.vowels:
            is_stressed = self.is_stressed_vowel(position, word, stress_vowel_index)
            transcription = self.apply_vowel_reduction(char_lower, is_stressed)
            
            stress_status = "ударный" if is_stressed else "безударный"
            description = f"глас., {stress_status}"
            
            return f"[{transcription}]", description
        
        elif char_lower in self.consonants:
            is_voiced = self.determine_consonant_voicing(char_lower, position, word)
            is_soft = self.determine_consonant_softness(char_lower, position, word)
            
            transcription = self.get_consonant_transcription(char_lower, is_voiced, is_soft)
            description = self.get_consonant_description(char_lower, is_voiced, is_soft)
            
            return f"[{transcription}]", description
        
        elif char_lower in [self.soft_sign, self.hard_sign]:
            sign_name = "мягкий знак" if char_lower == self.soft_sign else "твёрдый знак"
            return "-", f"{sign_name}, не обозначает звука"
        
        else:
            return char, "неизвестный символ"
    
    def analyze_word(self, word, stress_vowel_index=None):
        clean_word = self.sanitize_input(word)
        
        if not clean_word:
            return {
                'original_word': word,
                'clean_word': '',
                'syllable_count': 0,
                'letter_count': 0,
                'sound_count': 0,
                'stress_position': None,
                'analysis': []
            }
        
        if stress_vowel_index is None:
            stress_vowel_index = self.determine_stress_position(clean_word)
        
        syllable_count = self.count_syllables(clean_word)
        letter_count = len(clean_word)
        
        analysis = []
        for i, char in enumerate(clean_word):
            transcription, description = self.analyze_character(
                char, i, clean_word, stress_vowel_index
            )
            analysis.append({
                'letter': char,
                'transcription': transcription,
                'description': description
            })
        
        sound_count = sum(1 for item in analysis if item['transcription'] != "-")
        
        return {
            'original_word': word,
            'clean_word': clean_word,
            'syllable_count': syllable_count,
            'letter_count': letter_count,
            'sound_count': sound_count,
            'stress_position': stress_vowel_index,
            'analysis': analysis
        }
    
    def format_analysis_output(self, analysis):
        if not analysis['clean_word']:
            return "Ошибка: пустое слово для анализа."
        
        word = analysis['clean_word']
        syllable_count = analysis['syllable_count']
        syllable_word = self._get_syllable_word_form(syllable_count)
        
        result = [f"\n{word} – {syllable_count} {syllable_word}"]
        
        if analysis['stress_position'] is not None:
            stress_info = f"Ударение на {analysis['stress_position'] + 1}-м слоге"
            result.append(stress_info)
        
        result.append("")
        
        for item in analysis['analysis']:
            letter = item['letter']
            transcription = item['transcription']
            description = item['description']
            
            if transcription != "-":
                result.append(f"{letter} {transcription} – {description}")
            else:
                result.append(f"{letter} – {description}")
        
        letter_count = analysis['letter_count']
        sound_count = analysis['sound_count']
        letter_word = self._get_letter_word_form(letter_count)
        sound_word = self._get_sound_word_form(sound_count)
        
        result.append("")
        result.append(f"{letter_count} {letter_word}, {sound_count} {sound_word}")
        
        return "\n".join(result)
    
    def _get_syllable_word_form(self, count):
        if count % 10 == 1 and count % 100 != 11:
            return "слог"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "слога"
        else:
            return "слогов"
    
    def _get_letter_word_form(self, count):
        if count % 10 == 1 and count % 100 != 11:
            return "буква"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "буквы"
        else:
            return "букв"
    
    def _get_sound_word_form(self, count):
        if count % 10 == 1 and count % 100 != 11:
            return "звук"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "звука"
        else:
            return "звуков"


def main():
    analyzer = RussianPhoneticAnalyzer()
    
    print("=" * 50)
    print("ФОНЕТИЧЕСКИЙ АНАЛИЗАТОР РУССКОГО ЯЗЫКА")
    print("=" * 50)
    print("Введите слово для анализа или 'выход' для завершения работы.")
    
    while True:
        print("\n" + "-" * 30)
        user_input = input("Введите слово: ").strip()
        
        if user_input.lower() in ['выход', 'exit', 'quit', 'q', '']:
            print("До свидания!")
            break
        
        analysis = analyzer.analyze_word(user_input)
        
        if (analysis['syllable_count'] > 1 and 
            analysis['stress_position'] is None):
            
            print(f"Не удалось определить ударение автоматически.")
            print(f"Укажите номер ударного слога (1-{analysis['syllable_count']}) "
                  f"или нажмите Enter для ударения на первом слоге:")
            
            try:
                stress_input = input().strip()
                if stress_input:
                    stress_num = int(stress_input)
                    if 1 <= stress_num <= analysis['syllable_count']:
                        analysis = analyzer.analyze_word(user_input, stress_num - 1)
                    else:
                        print(f"Некорректный номер слога. Используется первый слог.")
                        analysis = analyzer.analyze_word(user_input, 0)
                else:
                    analysis = analyzer.analyze_word(user_input, 0)
            except ValueError:
                print("Некорректный ввод. Используется первый слог.")
                analysis = analyzer.analyze_word(user_input, 0)
        
        output = analyzer.format_analysis_output(analysis)
        print(output)


if __name__ == "__main__":
    main()