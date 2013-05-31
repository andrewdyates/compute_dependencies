# these extra, custom modules should be imported on demand, not by default

# Create a COMPUTERS singleton class instance that is backwards compadiable with the 
#   old dictionary based version
class COMPUTERCLS(object):
  # I don't have a great way to maintain this list automatically.
  # Just add new names to the list as they are created.
  # Map to module name
  KNOWN_COMPUTERS = {
    "Dcor": 'dcor_computer',
    "PCC": 'numpy_computers',
    "Cov": 'numpy_computers',
    "Spearman": 'numpy_computers',
    "Euclidean": 'numpy_computers',
    "Kendall": 'numpy_computers',
    "MINE": 'mine_computer',
    "HHG": 'hhg_computer',
  }
  def keys(self):
    return set(self.KNOWN_COMPUTERS.keys())
  def __getitem__(self, arg):
    # Get computer class from module, but only import on request
    assert arg in self.KNOWN_COMPUTERS
    mod = self.KNOWN_COMPUTERS[arg]
    exec "import %s" % mod
    exec "r = %s.COMPUTERS['%s']" % (mod, arg)
    return r
  
COMPUTERS = COMPUTERCLS()

# OLD WAY
# -----------------------------
# import dcor_computer
# import hhg_computer
# import mine_computer
# import numpy_computers

# COMPUTERS = {}
# COMPUTERS.update(dcor_computer.COMPUTERS)
# COMPUTERS.update(hhg_computer.COMPUTERS)
# COMPUTERS.update(mine_computer.COMPUTERS)
# COMPUTERS.update(numpy_computers.COMPUTERS)
