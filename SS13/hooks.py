import merge_config

saved_config = None

def pre_update(config):
  if config.config_file:
    saved_config = merge_config.parse_config(config.config_file)

def post_update(config):
  if config.config_file:
    #Apply the saved config to the file updated via Git
    merge_config.apply_config_to_existing(config.config_file, saved_config)
