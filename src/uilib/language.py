
import json
import importlib.resources
import traceback

BUILTIN:dict[str, dict[str, str]] = {}
DEFAULT:dict[str, str] = {}

def translate (id_:str, language:dict[str, str]|None=None) -> str:

  """指定IDに対応するテキストを取得します。

  Parameters
  ----------
  id_ : str
    取得するテキストのIDです。
  language : dict[str, str]|None
    テキストの検索先となる辞書型です。
    未指定ならば None が設定されます。
    本引数に None が指定された場合 uilib.language.DEFAULT が検索先に設定されます。

  Returns
  -------
  str
    引数 id_ に対応する文字列です。
    対応する文字列が見つからなかった時には、引数 id_ がそのまま返されます。
  """

  if language:
    lang = language
  else:
    lang = DEFAULT 
  return lang.get(id_, id_)

#setup

_module_dir:"pathlib.Path" = importlib.resources.files(__name__)

for file in _module_dir.joinpath("static/language").iterdir():
  with open(file, "r", encoding="utf-8") as stream:
    try:
      BUILTIN[file.stem] = json.load(stream)
    except:
      traceback.print_exc() #取り敢えず処理は継続します

DEFAULT = BUILTIN.get("ja", {})
