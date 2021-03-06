class Word:
    word_class = NotImplemented

    def __init__(self, original, translations, **kwargs):
        self.original = original
        self.translations = translations

    @classmethod
    def factory_from_word_class(cls, word_class, original, translations, **kwargs):
        word_class = cls.clean_word_class(word_class)

        for subclass in cls.__subclasses__():
            if subclass.is_word_class_for(word_class):
                return subclass(original, translations, **kwargs)

        # raise ValueError(f'Word factory got unknown word class: {word_class}')
        return cls(original, translations)

    @classmethod
    def is_word_class_for(cls, word_class):
        return word_class == cls.word_class

    @staticmethod
    def clean_word_class(word_class):
        if not word_class:
            return

        return word_class.rstrip('s').lower()
