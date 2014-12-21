#!/usr/bin/python

import psutil
import argparse
import subprocess

PROCESS_NAME = "DreamDaemon"
DD_INSTALL_PATH = "/usr/local/byond/bin/DreamDaemon"


def running_dreamdaemons():
  return [process for process in psutil.process_iter() 
          if process.name() == PROCESS_NAME]

def is_daemon_running(dmb_name):
  for daemon in running_dreamdaemons():
    if dmb_name in daemon.cmdline(): return True
  return False

def restart_server(dmb_name, dreamdaemon_args):
  if not is_daemon_running(dmb_name):
    dd_args = [DD_INSTALL_PATH, dmb_name] + dreamdaemon_args
    process = subprocess.Popen(dd_args)
    return process

def main():
  parser = argparse.ArgumentParser(description="Restarts the DreamDaemon instance specified by the named '.dmb.'")
  parser.add_argument("dmb", metavar="*.dmb", help="The .dmb name of the server to restart")
  parser.add_argument("dd_args", metavar="...", nargs=argparse.REMAINDER, help="The arguments to pass to DreamDaemon, excluding the .dmb")
  args = parser.parse_args()

  process = restart_server(args.dmb, args.dd_args)
  if process.returncode == None or process.returncode == 0:
    print("Command run successfully, PID: " + str(process.pid))
  else:
    print("Command failed with return code " + str(process.returncode))

if __name__ == "__main__":
  main()
