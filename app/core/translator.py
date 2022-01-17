import emoji
from app.transalation import trans, prural


class Translator:
    """
    TODO: In the future the user will save the language.
    """

    def __init__(self):
        self.trans = trans
        self.prural = prural

    def _(self, text):
        return self._prepare_text(self.trans(text))

    def _prepare_text(self, text):
        return emoji.emojize(text, use_aliases=True)

    def __call__(self, text):
        return self.trans(text)

    def ngettext(self, singular, plural, num):
        return self.prural(singular, plural, num)
