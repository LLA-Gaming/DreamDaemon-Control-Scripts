import os
import subprocess
import daemon
from config import CONFIGS, DEFAULT_CONFIG

def invoke_git(command, *args):
  process = subprocess.Popen(["git", command] + list(args), stdout=subprocess.PIPE, stderr=None)
  process.wait()
  return process.communicate()[0]

def git_latest_version():
  all_tags = invoke_git("tag", "-l").split("\n")
  version_tags = [tag for tag in all_tags if len(tag) > 0 and tag[0] == "v"]
  version_tags.sort(reverse=True)
  return version_tags[0]

def git_checkout(ref):
  invoke_git("checkout", ref)

def git_stash(command="save"):
  invoke_git("stash", command)

def git_fetch():
  invoke_git("fetch", "--all", "--tags")

def is_git_repo(path):
  return os.path.exists(os.path.join(path, ".git"))

def compile(config):
  subprocess.call(["DreamMaker", config.dme])

def update_daemon(config):
  original_dir = os.getcwd()
  if not is_git_repo(config.path):
    print("Target directory is not a git repository.")
    return False
  os.chdir(config.path)

  git_stash()
  git_fetch()

  try:
    version = git_latest_version()
  except IndexError:
    print("Unable to locate latest version, aborting.")
    return
 
  print("Checking out version " + version)
  git_checkout(version)
  git_stash("pop")

  compile(config)

  os.chdir(original_dir)
  return True
