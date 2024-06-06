import re
from os.path import isfile
import pandas as pd
from pathlib import Path
from pprint import pprint

class Parser:
  pattern  = re.compile(
    r"DRAMSys\.dram0  Total Energy:\s+(\d+\.\d+) (\w+)\n" +\
    r"DRAMSys\.dram0  Average Power:\s+(\d+\.\d+) (\w+)\n" +\
    r"DRAMSys\.controller0  Total Time:\s+(\d+) (\w+)\n" +\
    r"DRAMSys\.controller0  AVG BW:\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) \%\n" +\
    r"DRAMSys\.controller0  AVG BW\\IDLE:\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) \%\n" +\
    r"DRAMSys\.controller0  MAX BW:\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) (\w+)\/s\s+\|\s+(\d+\.\d+) \%\n" +\
    r"Simulation took (\d+\.\d+) seconds\."
  )
  groups = [
    "total_energy",     "unit_total_energy",
    "average_power",    "unit_average_power",
    "total_time",       "unit_total_time",
    "avg_bw_Gb",        "unit_avg_bw_Gb",        "avg_bw_GB",       "unit_avg_bw_GB",         "avg_bw_p",
    "avg_bw_idle_Gb",   "unit_avg_bw_idle_Gb",   "avg_bw_idle_GB",  "unit_avg_bw_idle_GB",    "avg_bw_idle_p",
    "max_bw_Gb",        "unit_max_bw_Gb",        "max_bw_GB",       "unit_max_bw_GB",         "max_bw_p",
    "simulation_time" 
  ]
  groups_no_power = [
    "total_time",       "unit_total_time",
    "avg_bw_Gb",        "unit_avg_bw_Gb",        "avg_bw_GB",       "unit_avg_bw_GB",         "avg_bw_p",
    "avg_bw_idle_Gb",   "unit_avg_bw_idle_Gb",   "avg_bw_idle_GB",  "unit_avg_bw_idle_GB",    "avg_bw_idle_p",
    "max_bw_Gb",        "unit_max_bw_Gb",        "max_bw_GB",       "unit_max_bw_GB",         "max_bw_p",
    "simulation_time" 
  ]
  units = {
    # timing values to miliseconds
    'ps': 10**(-9), 'ns': 10**(-6), 'us': 10**(-3), 'ms': 10**( 0),
    # bandwidth values to miliseconds
    'GB': 10**( 0), 'MB': 10**(-3), 'kB': 10**(-6),  'B': 10**(-9),
    'Gb': 10**( 0), 'Mb': 10**(-3), 'kb': 10**(-6),  'b': 10**(-9),
    # energy values to milijoules
    'pJ': 10**(-9), 'nJ': 10**(-6), 'uJ': 10**(-3), 'mJ': 10**( 0),
    # power values to miliwatts
    'pW': 10**(-9), 'nW': 10**(-6), 'uW': 10**(-3), 'mW': 10**( 0),
  }

  def __init__(self) -> None:
    pass

  def parse_file(self, file) -> dict:
    if not isfile(file):
      raise Exception(f"Parsing error: file not found: \"{file}\"")
    
    df = {}
    with open(file) as f:
      content = f.read()
      check = self.pattern.findall(content, re.M)
      if len(check) == 1:
        data = check[0]
        if len(data) == len(self.groups):
          df = {self.groups[i]: [data[i]] for i in range(len(data))}
        elif len(data) == len(self.groups_no_power):
          df = {self.groups_no_power[i]: [data[i]] for i in range(len(data))}
        else:
          raise Exception(f"Incorrect file format: {file}")
      else:
        raise Exception(f"Incorrect file format: {file}")
    pprint(df)
    
    df = self.convert_units(df)
    out_name = "parsed_"+Path(file).stem+".csv"
    self.to_csv(df, out_name)
    return df
  
  def convert_units(self, df_in):
    df_out = {}
    for label in self.groups:
      if label.startswith("unit"):
        value_label = label[5:]
        unit_label = label
        factor = self.units[df_in[unit_label][0]]
        df_out[value_label] = [float(df_in[value_label][0]) * factor]
    df_out["simulation_time"] = [float(df_in["simulation_time"][0]) * 10**(3)]
    df_out = pd.DataFrame(df_out)
    return df_out

  def to_csv(self, df_in, export_name):      
    df_in.to_csv(export_name)


#parser = Parser()
#file = "ddr4-example-ranktest.txt"
#df = parser.parse_file(file)

