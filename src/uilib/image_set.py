
import importlib.resources
from PIL import Image, ImageTk
from pathlib import Path

def get_image (path:"pathlib.Path|str", expect_size:tuple[int, int]|None=None):
  module_dir = importlib.resources.files(__name__)
  path_candidates = [
    module_dir.joinpath("static", path),
    Path(path)
  ]
  for path_candidate in path_candidates:
    if path_candidate.exists():
      image = Image.open(path_candidate)
      if expect_size:
        image.thumbnail(expect_size)
      return ImageTk.PhotoImage(image=image)
  else:
    raise FileNotFoundError(path_candidates) #tmp.
