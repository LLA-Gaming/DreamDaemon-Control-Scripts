#!/usr/bin/python

import psutil
import argparse
import subprocess
import os
import os.path
from os.path import basename

PROCESS_NAME = "DreamDaemon"
DD_INSTALL_PATH = "/usr/local/byond/bin/DreamDaemon"


def running_dreamdaemons():
  return [process for process in psutil.process_iter() 
          if process.name() == PROCESS_NAME]

def is_daemon_running(dmb_name):
  for daemon in running_dreamdaemons():
    if dmb_name in daemon.cmdline(): return True
  return False

def restart_server(dmb_path, dreamdaemon_args):
  if not is_daemon_running(basename(dmb_path)):
    dd_args = [DD_INSTALL_PATH, dmb_path] + dreamdaemon_args
    return create_daemon(dd_args)

def create_daemon(args):
  try:
    pid = os.fork() #Fork once, duplicating process
  except OSError, e:
    raise Exception, "{:s} [{:d}]".format(e.strerror, e.errno)

  if pid == 0:
    os.setsid() #Take leadership of a new session and new process group
    try:
      pid = os.fork() #Fork again, so no longer leader (can't attach to a terminal, orphaned)
    except OSError, e:
      raise Exception, "{:s} [{:d}]".format(e.strerror, e.errno)

    if pid == 0:
      try:
        maxfd = os.sysconf("SC_OPEN_MAX")
      except (AttributeError, ValueError):
        maxfd = 1024

      for fd in range(maxfd):
        try:
          os.close(fd)
        except OSError: #If fd wasn't open, ignore it
          pass

      os.execvp(args[0], args)
    else:
      os._exit(0)
  else:
    return True

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
