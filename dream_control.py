#!/usr/bin/python

import argparse
from os.path import basename
from subprocess import call
from daemon import *

PATH_TO_ADMINS = "/"
PATH_TO_CRONTAB = "/"
PATH_TO_DMB = "/"
PORT = "52601"
DREAM_DAEMON_ARGS = ["-logself", "-trusted", "-unsafe_diag"]

def list_daemons(args):
  daemons = running_dreamdaemons()
  for daemon in daemons:
    print("Daemon: {0}".format(" ".join(daemon.cmdline())))

def start_daemon(args):
  call(["crontab", PATH_TO_CRONTAB])
  print("Starting daemon running {0}".format(args.dmb_path))
  start_daemon_if_stopped(args.dmb_path, args.dd_args)

def stop_default_daemon(args):
  call(["crontab", "-r"])
  args.dmb_name = basename(PATH_TO_DMB)
  print("Stopping daemon running {0}".format(args.dmb_name))
  stop_daemon(args.dmb_name)

def restart_default_daemon(args):
  args.dmb_name = basename(PATH_TO_DMB)
  print("Stopping daemon running {0}".format(args.dmb_name))
  stop_daemon(args.dmb_name, force=True)
  start_default_daemon(args)

def start_default_daemon(args):
  args.dmb_path = PATH_TO_DMB
  args.dd_args = [PORT] + DREAM_DAEMON_ARGS
  start_daemon(args)

def edit_admins(args):
  call(["nano", PATH_TO_ADMINS])

def _main():
  parser = argparse.ArgumentParser(description="Commands for controlling DreamDaemon instances")
  subparsers = parser.add_subparsers()

  parser_list = subparsers.add_parser("list", help="Lists all running daemons")
  parser_list.set_defaults(func=list_daemons)

  parser_start = subparsers.add_parser("start", help="Starts (if not currently running) the DreamDaemon instance specified by the named '.dmb.'")
  parser_start.add_argument("dmb_path", metavar="/foo/bar/*.dmb", help="Path to the .dmb used by the DreamDaemon instance")
  parser_start.add_argument("dd_args", metavar="...", nargs=argparse.REMAINDER, help="The arguments to pass to DreamDaemon, excluding the .dmb")
  parser_start.set_defaults(func=start_daemon)
  
  parser_stop = subparsers.add_parser("stop")
  parser_stop.add_argument("dmb_name", help="Name of the dmb (with or without .dmb) of the daemon you want to kill.")
  parser_stop.set_defaults(func=stop_daemon)

  parser_stop_default = subparsers.add_parser("stop_default")
  parser_stop_default.set_defaults(func=stop_default_daemon)

  parser_restart_default = subparsers.add_parser("restart_default")
  parser_restart_default.set_defaults(func=restart_default_daemon)

  parser_start_default = subparsers.add_parser("start_default")
  parser_start_default.set_defaults(func=start_default_daemon)

  parser_edit_admins = subparsers.add_parser("edit_admins")
  parser_edit_admins.set_defaults(func=edit_admins)

  args = parser.parse_args()
  args.func(args)

if __name__ == "__main__":
  _main()
