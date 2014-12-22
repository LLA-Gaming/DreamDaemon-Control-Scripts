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

  final_path = os.path.join(dest, utc_timestamp())
  if not path.isdir(final_path):
    os.makedirs(final_path)

  for src in files:
    shutil.copy(src, final_path)
  return True
