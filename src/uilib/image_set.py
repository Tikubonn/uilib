
import importlib.resources
from PIL import Image, ImageTk

_uilib_dir:"pathlib.Path" = importlib.resources.files("uilib")
_PIL_IMAGES:"dict[str, PIL.Image]" = {
  "icon-add": Image.open(_uilib_dir.joinpath("static/image/icon/add.png")),
  "icon-delete": Image.open(_uilib_dir.joinpath("static/image/icon/delete.png")),
  "icon-edit": Image.open(_uilib_dir.joinpath("static/image/icon/edit.png")),
  "icon-move-up": Image.open(_uilib_dir.joinpath("static/image/icon/move-up.png")),
  "icon-move-down": Image.open(_uilib_dir.joinpath("static/image/icon/move-down.png")),
  "icon-search": Image.open(_uilib_dir.joinpath("static/image/icon/search.png")),
}

def get_image (id_:str, expect_size:tuple[int, int]) -> "tkinter.PhotoImage":
  image = _PIL_IMAGES[id_]
  image.copy()
  image.thumbnail(expect_size)
  return ImageTk.PhotoImage(image=image)
