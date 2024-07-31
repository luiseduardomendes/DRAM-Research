from os.path import join

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
    return join(self.path_app, f'sim_{self.app}.trace')