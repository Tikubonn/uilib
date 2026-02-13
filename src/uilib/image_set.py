
import importlib.resources
from PIL import Image, ImageTk

"""uilib で使用される画像データの管理を行うモジュールです。"""

_uilib_dir:"pathlib.Path" = importlib.resources.files("uilib")
_PIL_IMAGES:"dict[str, PIL.Image]" = {
  "icon-add": Image.open(_uilib_dir.joinpath("static/image/icon/add.png")),
  "icon-delete": Image.open(_uilib_dir.joinpath("static/image/icon/delete.png")),
  "icon-edit": Image.open(_uilib_dir.joinpath("static/image/icon/edit.png")),
  "icon-move-up": Image.open(_uilib_dir.joinpath("static/image/icon/move-up.png")),
  "icon-move-down": Image.open(_uilib_dir.joinpath("static/image/icon/move-down.png")),
  "icon-search": Image.open(_uilib_dir.joinpath("static/image/icon/search.png")),
}

def get_image (id_:str, expect_size:tuple[int, int]|None=None) -> "tkinter.PhotoImage":

  """指定された画像を tkinter.PhotoImage 形式で取得します。

  Parameters
  ----------
  id_ : str
    取得する画像の ID 名です。
  expect_size : tuple[int, int]
    取得する画像の望ましいサイズです。
    画像サイズが本サイズを超過する場合には自動的にリサイズを行います。

  Returns
  -------
  tkinter.PhotoImage
    適切にリサイズされた tkinter.PhotoImage 形式の画像オブジェクトです。
  """

  image = _PIL_IMAGES[id_]
  copied_image = image.copy()
  if expect_size:
    image.thumbnail(expect_size)
  return ImageTk.PhotoImage(image=copied_image)
