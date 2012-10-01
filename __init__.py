#!/usr/bin/python
"""Compute measures of dependency between two vectors."""
import os.path
import numpy as np
import errno
import time

# File name pattern used to save matrices.
RX_SAVE_PTN = re.compile("(?P<batchname>.+?)\.(?P<mname>[^.])+\.npy")

def intersect(x, y):
  """Return x, y such that no dimension has a missing value.

  Returns:
    (x,y) np.array tuple with no missing values or mismatched dimensions
  """
  if hasattr(x, 'mask'):
    x_mask = x.mask
  else:
    x_mask = np.zeros(x.shape, dtype=np.bool)
  if hasattr(y, 'mask'):
    y_mask = y.mask
  else:
    y_mask = np.zeros(y.shape, dtype=np.bool)
  join_select = (~x_mask & ~y_mask)
  if hasattr(x, 'mask'):
    r_x = x[join_select].data
  else:
    r_x = x[join_select]
  if hasattr(y, 'mask'):
    r_y = y[join_select].data
  else:
    r_y = y[join_select]    
  return (r_x, r_y)


class Computer(object):
  """BASE CLASS: Compute measures of dependency between two vectors."""
  MNAMES = []  # List of dependency measures computed per `compute`.
  HAS_NEG = False
  def compute(self, x, y):
    """Return dependency measure between x and y.
    OVERRIDE PER IMPLEMENTATION.
    
    Args:
      x: np.array of row vector
      y: np.array of row vector
    Returns:
      dict {str:num} such that each key in MNAMES has a value.
    """
    assert x and y # twart pychecker warnings
    return {}

class BatchComputer(object):
  """Compute, cache, and save a batch of dependency measures.

  Attributes:
    size: int of number of results cached
    computer: instance of Computer subclass
    Matrices: {name=>np.array} of length `size` of computed results per
      dependency measures in MNAMES
    MNAMES: [str] of dependency measures computed per vector pair in Computer
  """
  
  def __init__(self, computer=None, size=1):
    """Initialize results matrices, specify dependency computer.

    Args:
      computer: obj `Computer`, computes a collection of dependency measures.
      size: int results cache size
    """
    assert size is not None and size > 0
    assert computer is not None
    self.computed_set = set()
    
    self.computer = computer
    # Each of MNAMES will generate an individual results matrix.
    self.MNAMES = computer.MNAMES
    self.size = size
    # Create empty dependency matrices
    self.Matrices = {}
    for n in self.MNAMES:
      self.Matrices[n] = np.empty(size).fill(np.nan)

  @property
  def n_computed(self):
    return len(self.computed_set)

  def compute(self, x, y, i):
    """Compute and cache measure of dependencies using `compute`.

    Args:
      x, y: np.array of row vector
      i: int of computation ID in this batch
    """
    assert np.shape(x)[-1] == np.shape(y)[-1]
    assert len(np.shape(x)) <= 2 and len(np.shape(y)) <= 2
    assert i >= 0 and i < self.size
    results = self.computer.compute(x, y)
    assert set(results.keys()) == set(self.MNAMES)
    for key in self.MNAMES:
      self.Matrices[key][i] = results[key]
    self.computed_set.add(i)
    return results
  
  def get(self, i):
    """Return dict of dependency values computed for index i."""
    assert i >= 0 and i < self.size
    return dict([(k, self.Matrices[k][i]) for k in self.MNAMES])
  
  def nans(self):
    """Return total number of not-a-numbers in all results matrices."""
    return sum([np.sum(np.isnan(M)) for M in self.Matrices.values()])
  
  def save(self, outdir, batchname):
    """Save each of many result matrices to file.

    Args:
      outdir: str of path where files will be saved.
      batchname: str of filename tag;
        forms filename as: "%s.%s.npy" % (batchname, dep_name)
    Returns:
      {str:str} of dependency_name => filepath written
    """
    out_names = {}
    for name, M in self.Matrices.items():
      output_fname = os.path.join(target_dir, "%s.%s.npy" % (batchname, name))
      assert RX_SAVE_PTN.match(os.path.basename(output_fname))
      np.save(output_fname, M)
      out_names[name] = output_fname
    return out_names
