#!/usr/bin/python

import argparse
from os.path import basename
from subprocess import call
from restart_dreamdaemon import get_dreamdaemon, restart_server, running_dreamdaemons

PATH_TO_ADMINS = "/"
PATH_TO_CRONTAB = "/"
PATH_TO_DMB = "/"
PORT = "52600"
DREAM_DAEMON_ARGS = ["-logself", "-trusted", "-unsafe_diag"]

def list_daemons():
  daemons = running_dreamdaemons()
  for daemon in daemons:
    print("Daemon: {0}".format(" ".join(daemon.cmdline)))

def stop_daemon(args):
  call(["crontab", "-r"])
  process = get_dreamdaemon(args.dmb_name)
  process.terminate()

def stop_default_daemon(args):
  args.dmb_name = basename(PATH_TO_DMB)
  stop_daemon(args)

def restart_default_daemon():
  restart_server(PATH_TO_DMB, [PORT] + DREAM_DAEMON_ARGS)

def start_default_daemon():
  call(["crontab", PATH_TO_CRONTAB])
  restart_daemon()

def edit_admins():
  call(["nano", PATH_TO_ADMINS])

def _main():
  parser = argparse.ArgumentParser(desc="Commands for controlling DreamDaemon instances")
  subparsers = parser.add_subparsers()

  parser_list = subparsers.add_parser("list", help="Lists all running daemons")
  parser_list.set_defaults(func=list_daemons)
  
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
