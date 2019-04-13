import os
import subprocess
import daemon
import locale
import config as global_config

def invoke_git(command, *args):
  process = subprocess.Popen(["git", command] + list(args), stdout=subprocess.PIPE, stderr=None)
  process.wait()
  return process.communicate()[0].decode(locale.getpreferredencoding(False))

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

def compile(config):
  subprocess.call([global_config.DM_INSTALL_PATH, config.dme])

def update_daemon(config):
  original_dir = os.getcwd()
  os.chdir(config.path)

  config.run_hook("pre_update")

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

  config.run_hook("post_update")

  compile(config)

  os.chdir(original_dir)
