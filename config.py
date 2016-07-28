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

CONFIGS = [
Config(
  name="Test",
  path="./test",
  dmb="teststation.dmb",
  dme="tgstation.dme",
  port="52601",
  args=["-logself", "-trusted", "-unsafe_diag"],
  backup_files=["config/admins.txt", "config/names"],
  backup_dest="",
  hooks={
    "pre_update": sample_hook,
    "post_update": sample_hook
  }
)
]

#Index of the default configuration to use.
DEFAULT_CONFIG = 0
