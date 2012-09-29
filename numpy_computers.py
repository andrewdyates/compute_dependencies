#!/usr/bin/python
from __init__ import Computer
import numpy as np
from scipy.stats import mstats


class PCCComputer(Computer):
  MNAMES = ["PEARSON", "PEARSON_PV"]
  HAS_NEG = True
  def compute(self, x, y):
    assert np.size(x) == np.size(y)
    r, pv = mstats.pearsonr(x,y)
    return {
      'PEARSON': r,
      'PEARSON_PV': pv
      }

class CovComputer(Computer):
  """Use 'sample standard deviation' with 'Bessel's correction'; i.e., norm by N-1"""
  MNAMES = ["COVARIANCE", "STD_PRODUCT", "MIN_STD"]
  HAS_NEG = True
  def compute(self, x, y):
    assert np.size(x) == np.size(y)
    V = np.cov(x,y,bias=1) # divide by n-1
    std_x, std_y = np.sqrt(V[0,0]), np.sqrt(V[1,1])
    return {
      "COVARIANCE": V[0,1],
      "MIN_STD": min(std_x,std_y),
      "STD_PRODUCT": std_x * std_y
      }
    
class SpearmanComputer(Computer):
  MNAMES = ["SPEARMAN", "SPEARMAN_PV"]
  HAS_NEG = True
  def compute(self, x, y):
    assert np.size(x) == np.size(y)
    rho, pv = mstats.spearmanr(x,y)
    return {
      "SPEARMAN": rho,
      "SPEARMAN_PV": pv
      }

class EuclideanComputer(Computer):
  MNAMES = ["EUCLIDEAN"]
  def compute(self,x,y):
    assert np.size(x) == np.size(y)
    q = x-y
    d = np.sqrt((q*q.T).sum())
    return {"EUCLIDEAN": d}

class KendallComputer(Computer):
  MNAMES = ["KENDALL", "KENDALL_PV"]
  def compute(self,x,y):
    assert np.size(x) == np.size(y)
    k, p = mstats.kendalltau(x,y)
    return {
      "KENDALL": k,
      "KENDALL_PV": p
      }

COMPUTERS = {
  "PCCComputer": PCCComputer,
  "CovComputer": CovComputer,
  "SpearmanComputer": SpearmanComputer,
  "EuclideanComputer": EuclideanComputer,
  "KendallComputer": KendallComputer,
  }
