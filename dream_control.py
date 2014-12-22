#!/usr/bin/python2

import argparse
import daemon
from os.path import basename
from subprocess import call
from daemon import *
from backup import make_backup
from config import CONFIGS, DEFAULT_CONFIG, get_dmb_path

PATH_TO_CRONTAB = "/"

def list_configs(args):
  count = 0
  for config in CONFIGS:
    print("Config {0}:".format(count))
    for (key, value) in config.iteritems():
      print("    {0}: {1}".format(key, value))
    print("\n")
    count += 1

def list_daemons(args):
  daemons = running_dreamdaemons()
  for daemon in daemons:
    print("Daemon: {0}".format(" ".join(daemon.cmdline())))

def start_daemon(args):
  config = CONFIGS[args.config]
  call(["crontab", PATH_TO_CRONTAB])
  print("Starting daemon running {0}".format(config["dmb"]))
  start_daemon_if_stopped(get_dmb_path(config), config["port"], config["args"])

def start_default_daemon(args):
  args.config = DEFAULT_CONFIG
  start_daemon(args)

def stop_daemon(args):
  call(["crontab", "-r"])
  print("Stopping daemon running {0}".format(args.dmb_name))
  daemon.stop_daemon(args.dmb_name, args.force)

def stop_default_daemon(args):
  args.dmb_name = CONFIGS[DEFAULT_CONFIG]["dmb"]
  stop_daemon(args)

def restart_default_daemon(args):
  stop_default_daemon(args)
  start_default_daemon(args)

def edit_admins(args):
  call(["nano", os.path.join(CONFIG[DEFAULT_CONFIG]["path"], "config/admins.txt")])

def backup(args):
  print("Beginning backup of {0} to {1}".format(str(args.files), str(args.dest)))
  if make_backup(args.files, args.dest):
    print("Backup successful")
  else:
    print("Backup failed, destination is probably a file")

def _main():
  parser = argparse.ArgumentParser(description="Commands for controlling DreamDaemon instances")
  subparsers = parser.add_subparsers()

  parser_list_daemons = subparsers.add_parser("list_daemons", help="Lists all running daemons")
  parser_list_daemons.set_defaults(func=list_daemons)

  parser_list_configs = subparsers.add_parser("list_configs", help="Lists all available configurations")
  parser_list_configs.set_defaults(func=list_configs)

  parser_list = subparsers.add_parser("list", help="Lists all running daemons")
  parser_list.set_defaults(func=list_daemons)

  parser_start = subparsers.add_parser("start", help="Starts (if not currently running) the DreamDaemon instance specified by the config number.")
  parser_start.add_argument("config", type=int, help="Config number of the chosen configuration, e.g 1, 2, 3.")
  parser_start.set_defaults(func=start_daemon)

  parser_stop = subparsers.add_parser("stop", help="Stops the DreamDaemon instance specified by the named '.dmb.'")
  parser_stop.add_argument("dmb_name", metavar="*.dmb", help="Name of the .dmb used by the DreamDaemon instance")
  parser_stop.add_argument("-force", action="store_true", help="Sends SIGKILL instead of SIGTERM - Kills it outright")
  parser_stop.set_defaults(func=stop_daemon)

  parser_stop_default = subparsers.add_parser("stop_default", 
                                              help="""Stops the default daemon running and prevents autorestart.
                                                      Currently configured to: """ + CONFIGS[DEFAULT_CONFIG]["path"])
  parser_stop_default.add_argument("-force", action="store_true", help="Sends SIGKILL instead of SIGTERM - Kills it outright")
  parser_stop_default.set_defaults(func=stop_default_daemon)

  parser_restart_default = subparsers.add_parser("restart_default",
                                                 help="""Immediately kills (SIGKILL) the default daemon and starts
                                                         it again. Currently configured to: """ + CONFIGS[DEFAULT_CONFIG]["path"])
  parser_restart_default.set_defaults(func=restart_default_daemon)

  parser_start_default = subparsers.add_parser("start_default",
                                               help="""Starts the default daemon.
                                                       Currently configured to: """ + CONFIGS[DEFAULT_CONFIG]["path"])
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
