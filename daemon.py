import psutil
import os
from os.path import basename

PROCESS_NAME = "DreamDaemon"
DD_INSTALL_PATH = "/usr/local/byond/bin/DreamDaemon"

def create_daemon(args):
  """
  Spawns a new daemon running as an orphan. 
  Args: [0] is the executable name, the remaining list is passed as arguments to the 
  executable.
  """
  try:
    pid = os.fork() #Fork once, duplicating process
    if pid == 0:
      os.setsid() #Take leadership of a new session and new process group
      pid = os.fork() #Fork again, so no longer leader (can't attach to a terminal, orphaned)
      if pid == 0:
        try:
          maxfd = os.sysconf("SC_OPEN_MAX")
        except (AttributeError, ValueError):
          maxfd = 1024

        for fd in range(maxfd): #Close file descriptors
          try:
            os.close(fd)
          except OSError: #If fd wasn't open, ignore it
            pass

        os.execvp(args[0], args)
      else:
        os._exit(0)
    else:
      return True
  except OSError:
    return False

def stop_daemon(dmb_name, force=False):
  """
  Stops a running DreamDaemon instance, specified by the dmb name.
  """
  process = get_dreamdaemon(dmb_name)
  if process:
    if force:
      print("Process found, sending SIGKILL")
      process.kill()
    else:
      print("Process found, sending SIGTERM.")
      process.terminate()
  else:
    print("No process found.")

def running_dreamdaemons():
  """
  Returns a list of DreamDaemon processes.
  """
  return [process for process in psutil.process_iter() 
          if process.name() == PROCESS_NAME]

def get_dreamdaemon(dmb_name):
  """
  Returns the first daemon which has dmb_name in its arguments.
  """
  for daemon in running_dreamdaemons():
    for item in daemon.cmdline():
      if dmb_name in item: return daemon
  return False

def is_daemon_running(dmb_name):
  """
  True is a daemon can be found with dmb_name in its arguments.
  """
  if get_dreamdaemon(dmb_name): return True
  return False

def start_daemon_if_stopped(dmb_path, port, dreamdaemon_args):
  """
  Starts the daemon specified by arg 1 with the arguments specified by arg 2 
  if no daemon can be found running the dmb (or a dmb by the same name)
  """
  if not is_daemon_running(basename(dmb_path)):
    dd_args = [DD_INSTALL_PATH, dmb_path, port] + dreamdaemon_args
    return create_daemon(dd_args)
