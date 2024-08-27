from os.path import join
import subprocess

class CNNConv:
  def __init__(self, path, app):
    self.set_paths(path)
    self.set_app_paths(app)
    pass

  def set_paths(self, path):
    self.path_cnn_conv    = path
    self.path_nets        = join(path, "nets")
    self.path_netgen      = join(path, "netgen")

  def set_app_paths(self, app):
    self.app = app
    self.path_app         = join(self.path_nets, app)

  def get_trace_file_path(self):
    return join(self.path_app, "sim_results", 'main_mem.trace')

  def get_log_file_path(self):
    return join(self.path_app, f'sim_{self.app}.log')
  
  def run(
      self, 
      clusters = -1,
      units		= -1,
      lanes		= -1,
      nr_rams		= -1,
      line_size	= -1,
      associativity	= -1,
      ram_size = -1,
      directives = '',
      debug=False
  ):
    cmd = f'cd {self.path_cnn_conv} && make sim_{self.app}'
    if clusters != -1:
      cmd += f' CLUSTERS={clusters}'
    if units != -1:
      cmd += f' UNITS={units}'
    if lanes != -1:
      cmd += f' LANES={lanes}'
    if nr_rams != -1:
      cmd += f' NR_RAMS={nr_rams}'
    if line_size != -1:
      cmd += f' LINE_SIZE={line_size}'
    if associativity != -1:
      cmd += f' ASSOCIATIVITY={associativity}'
    if ram_size != -1:
      cmd += f' RAM_SIZE={ram_size}'
    cmd += directives

    if not debug:
      subprocess.call(cmd, shell=True)
    else:
      print(cmd)