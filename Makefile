make-messages:
	mkdir -p locales/es/LC_MESSAGES
	find ./app -iname "*.py" | xargs xgettext --from-code utf-8 -o locales/messages.pot
	msgmerge --update locales/es/LC_MESSAGES/messages.po locales/messages.pot
	msgfmt -o locales/es/LC_MESSAGES/messages.mo locales/es/LC_MESSAGES/messages.po