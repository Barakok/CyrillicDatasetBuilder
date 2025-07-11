from pymorphy2 import MorphAnalyzer


class WordMorphy:
    def __init__(self):
        self.morph = MorphAnalyzer()

    def get_words_morphy(self, word):
        cases = ["nomn", "gent", "datv", "accs", "ablt", "loct"]
        result = []

        for case in cases:
            inflect = self.morph.parse(word)[0].inflect({case})
            if inflect:
                declined = inflect.word
                result.append(declined)

        if len(result) == 0:
            result.append(word)

        return result
