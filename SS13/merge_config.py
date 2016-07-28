import re
from shutil import move
import sys

#Can optimise out regex later if necessary

blankLinePattern = "\s*"
blankLineRegex = re.compile(blankLinePattern)

commentPattern = "\s*#"
commentRegex = re.compile(commentPattern)

configPattern = "(?P<param>[^\s#]+)\s*(?P<value>.*)"
configRegex = re.compile(configPattern)

new_file = ""

def type_of_line(line):
  if blankLineRegex.match(line):
    return "blank"
  if commentRegex.match(line):
    return "comment"
  if configRegex.match(line):
    return "config"

def parse_config(config_path):
  with open(config_path, "r") as handle:
    initial_seek = handle.tell()
    config = dict()

    for line in handle:
      match_result = configRegex.match(line)
      if match_result:
        config[match_result.group("param")] = match_result.group("value")

    handle.seek(initial_seek)
    return config

def apply_config_to_existing(dest_path, stored_config):
  temp_config_path = dest_path + ".tmp"
  with open(dest_path, "r") as current_config, open(temp_config_path, "w") as temp_config:
    for line in current_config:
      config_match = configRegex.match(line)
      if config_match:
        param, value = config_match.group("param", "value")
        if param in stored_config:
          print("Using ", param, " : ", stored_config[param])
          temp_config.write(param + " " + stored_config[param] + "\n")
          continue

      #Write the original line to the new file if it's not a config line we have stored
      temp_config.write(line)

  old_config_path = dest_path + ".old"
  move(dest_path, old_config_path)
  move(temp_config_path, dest_path)
