
from easygoogletranslate import EasyGoogleTranslate


class TranslationHelper():
    def __init__(self):
        self.translate_en_to_iw = EasyGoogleTranslate(
            source_language='en',
            target_language='iw',
            timeout=10
        )

        self.translate_iw_to_en = EasyGoogleTranslate(
            source_language='iw',
            target_language='en',
            timeout=10
        )

    def translate_word(self, word):
        return self.translate_en_to_iw.translate(word)