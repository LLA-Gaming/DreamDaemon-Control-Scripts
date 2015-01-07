import os.path

class Config:
  def __init__(self, **kwargs):
    if kwargs:
      self.__dict__ = kwargs

  def items(self):
    return self.__dict__.items()

  def get_dmb_path(self):
    return os.path.join(self.path, self.dmb)

CONFIGS = [
Config(
  name="Test",
  path="",
  dmb="teststation.dmb",
  dme="tgstation.dme",
  port="52601",
  args=["-logself", "-trusted", "-unsafe_diag"],
  backup_files=["config/admins.txt", "config/names"],
  backup_dest=""
),
Config(
  name="Main",
  path="",
  dmb="tgstation.dmb",
  dme="tgstation.dme",
  port="52600",
  args=["-logself", "-trusted", "-unsafe_diag"],
  backup_files=["config/admins.txt"],
  backup_dest=""
)
]

#Index of the default configuration to use.
DEFAULT_CONFIG = 0
