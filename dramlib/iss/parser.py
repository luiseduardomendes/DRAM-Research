import re
from os.path import isfile, join
import pandas as pd
from pathlib import Path
from pprint import pprint

class Parser:
  pattern_frequency = re.compile(r'^Frequency AXI:\s+(\d+) MHz$')
  pattern_clusters  = re.compile(r'^\s+Clusters:\s+(\d+)$')
  pattern_units     = re.compile(r'^\s+Units per Cluster:\s+(\d+)$')
  pattern_lanes     = re.compile(r'^\s+Proc. Lanes per Unit:\s+(\d+)$')

  def __init__(self) -> None:
    self.df = pd.DataFrame()
    pass

  def parse_file(self, file, output_dir = '', to_csv=True) -> tuple:
    if not isfile(file):
      raise Exception(f"Parsing error: file not found: \"{file}\"")
    
    df = {
      'frequency': [],
      'clusters': [],
      'units': [],
      'lanes': []
    }
    with open(file) as f:
      for line in f:
        check = self.pattern_frequency.findall(line)
        if len(check) > 0:
          frequency = check[0]
          check = self.pattern_clusters.findall(line)
        elif len(check) > 0:
          clusters = check[0]
          check = self.pattern_units.findall(line)
        elif len(check) > 0:
          units = check[0]
          check = self.pattern_lanes.findall(line)
        elif len(check) > 0:
          lanes = check[0]
      f.close()
    df['frequency'].append(int(frequency))
    df['clusters'].append(int(clusters))
    df['units'].append(int(units))
    df['lanes'].append(int(lanes))
    df = pd.DataFrame(df)

    self.df = df
    if to_csv:
      out_name = join(output_dir, "parsed_"+Path(file).stem+".csv")
      self. df.to_csv(out_name)

    return (frequency, clusters, units, lanes)



