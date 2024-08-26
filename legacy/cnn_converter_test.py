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
   11, 2, 4, 8, 16
]

path_to_dramsys = "/home/luismendes/DRAMSys"
path_to_iss = "/home/luismendes/zuse_ki_avf/vpro_sys_behavioral/TOOLS/VPRO/ISS"
path_to_cnn_conv = "/home/luismendes/zuse_ki_avf/vpro_sys_behavioral/APPS/EISV/cnn_converter"

for cluster_size in cluster_sizes:
    conv = Converter(path_to_dramsys, path_to_iss, app_name)

    cnn_conv = CNNConv(path_to_cnn_conv, app_name)
    cnn_conv.run(units=cluster_size)

    path_to_log_file = cnn_conv.get_log_file_path()

    iss_parser = ISSParser()
    clkMhz, n_cluster, n_units, n_lanes = iss_parser.parse_file(path_to_log_file)

    experiment_state = f'CL{n_cluster}UN{n_units}LN{n_lanes}'

    path_to_output_log_files = 'output_dramsys_log_' + experiment_prefix
    path_to_output_parsed_files = "output_parsed_log_" + experiment_prefix

    if not exists(path_to_output_log_files):
      makedirs(path_to_output_log_files)

    if not exists(path_to_output_parsed_files):
      makedirs(path_to_output_parsed_files)

    stl_filename = f"{experiment_prefix}_trace_{app_name}_{experiment_state}.stl"
    path_to_new_trace_file_folder = join(conv.get_path('trc'), experiment_prefix)
    path_to_new_trace_file = join(path_to_new_trace_file_folder, stl_filename)

    new_cfg_filename = f"{experiment_prefix}_cfg_{app_name}_{experiment_state}.json"
    path_to_new_cfg_file_folder = join(conv.get_path('cfg'), 'costum_configs', experiment_prefix)
    path_to_new_cfg_file = join(path_to_new_cfg_file_folder, new_cfg_filename)

    predicted_output_log = f"{experiment_prefix}_cfg_{app_name}_{experiment_state}_log.txt"
    path_to_predicted_output_log = join(path_to_output_log_files, predicted_output_log)

    path_to_old_trace_file = cnn_conv.get_trace_file_path()

    path_to_old_cfg_file = join(conv.get_path('cfg'), cfg_file)


    burst_length = conv.conv(
      path_to_new_trace_file, 
      path_to_old_trace_file
    )

    conv.create_new_config_file(
      path_to_old_cfg_file, 
      path_to_new_cfg_file, 
      path_to_new_trace_file, 
      burst_length, clkMhz
    )



dsys = Dramsys(path_to_dramsys, experiment_prefix)
log_files_generated = dsys.run_simulation(output_dir=path_to_output_log_files)


parser = DRAMParser(True)
for file in log_files_generated:
  parser.parse_file(file, path_to_output_parsed_files)