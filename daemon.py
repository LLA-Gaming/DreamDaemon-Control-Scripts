import os

def create_daemon(args):
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
  except OSError, e:
    return False

