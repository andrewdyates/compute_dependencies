#!/usr/bin/python
from __init__ import Computer
# R and Rpy2 must be installed.
from rpy2 import robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
import numpy as np


class HHGComputer(Computer):
  MNAMES = ["SUM_CHI", "SUM_LR", "MAX_CHI", "MAX_LR"]

  def __init__(self):
    # Load HHG library from R installation.
    r('library("HHG2x2")')
    super(HHGComputer, self).__init__()

  def compute(self, x, y):
    """Return normalized HHG scores."""
    assert np.size(x) == np.size(y)
    n = np.size(x)
    robjects.globalenv["x"] = x
    robjects.globalenv["y"] = y
    r('Dx = as.matrix(dist((x),diag=TRUE,upper=TRUE))')
    r('Dy = as.matrix(dist((y),diag=TRUE,upper=TRUE))')
    HHG = r('myHHG(Dx,Dy)')
    v = n*(n-2)*(n-3) # max sum_chi value
    lg = np.log(2)
    return {
      "SUM_CHI": float(HHG.rx('sum_chisquared')[0][0]) / v,
      "SUM_LR": float(HHG.rx('sum_lr')[0][0]) / v / lg / (2/np.e),
      "MAX_CHI": float(HHG.rx('max_chisquared')[0][0]) / (n-2),
      "MAX_LR": float(HHG.rx('max_lr')[0][0]) / (n-2) / lg
      }

COMPUTERS = {"HHG": HHGComputer}
