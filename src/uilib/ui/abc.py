
from abc import ABC, abstractmethod

class ILoadable (ABC):

  @abstractmethod
  def load_from_param (self, param:"typing.Any"):
    pass

class IUI (ILoadable):

  @abstractmethod
  def get_value (self) -> "typing.Any":
    pass

  @abstractmethod
  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    pass
