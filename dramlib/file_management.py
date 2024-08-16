from os.path import join
from os import makedirs
import json

class DRAMConfigFile:
  def __init__(self):
    self.init_values()

  def start(self, input_file, path_file):
    self.read_input(input_file)
    self.read_path_file(path_file)
    self.calculate_paths()
    self.make_dirs()
  
  STANDARD_CLUSTER_VALUE = 8
  STANDARD_UNITS_VALUE = 8
  STANDARD_LANES_VALUE = 2
  STANDARD_CLKMHZ_VALUE = 200
  STANDARD_NRAMS_VALUE = 8
  STANDARD_LINESIZE_VALUE = 4096
  STANDARD_ASSOCIATIVITY_VALUE = 4
  STANDARD_RAMSIZE_VALUE = 524288
  STANDARD_BURST_LENGTH = 8
  
  def init_values(self):
    self.data = {}
    self.data['configs'] = {}
    self.data['params'] = {}
    self.data['paths'] = {}

    self.data['params']['prefix'] =     None
    self.data['params']['platform'] =   None
    self.data['params']['app'] =        None
    self.data['params']['dsys_cfg'] =   None
    self.data['params']['variable'] =   None
    self.data['params']['values'] =     None

    self.data['configs']['cluster'] =       self.STANDARD_CLUSTER_VALUE,
    self.data['configs']['units'] =         self.STANDARD_UNITS_VALUE,
    self.data['configs']['lanes'] =         self.STANDARD_LANES_VALUE,
    self.data['configs']['clkMhz'] =        self.STANDARD_CLKMHZ_VALUE, 
    self.data['configs']['n_rams'] =        self.STANDARD_NRAMS_VALUE, 
    self.data['configs']['line_size'] =     self.STANDARD_LINESIZE_VALUE, 
    self.data['configs']['associativity'] = self.STANDARD_ASSOCIATIVITY_VALUE, 
    self.data['configs']['ram_size'] =      self.STANDARD_RAMSIZE_VALUE
    self.data['configs']['burst_length'] =  self.STANDARD_BURST_LENGTH  

    self.data['paths']['path_to_log_file'] =            None,
    self.data['paths']['path_to_original_trace_file'] = None, 
    self.data['paths']['path_to_dramsys_config_file'] = None,
    self.data['paths']['path_to_created_config_file'] = None,
    self.data['paths']['path_to_created_trace_file'] =  None,
    self.data['paths']['path_to_output_dramsys'] =      None,
    self.data['paths']['path_to_output_parsed'] =       None,
    self.data['paths']['path_to_output_graphs'] =       None
    self.data['paths']['dramsys']         =             None
    self.data['paths']['zuse_avf_ki']     =             None
    self.data['paths']['output_data']     =             None

    self.data['addpath']['relative_folder'] =           None
    self.data['addpath']['filename_no_ext'] =           None
    self.data['addpath']['relative_filepath'] =         None
    self.data['addpath']['output'] =                    None

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

  def read_existing(self):
    pass

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
        'log_file': f'sim_{df['params']['app']}.log', 
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
       df['params']['zuse_avf_ki'], 
    )

    df['paths']['path_to_dramsys_config_file'] = join(
      df['paths']['dramsys'], 
      'configs',
      df['params']['dsys_cfg']
    )

    df['paths']['path_to_created_config_file'] = join(
      df['paths']['dramsys'], 
      'configs', 
      df['addpath']['filename_no_ext']+'.json'
    )

    df['paths']['path_to_created_trace_file']  = join(
      df['paths']['dramsys'], 
      'configs', 'traces',
      self.relative_file_path + ".stl"
    )

    df['paths']['path_to_output_dramsys']      = join(
      df['paths']['dramsys'], 
      'outputs',
      self.relative_file_path + ".log"
    )

    df['paths']['path_to_output_parsed']       = join(
      df['paths']['output_data'], 
      'parsed_data',
      df['addpath']['relative_filepath']+'.csv'
    )
    
    df['paths']['path_to_output_graphs']       = join(
      df['paths']['output_data'], 
      'graphs',
      df['addpath']['relative_folder']
    )

  def define_filename(self, value, df):
    tmp = df['params']
    self.filename_no_ext = f'{tmp['prefix']}_{tmp['variable']}_{value}'
    self.relative_file_path = join(self.relative_folder, self.filename_no_ext)

    df['addpath']['filename_no_ext'] =           self.filename_no_ext
    df['addpath']['relative_filepath'] =         self.relative_file_path

  def make_dirs(self, df):
    tmp = df['params']
    folder = f'{tmp['prefix']}'
    folder = join(folder, f'{tmp['dsys_cfg']}_{tmp['app']}')
    folder = join(folder, f'{tmp['variable']}')
    makedirs(folder, exist_ok=True)
    self.relative_folder = folder
    df['addpath']['relative_folder'] = folder

  def save(self, file:str):
    self.read_input(file)
    variable = self.data['params']['variable']
    values = self.data['params']['values']

    newdata = self.data[:]
    for value in values:
      newdata['config'][variable] = value
      self.calculate_paths(newdata)
      self.define_filename(value, newdata)
      self.make_dirs(newdata)
      
      self.create_experiment(self, join(newdata['addpath']['output'], newdata['addpath']['relative_filepath']+'.json'))

  def create_experiment(self, filename):
    experiment = self.data
    with open(filename, 'w') as f:
      json.dump(experiment, f)
      f.close()
    return experiment

# TODO: create functions that provide the path to each of the processes of the simulation
# TODO: ISS
  
# TODO: CNN 
  def get_cnn_data(self):
    return {
      'path_to_cnn_conv':       join(self.data['paths']['zuse_avf_ki'], 'APPS', 'EISV', 'cnn_converter'),
      'app':                    self.data['params']['app'],
      'variable':               self.data['configs']['variable'],
      'value':                  self.data['configs']['value']
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
    self.data['configs']['cluster'] =       n_cluster,
    self.data['configs']['units'] =         n_units,
    self.data['configs']['lanes'] =         n_lanes,
    self.data['configs']['clkMhz'] =        clkMhz, 
    self.data['configs']['n_rams'] =        n_rams, 
    self.data['configs']['line_size'] =     line_size, 
    self.data['configs']['associativity'] = associativity, 
    self.data['configs']['ram_size'] =      ram_size
    self.save(file)

  
# TODO: DramSys converter
  def get_conv_data(self):
    return {
      'path_to_new_trace_file': self.data['paths']['path_to_created_trace_file'],
      'path_to_old_trace_file': self.data['paths']['path_to_original_trace_file'],
      'path_to_old_cfg_file':   self.data['paths']['path_to_dramsys_config_file'],
      'path_to_new_cfg_file':   self.data['paths']['path_to_created_config_file'],
      'clkMhz':                 self.data['configs']['clkMhz']
    }

  def update_config_file_conv(self, file, burst_length):
    self.data['configs']['burst_length'] = burst_length
    self.save(file)
  
# TODO: Dramsys
  def get_dramsys_data(self):
    return {
      'path_to_dramsys':        self.data['paths']['dramsys'],
      'prefix':                 self.data['params']['prefix'],
      'output_dir':             self.data['paths']['path_to_output_dramsys'],
      'cfgs_dir':               self.data['paths']['path_to_created_config_file'],
    }
  
# TODO: Parser
  def get_parser_data(self):
    return {
      'path_to_output_parsed':  self.data['paths']['path_to_output_parsed'],
    }
  
# TODO: analyser