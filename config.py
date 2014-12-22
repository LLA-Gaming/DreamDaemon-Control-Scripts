import os.path

CONFIGS = [
{
  "name": "Test",
  "path": "/",
  "dmb": "teststation.dmb",
  "port": "52601",
  "args": ["-logself", "-trusted", "-unsafe_diag"],
  "backup_files": ["config/admins.txt"],
  "backup_dest": "/"
}
]

#Index of the default configuration to use.
DEFAULT_CONFIG = 0


def get_dmb_path(config):
  return os.path.join(config["path"], config["dmb"])
