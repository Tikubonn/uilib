
from abc import ABC, abstractmethod

class ILoadable (ABC):

  """任意のパラメータから状態を復元する機能を規定します。"""

  @abstractmethod
  def load_from_param (self, param:"typing.Any"):

    """任意のパラメータを基にオブジェクトの状態を復元します。

    Parameters
    ----------
    param : typing.Any
      復元に用いられるパラメータです。
    """

    pass

class IUI (ILoadable):

  """UI の作成・管理を行う機能を規定します。
  
  規定される機能の一覧は次のとおりです。
  
  * tkinter ウィジットの作成
  * UI 設定値の管理
  * uilib.ui.abc.ILoadable に規定された方法による UI の状態復元
  """

  @abstractmethod
  def get_value (self) -> "typing.Any":

    """UI 設定値を取得します。

    Returns
    -------
    typing.Any
      取得した UI 設定値です。
    """

    """
    """

    pass

  @abstractmethod
  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    
    """tkinter ウィジットを作成します。

    Parameters
    ----------
    master : tkinter.Widget
      作成される tkinter ウィジットの親となる tkinter.Widget もしくは tkinter.Tk インスタンスです。

    Returns
    -------
    tkinter.Widget
      作成された tkinter ウィジットです。
    """
