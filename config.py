import os.path

import SS13.hooks

class Config:
  def __init__(self, **kwargs):
    if kwargs:
      self.__dict__ = kwargs

  def items(self):
    return self.__dict__.items()

  def get_dmb_path(self):
    return os.path.join(self.path, self.dmb)

  def run_hook(self, hook_name):
    if self.hooks and hook_name in self.hooks:
      return self.hooks[hook_name](self)

def sample_hook(config):
  print("Hello from the Sample Hook!")

DD_INSTALL_PATH = "/usr/local/byond/bin/DreamDaemon"
DM_INSTALL_PATH = "/usr/local/byond/bin/DreamMaker"
PATH_TO_CRONTAB = "/root/SS13/scripts/ss13.cron"

CONFIGS = [
Config(
  name="Test",
  path="../tgstation",
  dmb="tgstation.dmb",
  dme="tgstation.dme",
  port="52601",
  args=["-logself", "-trusted", "-unsafe_diag"],
  config_file="config/config.txt",
  backup_files=["config/admins.txt", "config/names"],
  backup_dest="",
  hooks={
    "pre_update": SS13.hooks.pre_update,
    "post_update": SS13.hooks.post_update
  }
)
]

#Index of the default configuration to use.
DEFAULT_CONFIG = 0
