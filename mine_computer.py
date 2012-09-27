#!/usr/bin/python
# minepy must be installed. See http://mpba.fbk.eu/cmine
import minepy
import numpy as np
from __init__ import Computer

class MINEComputer(Computer):
  MNAMES = ["MIC", "MAS", "MEV", "MCN"]

  def __init__(self, alpha=0.6, c=15):
    assert alpha > 0 and alpha <= 1 and c > 0
    self.mine = minepy.MINE(alpha=alpha, c=c)
    super(MINEComputer, self).__init__()
    
  def compute(self, x, y):
    assert np.size(x) == np.size(y)
    self.mine.score(x, y)
    return {
      "MIC": self.mine.mic(),
      "MAS": self.mine.mas(),
      "MEV": self.mine.mev(),
      "MCN": self.mine.mev()
      }

