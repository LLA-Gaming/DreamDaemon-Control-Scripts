import os.path
import sys

import SS13.merge_config as merge_config
sys.path.append("..")
import update as git

saved_config = None

def pre_update(config):
  global saved_config

  if config.config_file:
    path_to_config_file = config.config_file
    print("SS13 Pre Update: Saving config file at " + path_to_config_file)
    saved_config = merge_config.parse_config(path_to_config_file)

    print(git.invoke_git("checkout", "--", config.config_file))


def post_update(config):
  if config.config_file:
    print("SS13 Post Update: Applying config file...")
    #Apply the saved config to the file updated via Git
    merge_config.apply_config_to_existing(config.config_file, saved_config)
