from os import listdir
import os
from pprint import pprint
from os.path import isfile, join

#path = 'configs/'
#files = [(f[:-4], join(path, f)) for f in listdir(path) if isfile(join(path, f)) and f.startswith('scale_Array')]
#network = "topologies/conv_nets/mobilenet.csv"
#output_folder = "output_log_array"

class ScaleSim:
  def simulate(self, path: str, network_path: str, prefix: str = "" , output_folder: str = "output"):
    self.path = path
    self.output_folder = output_folder
    self.network_path = network_path
    self.prefix = prefix

    self.files = self.__list_cfg_files_with_prefix__(path, prefix)

    self.__create_paths__()
    self.__display_info__()
    self.__run_simulation__()

  def __create_paths__(self):  
    if not os.path.isdir(self.output_folder):
      os.mkdir(self.output_folder)

  def __list_cfg_files_with_prefix__(self, path: str, prefix: str):
    files = [
      (f[:-4], join(path, f)) 
      for f in listdir(path) 
      if isfile(join(path, f)) and f.startswith(prefix) and f.endswith('.cfg')
    ]
    return files

  def __create_output_path__(self, name: str, ) -> str:
    output_file = name + ".log"
    output_file = os.path.join(self.output_folder, output_file)
    return output_file
    
  def __create_cmd__(self, file:str, output_file:str) -> str:
    python_main = "./scale.py"
    cmd = "python " + python_main + " -arch_config=" + file + " -network=" + self.network_path + " >> " + output_file
    return cmd

  def __display_info__(self) -> None:
    print("Execution queue: ")
    pprint(self.files)

  def __run_execution__(self, name: str, file: str):
    log = self.__create_output_path__(name)
    cmd = self.__create_cmd__(file, log)
    os.system(cmd)

  def __run_simulation__(self):
    for name, file in self.files:
      print("Running: ", name)
      self.__run_execution__(name, file)
      

