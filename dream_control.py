#!/usr/bin/python2

import argparse
import daemon
from os.path import basename
from subprocess import call
from daemon import *
from backup import make_backup
from config import CONFIGS

PATH_TO_CRONTAB = "/"
PATH_TO_DMB = "/"

def list_daemons(args):
  daemons = running_dreamdaemons()
  for daemon in daemons:
    print("Daemon: {0}".format(" ".join(daemon.cmdline())))

def start_daemon(args):
  call(["crontab", PATH_TO_CRONTAB])
  print("Starting daemon running {0}".format(args.dmb_path))
  start_daemon_if_stopped(args.dmb_path, args.dd_args)

def start_default_daemon(args):
  args.dmb_path = PATH_TO_DMB
  args.dd_args = [PORT] + DREAM_DAEMON_ARGS
  start_daemon(args)

def stop_daemon(args):
  call(["crontab", "-r"])
  print("Stopping daemon running {0}".format(args.dmb_name))
  daemon.stop_daemon(args.dmb_name)

def stop_default_daemon(args):
  args.dmb_name = basename(PATH_TO_DMB)
  stop_daemon(args)

def restart_default_daemon(args):
  args.dmb_name = basename(PATH_TO_DMB)
  print("Stopping daemon running {0}".format(args.dmb_name))
  stop_daemon(args.dmb_name, force=True)
  start_default_daemon(args)

def edit_admins(args):
  call(["nano", PATH_TO_ADMINS])

def backup(args):
  print("Beginning backup of {0} to {1}".format(str(args.files), str(args.dest)))
  if make_backup(args.files, args.dest):
    print("Backup successful")
  else:
    print("Backup failed, destination is probably a file")

def _main():
  parser = argparse.ArgumentParser(description="Commands for controlling DreamDaemon instances")
  subparsers = parser.add_subparsers()

  parser_list = subparsers.add_parser("list", help="Lists all running daemons")
  parser_list.set_defaults(func=list_daemons)

  parser_start = subparsers.add_parser("start", help="Starts (if not currently running) the DreamDaemon instance specified by the named '.dmb.'")
  parser_start.add_argument("dmb_path", metavar="/foo/bar/*.dmb", help="Path to the .dmb used by the DreamDaemon instance")
  parser_start.add_argument("dd_args", metavar="...", nargs=argparse.REMAINDER, help="The arguments to pass to DreamDaemon, excluding the .dmb")
  parser_start.set_defaults(func=start_daemon)

  parser_stop = subparsers.add_parser("stop", help="Stops the DreamDaemon instance specified by the named '.dmb.'")
  parser_stop.add_argument("dmb_name", metavar="*.dmb", help="Name of the .dmb used by the DreamDaemon instance")
  parser_stop.set_defaults(func=stop_daemon)

  parser_stop_default = subparsers.add_parser("stop_default", 
                                              help="""Stops the default daemon running and prevents autorestart.
                                                      Currently configured to: """ + PATH_TO_DMB)
  parser_stop_default.set_defaults(func=stop_default_daemon)

  parser_restart_default = subparsers.add_parser("restart_default",
                                                 help="""Immediately kills (SIGKILL) the default daemon and starts
                                                         it again. Currently configured to: """ + PATH_TO_DMB)
  parser_restart_default.set_defaults(func=restart_default_daemon)

  parser_start_default = subparsers.add_parser("start_default",
                                               help="""Starts the default daemon.
                                                       Currently configured to: """ + PATH_TO_DMB)
  parser_start_default.set_defaults(func=start_default_daemon)

  parser_edit_admins = subparsers.add_parser("edit_admins", help="Opens admins.txt in nano.")
  parser_edit_admins.set_defaults(func=edit_admins)

  parser_backup = subparsers.add_parser("backup", help="Backup a list of files to a directory.")
  parser_backup.add_argument("dest", help="Destination directory (Doesn't need to exist)")
  parser_backup.add_argument("files", metavar="file", help="File to copy", nargs="+")
  parser_backup.set_defaults(func=backup)

  args = parser.parse_args()
  args.func(args)

if __name__ == "__main__":
  _main()
