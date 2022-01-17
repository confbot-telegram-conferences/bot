find app -iname "*.py" | xargs xgettext --from-code utf-8 -o locales/messages.pot

msginit --input=locales/messages.pot --locale=es --output=locales/es/LC_MESSAGES/messages.po

msgfmt -o locales/es/LC_MESSAGES/base.mo locales/es/LC_MESSAGES/base

make make-messages