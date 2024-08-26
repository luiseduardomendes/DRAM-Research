from dramlib.iss.converter import Converter
from dramlib.dramsys.simulation import Dramsys
from dramlib.dramsys.parsing import Parser as DRAMParser
from dramlib.iss import Parser as ISSParser
from dramlib.cnn_conv.cnn_conv import CNNConv
from os.path import join, exists
from os import makedirs

experiment_prefix = 'cnn_conv'
app_name = 'yololite'
cfg_file = 'ddr4-example.json'
cluster_sizes = [
   1, 2, 4, 8, 16
]

path_to_dramsys = "/home/luismendes/DRAMSys"
path_to_iss = "/home/luismendes/zuse_ki_avf/vpro_sys_behavioral/TOOLS/VPRO/ISS"
path_to_cnn_conv = "/home/luismendes/zuse_ki_avf/vpro_sys_behavioral/APPS/EISV/cnn_converter"

conv = Converter(path_to_dramsys, path_to_iss, app_name)
cnn_conv = CNNConv(path_to_cnn_conv, app_name)
iss_parser = ISSParser()

for cluster_size in cluster_sizes:
  cnn_conv.run(units=cluster_size)

  # === determining experiment features ===
  path_to_log_file = cnn_conv.get_log_file_path()
  clkMhz, n_cluster, n_units, n_lanes = iss_parser.parse_file(path_to_log_file)
  experiment_state = f'CL{n_cluster}UN{n_units}LN{n_lanes}'

  # === check existance ===
  # TODO: determine a way to be able to put together all the experiment state
  # information with the logs generated, so that the file names doesnt need to
  # have all the needed information

  # === new file management system ===
  # 
  # main idea: create a file which contains the path to all the logs related to
  # that specific run of the simulators
  #
  # to use this kind of file management, we first need to develop a script that
  # automatically creates this file and all the necessary information:
  # the script must receive as input a config file as following
  #
  # params:{
  #   prefix: cluster01
  #   platform: [iss | cnn]
  #   app: [conv2d, ... | yololite, ...]
  #   dsys_cfg: ddr4-example.json
  #   variable: [cluster, units, lanes, ...]
  #   values: [1, 2, 4, 8, 16]
  # }
  #
  # and then produce as output the following information
  #
  # {
  #   experiment:{
  #     params:{
  #       prefix: cluster01
  #       platform: [iss/cnn]
  #       app: [conv2d/yololite]
  #       dsys_cfg: ddr4-example.json
  #     }
  #     paths:{
  #      path_to_log_file: /home/luismendes/...    
  #      path_to_original_trace_file: /home/luismendes/...
  #      path_to_dramsys_config_file: /home/luismendes/...
  #      path_to_created_trace_file: /home/luismendes/...
  #      path_to_output_iss: /home/luismendes/...
  #      path_to_output_dramsys: /home/luismendes/...
  #      path_to_output_parsed: /home/luismendes/...
  #      path_to_output_graphs: /home/luismendes/...
  #     }
  #     config:{
  #       clusters: 8
  #       units: 8
  #       lanes: 2
  #       clkMhz: 200
  #       n_rams: 8
  #       line_size: 4096
  #       associativity: 4
  #       ram_size: 524288
  #     }
  #   }
  # }
  #
  # it will produce one json file for each of the values indicated in the input
  # changing the value of the interest variable
  #
  # after that, all of the classes in the environment must be able to receive a 
  # json file as input and then fill the needed fields for each of the classes

  # === creating path to output logs ===
  path_to_output_log_files = 'output_' + experiment_prefix + '_dramsys_log'
  makedirs(path_to_output_log_files, exist_ok=True)
  path_to_output_parsed_files = "output_"+ experiment_prefix + "_parsed_log"
  makedirs(path_to_output_parsed_files, exist_ok=True)

  # === creating path to config files ===
  new_cfg_filename = f"{experiment_prefix}_cfg_{app_name}_{experiment_state}.json"
  path_to_new_cfg_file = join(conv.get_path('cfg'), 'costum_configs', experiment_prefix, new_cfg_filename)
  path_to_old_cfg_file = join(conv.get_path('cfg'), cfg_file)

  # === creating path to trace files ===
  stl_filename = f"{experiment_prefix}_trace_{app_name}_{experiment_state}.stl"
  path_to_new_trace_file = join(conv.get_path('trc'), experiment_prefix, stl_filename)
  path_to_old_trace_file = cnn_conv.get_trace_file_path()
  
  # === converting trace file ===
  burst_length = conv.conv(
    path_to_new_trace_file, 
    path_to_old_trace_file
  )

  # === editing config file ===
  conv.create_new_config_file(
    path_to_old_cfg_file, 
    path_to_new_cfg_file, 
    path_to_new_trace_file, 
    burst_length, clkMhz
  )

# === running dramsys analysis over all generated files ===
dsys = Dramsys(path_to_dramsys, experiment_prefix)
log_files_generated = dsys.run_simulation(output_dir=path_to_output_log_files)

# === running parsing over all generated files ===
parser = DRAMParser(True)
for file in log_files_generated:
  parser.parse_file(file, path_to_output_parsed_files)