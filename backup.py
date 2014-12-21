#!/usr/bin/python

import os
import os.path as path
import shutil
import argparse
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

def _main():
  parser = argparse.ArgumentParser(description="Backup a list of files to a directory.")
  parser.add_argument("dest", help="Destination directory (Doesn't need to exist)")
  parser.add_argument("files", metavar="file", help="File to copy", nargs="+")
  args = parser.parse_args()

  print("Beginning backup of {0} to {1}".format(str(args.files), str(args.dest)))
  if make_backup(args.files, args.dest):
    print("Backup successful")
  else:
    print("Backup failed, destination is probably a file")

if __name__ == "__main__":
  _main()
