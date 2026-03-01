
import json
import importlib.resources

_module_dir:"pathlib.Path" = importlib.resources.files(__name__)

_language_files = {
  "japanese": _module_dir.joinpath("static/language/japanese.json")
}

BUILTIN:dict[str, str] = {}
for id_, file in _language_files.items():
  with open(file, "r", encoding="utf-8") as stream:
    data = json.load(stream)
  BUILTIN[id_] = data

def translate (id_:str, language:dict[str, str]) -> str:
  return language.get(id_, id_)
