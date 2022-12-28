import gettext
import os
import json
from pathlib import Path
_current_directory = os.path.dirname(os.path.realpath(__file__))
_parent_directory = os.path.dirname(_current_directory)
json_filename = _parent_directory + '/i18n/language.json'
json_pathname = Path(json_filename)
# TODO: Read user-chosen language from config then set it here
with open(json_pathname, 'r', encoding='utf-8') as f:
    languageDict = json.load(f)
currentLanguage=languageDict["Language"]
if currentLanguage =="ENGLISH":
    os.environ['LANGUAGE'] = 'en'
elif currentLanguage=="JAPANESE":
    os.environ['LANGUAGE'] = 'ja'
else:
    os.environ['LANGUAGE'] = 'vi'
locale_dir = os.path.dirname(__file__) + '/'
gettext.bindtextdomain('otani_analyzer', locale_dir)
gettext.textdomain('otani_analyzer')

_ = gettext.gettext