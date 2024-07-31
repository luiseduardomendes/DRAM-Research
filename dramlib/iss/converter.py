import json
from os.path import join
from pathlib import Path

class Converter:

  association_table = {
    'r': 'read',
    'w': 'write'
  }

  def __init__(self, dramsys_path, iss_path, app) -> None:
    self.init_paths(dramsys_path)
    self.init_iss_paths(iss_path, app)

  def init_paths(self, dramsys_path):
    self.dramsys_path = dramsys_path
    self.config_path = join(dramsys_path, "configs")
    self.addrsmap_path = join(self.config_path, "addressmapping")
    self.mcconfig = join(self.config_path, "mcconfig")
    self.memspec_path = join(self.config_path, "memspec")
    self.simconfig_path = join(self.config_path, "simconfig")
    self.traces_path = join(self.config_path, "traces")

  def init_iss_paths(self, iss_path, app):
    self.path_iss = iss_path
    self.path_apps = join(iss_path, "apps")
    self.path_app = join(self.path_apps, app)
    self.path_build_release = join(self.path_app, "build_release")
    self.path_exit = join(self.path_app, "exit")
    self.path_input = join(self.path_app, "input")

  def conv(self, output_file = '../build_release/main_mem.stl', input_file = '../build_release/main_mem.trace'):
    counter = 0
    out = open(output_file, "w")
    with open(input_file) as f:
      for line in f:
        tick_counter, dst_addr, burst_length, read_write = line.split(',')
        read_write = read_write[0]
        new_line = f"{tick_counter}:\t{self.association_table[read_write]} {hex(int(dst_addr))}\n"
        out.write(new_line)
        counter += 1
      f.close()
    out.close()
    return int(burst_length)
  
  def create_new_config_file(self, config_file:str, new_cfg_file:str, trace, burst_length, clkMhz, create_new_files = True):
    if not config_file.endswith(".json"):
      raise Exception(f"file {config_file} is not json file")
    with open(config_file, 'r') as f:
      json_object = json.load(f)
      f.close()

    data = json_object['simulation']
    
    memspec_filename = data['memspec']
    if not memspec_filename.endswith(".json"):
      raise Exception(f"file {memspec_filename} is not json file")
    
    new_memspec_filename = self.update_burst_length(burst_length, memspec_filename, create_new_files)
    data['memspec'] = new_memspec_filename

    data["tracesetup"][0]['clkMhz'] = clkMhz
    data["tracesetup"][0]['name'] = Path(trace).name

    json_object['simulation'] = data

    with open(new_cfg_file, 'w') as f:
      json_object = json.dumps(json_object, indent=4)
      f.write(json_object)
      f.close()

  def update_config_file(self, config_file:str, trace, burst_length, clkMhz, create_new_files = True):
    self.create_new_config_file(
      config_file,
      config_file,
      trace,
      burst_length,
      clkMhz,
      create_new_files
    )

  def append_trace(self, config_file:str, trace, clkMhz):
    if not config_file.endswith(".json"):
      raise Exception(f"file {config_file} is not json file")
    
    with open(config_file, 'r') as f:
      json_object = json.load(f)
      f.close()

    json_object['simulation']['tracesetup'].append(
      {
        'clkMhz':clkMhz,
        'name':Path(trace).name,
      }
    )

    with open(config_file, 'w') as f:
      json.dump(json_object, f, indent=4)
      f.close()

  def update_burst_length(self, burst_length, memspec_filename, new_file = True):
    memspec_filename_abs = join(self.memspec_path, memspec_filename)
    with open(memspec_filename_abs, 'r') as f:
      memspec_obj = json.load(f)
      f.close()
    memspec_obj["memspec"]["memarchitecturespec"]["burstLength"] = burst_length

    if new_file:
      new_memspec_filename = Path(memspec_filename_abs).stem + f"_BL{burst_length}" + '.json'
      fullpath_new_memspec_filename = join(self.memspec_path, new_memspec_filename)
    else:
      new_memspec_filename = memspec_filename
      fullpath_new_memspec_filename = memspec_filename_abs
    
    with open(fullpath_new_memspec_filename, 'w') as f:
      json.dump(memspec_obj, f, indent=4)
      f.close()
    return new_memspec_filename

  def get_path(self, key):
    data = {
      'cfg': self.config_path,
      'adr': self.addrsmap_path,
      'mcc': self.mcconfig,
      'mem': self.memspec_path,
      'sim': self.simconfig_path,
      'trc': self.traces_path,
      'iss': self.path_iss,
      'aps': self.path_apps,
      'app': self.path_app,
      'brl': self.path_build_release,
      'inp': self.path_input,
      'ext': self.path_exit,
    }
    return data[key]
  
  def get_output_log_path(self):
    return join(self.path_build_release, "log.txt")
  
  def get_trace_file_path(self):
    return join(self.path_build_release, "main_mem.trace")
  


