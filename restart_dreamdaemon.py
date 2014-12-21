#!/usr/bin/python

import psutil
import argparse
import subprocess
from daemon import create_daemon
import os.path
from os.path import basename

PROCESS_NAME = "DreamDaemon"
DD_INSTALL_PATH = "/usr/local/byond/bin/DreamDaemon"


def running_dreamdaemons():
  return [process for process in psutil.process_iter() 
          if process.name() == PROCESS_NAME]

def get_dreamdaemon(dmb_name):
  for daemon in running_dreamdaemons():
    for item in daemon.cmdline():
      if dmb_name in item: return daemon
  return False

def is_daemon_running(dmb_name):
  if get_dreamdaemon(dmb_name): return True
  return False

def restart_server(dmb_path, dreamdaemon_args):
  if not is_daemon_running(basename(dmb_path)):
    dd_args = [DD_INSTALL_PATH, dmb_path] + dreamdaemon_args
    return create_daemon(dd_args)

def main():
  parser = argparse.ArgumentParser(description="Restarts the DreamDaemon instance specified by the named '.dmb.'")
  parser.add_argument("dmb_path", metavar="/foo/bar/*.dmb", help="Path to the .dmb used by the DreamDaemon instance")
  parser.add_argument("dd_args", metavar="...", nargs=argparse.REMAINDER, help="The arguments to pass to DreamDaemon, excluding the .dmb")
  args = parser.parse_args()

  process = restart_server(args.dmb_path, args.dd_args)
  if not process:
    print("Server is already running!")
  else:
    print("Attempting to spawn server.")

if __name__ == "__main__":
  main()
