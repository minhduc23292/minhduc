#!/bin/bash -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

# Export .pot file
find . -type f -name '*.py' | xargs xgettext --from-code=UTF-8
mv messages.po i18n/otani_analyzer.pot

# Init .po file for new language
# Put here for future reference
# msginit -i i18n/otani_analyzer.pot -o i18n/vi/LC_MESSAGES/otani_analyzer.po -l vi

# Update .po file
msgmerge -U i18n/vi/LC_MESSAGES/otani_analyzer.po i18n/otani_analyzer.pot
msgmerge -U i18n/ja/LC_MESSAGES/otani_analyzer.po i18n/otani_analyzer.pot

# Generate .mo file
msgfmt i18n/vi/LC_MESSAGES/otani_analyzer.po -o i18n/vi/LC_MESSAGES/otani_analyzer.mo
msgfmt i18n/ja/LC_MESSAGES/otani_analyzer.po -o i18n/ja/LC_MESSAGES/otani_analyzer.mo