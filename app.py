from dramlib import DRAMConfigFile

input_file = 'example2.json'
path_file  = 'paths.json'

dcf = DRAMConfigFile()
dcf.start(input_file, path_file)
dcf.save_defaults()
dcf.save()