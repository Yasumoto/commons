from twitter.common import app


@app.command
def deploy(args, options):
  """A command to deploy a set of components to a cluster.

  A command-line tool should do its own option parsing within a command module, which will enable
  reusability as well as testable code without requiring fully executable commands. Most of the code
  within this function should deal with input validation and then delegate to a `deploy_api` module.

  Typically if you have multiple components, there will be a separate `commands` module which
  contains a separate submodule per component that needs to be deployed. For Apache Aurora, this
  means there is a `scheduler.py` which is used to deploy the Aurora Scheduler itself, along with a
  separate module for deploying the `aurora-client`, and a separate module for deploying the various
  cluster-wide components such as the `thermos-executor` and `thermos-observer`.

  :param args: list of arguments given to the command
  :type args: list of strings
  :param options: the optional flags passed into the command- each command should add as many
      options as needed
  :type options: optparse Options
  :rtype: 0 if success, otherwise Unix-y return value
  """