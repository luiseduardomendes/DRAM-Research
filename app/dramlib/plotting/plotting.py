import pandas as pd
from dramlib.file_management import DRAMConfigFile 
import json
from os.path import join

class Plotter:
  variables = [
    'CLUSTERS',
    'UNITS',
    'LAMES',
    'NR_RAMS',
    'LINE_SIZE',
    'ASSOCIATIVITY',
    'RAM_SIZE'
  ]

  def __init__(self, file) -> None:
    self.dcf = DRAMConfigFile()
    self.dcf.update_config(file)

    data = self.dcf.get_analyser_data()

    path          = data['path_to_group_csv']
    self.variable = data['variable']
    self.output   = data['path_to_output_graphs']

    self.df = pd.read_csv(path)

  def plot_all(self):
    self.total_time()
    self.average_bandwidth()
    self.average_bandwidth_idle()
    self.average_power()
    self.total_energy()

  def total_time(self):
    graph_name = 'total_time' + ".jpg"
    self.df.plot(
      self.variable, 'total_time', 
      grid=True,
      title=f'Execution Time per Number of {self.variable}'
    ).get_figure().savefig(join(self.output, graph_name))


  def average_bandwidth(self):
    graph_name = 'avg_bw_Gb' + ".jpg"
    self.df.plot(
      self.variable, 'avg_bw_Gb', 
      grid=True,
      title=f'Average Bandwidth(Gb) per Number of {self.variable}'
    ).get_figure().savefig(join(self.output, graph_name))
    
  def average_bandwidth_idle(self):
    graph_name = 'avg_bw_idle_Gb' + ".jpg"
    self.df.plot(
      self.variable, 'avg_bw_idle_Gb', 
      grid=True,
      title=f'Average Bandwidth(Gb) idle per Number of {self.variable}'
    ).get_figure().savefig(join(self.output, graph_name))

  def average_power(self):
    graph_name = 'average_power' + ".jpg"
    self.df.plot(
      self.variable, 'average_power', 
      grid=True,
      title=f'Average Power(mW) per Number of {self.variable}'
    ).get_figure().savefig(join(self.output, graph_name))

  def total_energy(self):
    graph_name = 'total_energy' + ".jpg"
    self.df.plot(
      self.variable, 'total_energy', 
      grid=True,
      title=f'Total Energy per Number of {self.variable}',
    ).get_figure().savefig(join(self.output, graph_name))

