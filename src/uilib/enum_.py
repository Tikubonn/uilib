
from enum import Flag, auto, unique

"""uilib で使用される列挙型が定義されています。"""

@unique
class Direction (Flag):

  """レイアウト時の揃え方向などを表すために使用される列挙型です。
  
  Notes
  -----
  これらは enum.Flag を継承しているため、複数方向を同時指定することが可能です。
  複数方向を指定した場合の動作は、各関数によって規定されます。

  Attributes
  ----------
  N : uilib.enum_.Direction
    東西南北のうち、北を表します。
  S : uilib.enum_.Direction
    東西南北のうち、南を表します。
  W : uilib.enum_.Direction
    東西南北のうち、西を表します。
  E : uilib.enum_.Direction
    東西南北のうち、東を表します。
  """

  N = auto()
  S = auto()
  W = auto()
  E = auto()
