import json
import os
from os import listdir
from os.path import join, isfile, basename, isabs

class Dramsys:
  def __init__(self, dramsys_path: str, prefix: str = ''):
    self.dramsys_path = dramsys_path
    self.prefix       = prefix

    self.__set_up_paths__()


  def __set_up_paths__(self):
    self.build_path         = join(self.dramsys_path, "build"   )
    self.bin_path           = join(self.build_path,   "bin"     )
    self.dramsys_exec_path  = join(self.bin_path,     "DRAMSys" )
    self.cfgs_path          = join(self.dramsys_path, "configs" )
    self.traces_path        = join(self.cfgs_path,    "traces"  )


  #def __create_cfg_and_trace_files__(self, input_path, prefix):
  #  input_files = self.__list_trace_files_with_prefix__(input_path, prefix)
  #
  #  for name, file in input_files:
  #    if not isfile(join(self.traces_path, basename(file))):
  #      os.system(f"mv {file} {self.traces_path}")
  #      self.__create_config_files__(self.cfg_based, basename(file), name)
  #
  #    else:
  #      raise Exception(f"file {file} already exists in {self.traces_path}")


  def __list_cfg_files_with_prefix__(self, path: str, prefix: str):
    files = [
      (f[:-4], join(path, f)) 
      for f in listdir(path) 
      if isfile(join(path, f)) and f.startswith(prefix) and f.endswith('.stl')
    ]
    return files


  def __list_trace_files_with_prefix__(self, path: str, prefix: str):
    files = [
      (f[:-5], join(path, f)) 
      for f in listdir(path) 
      if isfile(join(path, f)) and f.startswith(prefix) and f.endswith('.json')
    ]
    return files


  def __create_config_files__(self, cfg_based: str, stl_file: str, name: str):
    cfg_name = cfg_based[:-5]
    output_filename = f"{cfg_name}-{name}.json"
    output = join(self.traces_path, output_filename)
    
    with open(cfg_based) as f:
      data = json.load(f)
      data["simulation"]["tracesetup"][0]["name"] = stl_file
      data["simulation"]["tracesetup"]["simulationid"] = stl_file
      out = open(output)
      json.dump(data, out)
      out.close()
      f.close()


  def __display_info__(self, name: str):
    print(f"Executing now: {name}")


  def __display_summary__(self):
    print("Execution List:")
    for name, file in self.input_files:
      print(f"file: {name} - {file}")


  # input_path refers to the scalesim files to be converted
  def run_simulation(self, config_dir: str = ''):
    #self.input_path = input_path
    #self.__create_cfg_and_trace_files__(self.input_path, self.prefix)
    self.input_files = self.__list_cfg_files_with_prefix__(config_dir, self.prefix)

    self.__display_summary__()

    for name, file in self.input_files:
      self.__display_info__(name)
      self.run_execution(file)


  def __generate_cmd__(self, cfg_file, output_file):
    return f"{self.dramsys_exec_path} {cfg_file} > {output_file}"


  def run_execution(self, cfg_file, output_file = ''):
    if not isabs(cfg_file):
      relative_cfg_file = join(self.cfgs_path, cfg_file)
    
    if not isfile(cfg_file):
      if not isfile(relative_cfg_file):
        raise Exception(f"Configuration file \"{cfg_file}\" or \"{relative_cfg_file}\"does not exists")
      else:
        cfg_file = relative_cfg_file

    if not cfg_file.endswith(".json"):
      raise Exception(f"configuration file \"{cfg_file}\" must be a \".json\" file")
    
    else:
      file_name = basename(cfg_file)[:-5]
      if output_file == '':
        output_file = file_name + ".txt"
    cmd = self.__generate_cmd__(cfg_file, output_file)
    print(cmd)
    #os.system(cmd)