#!/usr/bin/python
from __init__ import Computer
from dcor import *


class DcorComputer(Computer):
  MNAMES = ["DCOR", "DCOV"]

  def compute(self, x, y):
    dc, dr, dvx, dvy = dcov_all(x,y)
    return {
      "DCOR": dr,
      "DCOV": dc
      }
