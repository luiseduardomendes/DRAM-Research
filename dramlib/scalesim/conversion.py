from os.path import join, isfile, isdir
from os import listdir
from pprint import pprint
import pandas as pd
import numpy as np
import math
import re

#"outputs/MLPERF_AlphaGoZero_32x32_os/layer_wise/yolo_tiny_Conv2_dram_ofmap_write.csv"
#input_path = "outputs/MLPERF_AlphaGoZero_32x32_os/layer_wise/"
#network = "yolo_tiny"
#layer = "Conv2"
#config = "scale"

class Converter:
  def generate_output_file(self, config: str, network: str, layer: str) -> str:
    return f"trace_{config}_{network}_{layer}.stl"

  def generate_input_files_from_path(self, input_path: str, exec_tag: str, include_ifmap: bool = False) -> list:
    if include_ifmap:
      input_files = [
        join(input_path, f"{exec_tag}_dram_filter_read.csv"),
        join(input_path, f"{exec_tag}_dram_ifmap_read.csv"),
        join(input_path, f"{exec_tag}_dram_ofmap_write.csv"),
      ]
    else:
      input_files = [
        join(input_path, f"{exec_tag}_dram_filter_read.csv"),
        join(input_path, f"{exec_tag}_dram_ofmap_write.csv"),
      ]
    for f in input_files:
      if not isfile(f):
        raise Exception(f"File {f} not found")
    return input_files

  def generate_exec_tag(self, network, layer):
    return f"{network}_{layer}"
  
  def generate_input_path(self, input_path, config):
    return join(input_path, config, "layer_wise")
  
  def generate_layer_list(self, network_path, network):
    files = [f for f in listdir(network_path) if f.endswith('_dram_filter_read.csv')]
    re.compile('')
    layer_list = []
    for filename in files:
      layer_and_rest = filename[len(network) + 1:]
      layer = layer_and_rest.rsplit('_dram_filter_read.csv', 1)[0]
      layer_list.append(layer)
    return layer_list
  
  def generate_config_list(self, scalesim_output_path):
    path = scalesim_output_path
    return [f for f in listdir(path) if isdir(join(path, f)) and isdir(join(path, f, "layer_wise"))]

  def generate_network_list(self, config_path):
    configs = [f for f in listdir(config_path) if f.endswith("_avg_bw.csv")]
    return [f.split("_avg_bw.csv")[0] for f in configs]

  def __generate_msg__(self, read, counter, accesses):
    msgs = []
    for access in accesses:
      msg = f"{counter}:\t"
      if read:
        msg += "read\t"
      else:
        msg += "write\t"
      msg += access + "\n"
      msgs.append(msg)
      counter += 1
    return msgs, counter

  def __parse_accesses__(self, row):
    accesses = row.split(',')[1:-1]
    accesses = [float(access) for access in accesses]
    return accesses

  def __is_read_file__(self, input_file):
    return input_file[-8:-4] == "read"

  def to_dramsys(self, path, network, layer, config, max_consecutive_data, include_ifmap=True):
    exec_tag = self.generate_exec_tag(network, layer)
    input_path = self.generate_input_path(path, config)
    input_files = self.generate_input_files_from_path(input_path, exec_tag, include_ifmap)
    output_file = self.generate_output_file(config, network, layer)

    self.convert(input_files, output_file, max_consecutive_data)

  def convert(self, input_files: list, output_file: str, max_consecutive_data):
    counter = 0
    with open(output_file, "w") as out:
      for input_file in input_files:
        read = self.__is_read_file__(input_file)
        df = pd.read_csv(input_file, header=None)
        to_list = self.scale_to_list_binary(df, max_consecutive_data)
        for row in to_list:
          msgs, counter = self.__generate_msg__(read, counter, row)
          for msg in msgs:
            out.write(msg)
      out.close()

  # convert all files in a given output folder
  def convert_all(self, path, max_consecutive_data, include_ifmap):
    file_structure = self.generate_structure_dict(path)
    result = {
      "path": [],
      "network": [],
      "layer": [],
      "config": []
    }

    for config in file_structure.keys():
      for network in file_structure[config].keys():
        for layer in file_structure[config][network]:
          #print(path, network, layer, config)
          result["path"].append(path)
          result["network"].append(network)
          result["layer"].append(layer)
          result["config"].append(config)
          #self.to_dramsys(path, network, layer, config, max_consecutive_data, include_ifmap)
    pd.DataFrame(result).to_csv("result.csv")

  def scale_to_list_binary(self, data, max_consecutive_data):
    data = data.applymap(convert_to_int)
    #print(data)
    data = data.iloc[:,1:-1]
    data = data.to_numpy()
    #print(data)
    row_d, col = data.shape
    
    lsb_bits = int(math.log2(max_consecutive_data))
    data_list = data.tolist()
    #print(np.asarray(data_list).shape)
    #pprint(data_list)
    bin_list = []
    for row in data_list:
      temp_list = []
      for val in row:
        bin_val = int_to_binary(int(abs(val)))
        if lsb_bits != 0:
          round_bin = bin_val[:-lsb_bits]
          final_bin = round_bin.ljust(32, "0")
        else:
          final_bin = bin_val[:]
        temp_list.append(final_bin)
      bin_list.append(temp_list)
    
    #pprint(bin_list)
    int_list = []
    flat_list = []
    for row in bin_list:
      tmp = []
      for val in row:

        int_val = int(val, 2)
        if lsb_bits == 6:
            int_val = int_val >> 1
        tmp.append(int_val)
        flat_list.append(int_val)

      int_list.append(tmp)
    data_new = np.array(int_list)
    flatt_list_new = list(set(flat_list))
    res_dict = dict()
    #pprint(data_new)

    for q in range(row_d):
      name = "row" + str(q)
      res_dict[name] = []

    for d in flatt_list_new:
      idxs = np.where(data_new == d)
      res_dict["row"+str(idxs[0][0])].append(d)

    #pprint(res_dict)
    final_list = []
    counter = 0
    for _, key in enumerate(res_dict):
      temp_list = []
      i = res_dict[key]
      if i:
        counter += 1
        for j in i:
          tmp = j
          if(tmp != -1):
            tmp = "0x" + str(tmp)
            temp_list.append(tmp)
        final_list.append(temp_list)
    return final_list
  
  def generate_structure_dict(self, path):
    configs = self.generate_config_list(path)
    networks = {config: self.generate_network_list(join(path, config)) for config in configs}
    data = {
      config: {
        network: 
          self.generate_layer_list(
            self.generate_input_path(path, config), 
            network
          ) 
          for network in networks[config]
      } for config in networks.keys()
    }
    return data

  def generate_structure(self, path):
    data = self.generate_structure_dict(path)

    multi_index_tuples = []

    for key1, subdict in data.items():
      for key2, layers in subdict.items():
        for layer in layers:
          multi_index_tuples.append((key1, key2, layer))

    # Preparar a lista de tuplas para os índices e a colu"na
    rows = []

    for key1, subdict in data.items():
      for key2, layers in subdict.items():
        for layer in layers:
          rows.append((key1, key2, layer))

    # Criar o DataFrame a partir das listas
    df = pd.DataFrame(rows, columns=["Configuration", "Network", "Layer"])

    # Definir os índices de nível superior
    df.set_index(["Configuration", "Network"], inplace=True)
    return df


def convert_to_int(value):
    try:
      if isinstance(value, float) and value.is_integer():
          return int(value)
      
      return int(float(value))
    except (ValueError, TypeError):
      return -1
    
def int_to_binary(a):
  return  '{0:032b}'.format(a)

