#!/usr/bin/python
from __init__ import Computer
import numpy as np
from dcor import *


class DcorComputer(Computer):
  MNAMES = ["DCOR", "DCOV"]

  def compute(self, x, y):
    dc, dr, dvx, dvy = dcov_all(x,y)
    return {
      "DCOR": np.sqrt(dr),
      "DCOV": np.sqrt(dc)
      }

COMPUTERS = {"Dcor": DcorComputer}

