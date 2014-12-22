#!/usr/bin/python

import os
import os.path as path
import shutil
from time import gmtime, time, strftime

def utc_timestamp():
  time_struct = gmtime(time())
  return strftime("%H-%m-%Y-%m-%d", time_struct)

def make_backup(files, dest):
  if path.isfile(dest): return False

  final_path = path.join(dest, utc_timestamp())
  if not path.isdir(final_path):
    os.makedirs(final_path)

  for src in files:
    if os.path.isdir(src):
      final_dir_path = path.join(final_path, path.basename(src))
      shutil.copytree(src, final_dir_path)
    else:
      shutil.copy(src, final_path)
  return True
