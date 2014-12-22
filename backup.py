#!/usr/bin/python

import os
import os.path as path
import shutil
from time import gmtime, time, strftime

def utc_timestamp():
  time_struct = gmtime(time())
  return strftime("%H-%m-%Y-%m-%d", time_struct)

def make_backup(basedir, files, dest):
  if path.isfile(dest): return False

  final_path = path.join(dest, utc_timestamp())
  if not path.isdir(final_path):
    os.makedirs(final_path)

  for relative_path in files:
    file_path = path.join(basedir, relative_path)
    if path.isdir(file_path):
      final_dir_path = path.join(final_path, path.basename(file_path))
      shutil.copytree(file_path, final_dir_path)
    else:
      shutil.copy(file_path, final_path)
  return True
