from os.path import join
from os import makedirs
import json
from pprint import pprint

class DRAMConfigFile:
  def __init__(self):
    self.init_values()

  def start(self, input_file, path_file):
    self.read_input(input_file)
    self.read_path_file(path_file)
  
  DEFAULT_CLUSTER_VALUE = 8
  DEFAULT_UNITS_VALUE = 8
  DEFAULT_LANES_VALUE = 2
  DEFAULT_CLKMHZ_VALUE = 200
  DEFAULT_NRAMS_VALUE = 8
  DEFAULT_LINESIZE_VALUE = 4096
  DEFAULT_ASSOCIATIVITY_VALUE = 4
  DEFAULT_RAMSIZE_VALUE = 524288
  DEFAULT_BURST_LENGTH = 8
  
  def init_values(self):
    self.data = {}
    self.data['configs'] = {}
    self.data['params'] = {}
    self.data['paths'] = {}
    self.data['addpath'] = {}

    self.data['params']['prefix'] =     None
    self.data['params']['platform'] =   None
    self.data['params']['app'] =        None
    self.data['params']['dsys_cfg'] =   None
    self.data['params']['variable'] =   None
    self.data['params']['values'] =     None
    self.data['params']['value'] =     None

    self.data['configs']['cluster'] =       self.DEFAULT_CLUSTER_VALUE
    self.data['configs']['units'] =         self.DEFAULT_UNITS_VALUE
    self.data['configs']['lanes'] =         self.DEFAULT_LANES_VALUE
    self.data['configs']['clkMhz'] =        self.DEFAULT_CLKMHZ_VALUE
    self.data['configs']['n_rams'] =        self.DEFAULT_NRAMS_VALUE 
    self.data['configs']['line_size'] =     self.DEFAULT_LINESIZE_VALUE
    self.data['configs']['associativity'] = self.DEFAULT_ASSOCIATIVITY_VALUE
    self.data['configs']['ram_size'] =      self.DEFAULT_RAMSIZE_VALUE
    self.data['configs']['burst_length'] =  self.DEFAULT_BURST_LENGTH  

    self.data['paths']['path_to_log_file'] =            None
    self.data['paths']['path_to_original_trace_file'] = None
    self.data['paths']['path_to_dramsys_config_file'] = None
    self.data['paths']['path_to_created_config_file'] = None
    self.data['paths']['path_to_created_trace_file'] =  None
    self.data['paths']['path_to_output_dramsys'] =      None
    self.data['paths']['path_to_output_parsed'] =       None
    self.data['paths']['path_to_output_graphs'] =       None
    self.data['paths']['path_to_config_file'] =         None
    self.data['paths']['dramsys']         =             None
    self.data['paths']['zuse_avf_ki']     =             None
    self.data['paths']['output_data']     =             None

    self.data['addpath']['relative_folder'] =           None
    self.data['addpath']['filename_no_ext'] =           None

  def read_path_file(self, filename):
    with open(filename, 'r') as f:
      json_obj = json.load(f)
      f.close()

    self.data['paths']['dramsys']         = json_obj["paths"].get("dramsys",    None)
    self.data['paths']['zuse_avf_ki']     = json_obj["paths"].get("zuse_avf_ki",  None)
    self.data['paths']['output_data']     = json_obj["paths"].get("output_data",  None)

  def read_input(self, file:str):
    with open(file, 'r') as f:
      json_obj = json.load(f)
      f.close()

    self.data['params']['prefix']       = json_obj["params"].get("prefix",    None)
    self.data['params']['platform']     = json_obj["params"].get("platform",  None)
    self.data['params']['app']          = json_obj["params"].get("app",       None)
    self.data['params']['dsys_cfg']     = json_obj["params"].get("dsys_cfg",  None)
    self.data['params']['variable']     = json_obj["params"].get("variable",  None)
    self.data['params']['values']       = json_obj["params"].get("values",    []  )

  def read_config(self, file_path):
    with open(file_path, 'r') as file:
      self.data = json.load(file)

  def __str__(self):
    # String representation of the object for easy printing
    return (
      f"Prefix: {self.data['params']['prefix']}\n"
      f"Platform: {self.data['params']['platform']}\n"
      f"App: {self.data['params']['app']}\n"
      f"Dsys_cfg: {self.data['params']['dsys_cfg']}\n"
      f"Variable: {self.data['params']['variable']}\n"
      f"Values: {self.data['params']['values']}\n"
    )

  def calculate_paths(self, df):
    platform = df['params']['platform']
    
    path_dict = {
      'iss': join('vpro_sys_behavioral', 'TOOLS', 'VPRO', 'ISS', 'apps', df['params']['app']),
      'cnn': join('vpro_sys_behavioral', 'APPS', 'EISV', 'cnn_converter', 'nets', df['params']['app']),
    }
    subfolder = {
      'iss':{
        'log_file': join('build_release', 'log.txt'), 
        'trace_file': join('build_release', 'main_mem.trace')
      },
      'cnn':{
        'log_file': f'sim_{df["params"]["app"]}.log', 
        'trace_file': join('sim_results', 'main_mem.trace')
      }
    }
    
    df['paths']['path_to_log_file']            = join(
      df['paths']['zuse_avf_ki'], 
      path_dict[platform], 
      subfolder[platform]['log_file']
    )

    df['paths']['path_to_original_trace_file'] = join(
      df['paths']['zuse_avf_ki'], 
      path_dict[platform], 
      subfolder[platform]['trace_file']
    )

    df['paths']['path_to_dramsys_config_file'] = join(
      df['paths']['dramsys'], 
      'configs',
      df['params']['dsys_cfg']
    )

    folder = join(
      df['paths']['dramsys'], 
      'configs', 
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)

    df['paths']['path_to_created_config_file'] = join(
      folder,
      df['addpath']['filename_no_ext']+'.json'
    )

    folder = join(
      df['paths']['dramsys'], 
      'configs', 'traces',
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)

    df['paths']['path_to_created_trace_file']  = join(
      folder,
      df['addpath']['filename_no_ext']+".stl"
    )

    folder = join(
      df['paths']['output_data'],
      "dramsys_logs",
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)

    df['paths']['path_to_output_dramsys']      = join(
      folder,
      df['addpath']['filename_no_ext']+".log"
    )

    folder = join(
      df['paths']['output_data'], 
      'parsed_data',
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)

    df['paths']['path_to_output_parsed']       = join(
      folder,
      df['addpath']['filename_no_ext']+'.csv'
    )

    folder = join(
      df['paths']['output_data'], 
      'graphs',
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)
    
    df['paths']['path_to_output_graphs']       = join(
      folder,
      df['addpath']['filename_no_ext']+'.jpg'
    )

    folder = join(
      df['paths']['output_data'],
      'config',
      df['addpath']['relative_folder'],
    )
    makedirs(folder, exist_ok=True)

    df['paths']['path_to_config_file']         = join(
      folder,
      df['addpath']['filename_no_ext']+'.json'
    )

  def define_folder(self, df):
    tmp = df['params']
    df['addpath']['relative_folder'] = join(
      tmp['prefix'], 
      tmp['dsys_cfg'], 
      tmp['app'],
      tmp['variable']
    )
  
  def define_filename(self, value, df):
    tmp = df['params']
    df['addpath']['filename_no_ext'] = f"{tmp['prefix']}_{tmp['variable']}_{value}"

  def save_defaults(self):
    data = {'default_values': {}}

    data['default_values']['cluster'] =       self.DEFAULT_CLUSTER_VALUE
    data['default_values']['units'] =         self.DEFAULT_UNITS_VALUE
    data['default_values']['lanes'] =         self.DEFAULT_LANES_VALUE
    data['default_values']['clkMhz'] =        self.DEFAULT_CLKMHZ_VALUE
    data['default_values']['n_rams'] =        self.DEFAULT_NRAMS_VALUE
    data['default_values']['line_size'] =     self.DEFAULT_LINESIZE_VALUE
    data['default_values']['associativity'] = self.DEFAULT_ASSOCIATIVITY_VALUE
    data['default_values']['ram_size'] =      self.DEFAULT_RAMSIZE_VALUE
    data['default_values']['burst_length'] =  self.DEFAULT_BURST_LENGTH  

    folder = self.data['paths']['output_data']
    makedirs(folder, exist_ok=True)
    file_path = join(folder, 'default_values.json')

    with open(file_path, 'w') as f:
      json.dump(data, f, indent = 4)
      f.close()

    return file_path

  def save(self):
    newdata = self.data.copy()
    self.define_folder(newdata)
    file_list = []

    variable = self.data['params']['variable']
    values = self.data['params']['values']

    for value in values:
      newdata['configs'][variable] = value
      newdata['params']['value'] = value
      self.define_filename(value, newdata)
      self.calculate_paths(newdata)
      
      cfg_file = newdata['paths']['path_to_config_file']
      file_list.append(cfg_file)

      self.create_experiment(cfg_file)
    return file_list

  def create_experiment(self, filename):
    experiment = self.data
    with open(filename, 'w') as f:
      json.dump(experiment, f, indent = 4)
      f.close()
    return experiment

  def variable_map(self, variable):
    data = {
      'cluster': 'CLUSTERS',
      'units': 'UNITS',
      'lanes': 'LAMES',
      'n_rams': 'NR_RAMS',
      'line_size': 'LINE_SIZE',
      'associativity': 'ASSOCIATIVITY',
      'ram_size': 'RAM_SIZE'
    }
    return data[variable]

# TODO: create functions that provide the path to each of the processes of the simulation
# TODO: ISS
  
# TODO: CNN 
  def get_cnn_data(self):
    return {
      'path_to_cnn_conv':       join(self.data['paths']['zuse_avf_ki'], 'vpro_sys_behavioral', 'APPS', 'EISV', 'cnn_converter'),
      'app':                    self.data['params']['app'],
      'variable':               self.data['params']['variable'],
      'value':                  self.data['params']['value']
    }
  def update_config_file_cnn(
      self, 
      file,
      clkMhz, 
      n_cluster, 
      n_units, 
      n_lanes,
      n_rams,
      line_size,
      associativity,
      ram_size
    ):
    self.read_config(file)
    self.data['paths']['path_to_config_file'] = file
    self.data['configs']['cluster'] =       n_cluster,
    self.data['configs']['units'] =         n_units,
    self.data['configs']['lanes'] =         n_lanes,
    self.data['configs']['clkMhz'] =        clkMhz, 
    self.data['configs']['n_rams'] =        n_rams, 
    self.data['configs']['line_size'] =     line_size, 
    self.data['configs']['associativity'] = associativity, 
    self.data['configs']['ram_size'] =      ram_size
    self.save()

  
# TODO: DramSys converter
  def get_conv_data(self):
    return {
      'path_to_dramsys':        self.data['paths']['dramsys'],
      'path_to_new_trace_file': self.data['paths']['path_to_created_trace_file'],
      'path_to_old_trace_file': self.data['paths']['path_to_original_trace_file'],
      'path_to_old_cfg_file':   self.data['paths']['path_to_dramsys_config_file'],
      'path_to_new_cfg_file':   self.data['paths']['path_to_created_config_file'],
      'clkMhz':                 self.data['configs']['clkMhz'],
    }

  def update_config_file_conv(self, file, burst_length):
    self.read_config(file)
    self.data['configs']['burst_length'] = burst_length
    self.data['paths']['path_to_config_file'] = file
    self.save()
  
# TODO: Dramsys
  def get_dramsys_data(self):
    return {
      'path_to_dramsys':        self.data['paths']['dramsys'],
      'prefix':                 self.data['params']['prefix'],
      'output_file':            self.data['paths']['path_to_output_dramsys'],
      'cfg_file':               self.data['paths']['path_to_created_config_file'],
    }
  
# TODO: Parser
  def get_parser_data(self):
    return {
      'path_to_output_dramsys': self.data['paths']['path_to_output_dramsys'],
      'path_to_output_parsed':  self.data['paths']['path_to_output_parsed'],
    }
  
# TODO: analyser
  def get_analyser_data(self):
    return {
      'path_to_output_graphs':  None
    }