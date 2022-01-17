import gettext
import emoji

lang_translations = gettext.translation(
    "messages", localedir="locales", languages=["es"]
)
lang_translations.install()


def trans(*args, **kwargs):
    return emoji.emojize(lang_translations.gettext(*args, **kwargs), use_aliases=True)


prural = lang_translations.ngettext
