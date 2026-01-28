
from enum import Flag, auto, unique

@unique
class Direction (Flag):

  N = auto()
  S = auto()
  W = auto()
  E = auto()
