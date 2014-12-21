#!/usr/bin/python

import psutil
import argparse

_PROCESS_NAME = "DreamDaemon"

parser = argparse.ArgumentParser(description="Restarts the DreamDaemon instance specified by the named '.dmb.'")
parser.add_argument("dmb", metavar="*.dmb", help="The .dmb name of the server to restart")
args = parser.parse_args()

def running_dreamdaemons():
  return [process for process in psutil.process_iter() 
          if process.name() == _PROCESS_NAME]

def is_daemon_running(daemon_dmb):
  for daemon in running_dreamdaemons():
    if args.dmb in daemon.cmdline(): return True
  return False

print(is_daemon_running(args.dmb))
