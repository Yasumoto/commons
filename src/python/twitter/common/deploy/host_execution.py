import getpass
import time

from twitter.common import log
from twitter.common.lang import AbstractClass

from ansible.runner import Runner
import pkg_resources


#TODO(jsmith): Upgrade version of PEX to 1.0 to remove + improve this
def access_zipped_assets(static_module_name, static_path, asset_path, dir_location='.'):
  """
  Create a copy of static resource files as we can't serve
  them from within the pex file.


  :param static_module_name: Module name containing module to cache in a tempdir
  :type static_module_name: string in the form of 'twitter.common.zookeeper'
  :param static_path: Module name of the form 'serverset'
  :param asset_path: Initially a module name that's the same as the static_path, but will be
      changed to walk the directory tree
  :param dir_location: directory to create a new temporary directory in
  """
  import os
  from twitter.common.dirutil import safe_mkdir, safe_mkdtemp
  temp_dir = safe_mkdtemp(dir=dir_location)
  for asset in pkg_resources.resource_listdir(static_module_name, asset_path):
    asset_target = os.path.join(os.path.relpath(asset_path, static_path), asset)[2:]
    if pkg_resources.resource_isdir(static_module_name, os.path.join(asset_path, asset)):
      safe_mkdir(os.path.join(temp_dir, asset_target))
      access_zipped_assets(static_module_name, static_path, os.path.join(asset_path, asset))
    else:
      with open(os.path.join(temp_dir, asset_target), 'wb') as fp:
        path = os.path.join(static_path, asset_target)
        file_data = pkg_resources.resource_string(static_module_name, path)
        fp.write(file_data)
  return temp_dir

class SchedulerExecution(AbstractClass):
  """Run commands on a set of Hosts."""

  class Error(Exception): pass
  class RemoteExecutionError(Error): pass

  def __init__(self, hostnames, cluster):
    """
    :param hostnames: list of hostnames to interact with
    :type hostnames: list of strings
    """
    self.module_name = 'module.py'
    self.module_path = access_zipped_assets('twitter.common', 'deploy', 'deploy')
    self.hostnames = hostnames
    self._sudo_password = None

  def verify_and_log_results(self, results):
    """Echo the output of an ansible run

    There are two types of entries in the results- hosts that were 'contacted' and hosts that were
    'dark' (or unable to be connected to via ssh). 'dark' hosts are almost guaranteed to be bad, for
    any of several reasons. A host that was 'contacted' isn't guaranteed to be successful- it could
    have a bad rpm database, and not be able to install an RPM for instance, which means it's result
    will be False. This will raise RemoteExecutionError.

    :param results: Output from an ansible Runner command against hosts
    :type results: dictionary
    :rtype: list of strings containing message output
    """
    messages = []
    failures = []
    for hostname, result in results.get("contacted").items():
      success = result.get("success") or "unknown"
      message = '%s' % result.get("msg") or "unknown"
      messages.append(message)
      log.debug(message)
      if success is not True:
        failures.append(hostname)
        log.error('%s had a failure:\n%s' % (hostname, message))
      log.debug("%s" % result)

    for hostname, result in results.get("dark").items():
      failures.append(hostname)
      message = '%s\t%s' % (hostname, result.get("msg") or "unknown")
      messages.append(message)
      log.error(message)

    if len(failures) > 0:
      log.error("Detected %s hosts with errors!" % len(failures))
      raise self.RemoteExecutionError('Errors running on: %s' % failures)
    return messages

  @property
  def sudo_password(self):
    if not self._sudo_password:
      self._sudo_password = getpass.getpass('Enter sudo password: ')
    return self._sudo_password

  def run_module(self, module_args, sudo=False):
    """Using ansible, scp the scheduler module over to the host and execute it with arguments.

    :param module_args: Configuration passed to Module that is executed on the remote host
    :type module_args: dictionary
    :rtype: list of strings containing the message returned from the commands on each host
    """
    log.debug("Running %s on: %s" % (module_args, self.hostnames))
    user = 'aurora'
    sudo_pass = None
    #TODO(jsmith): Re-try if password auth issue...
    if sudo:
      user = getpass.getuser()
      sudo_pass = self.sudo_password
    runner = Runner(
        forks=1,
        module_name=self.module_name,
        module_args=module_args,
        module_path=self.module_path,
        pattern='*',
        remote_user=user,
        sudo=sudo,
        sudo_pass=sudo_pass,
        host_list=self.hostnames)
    results = runner.run()
    log.debug("Results: %s" % results)
    # Raises RemoteExecutionError
    return self.verify_and_log_results(results)

  def command(self):
    raise NotImplementedError('Each subclass must implement at least one command to be executed.')

    return self.run_module(dict(key_to_fill=True))