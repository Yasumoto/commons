#!/usr/bin/env python2.7

import socket

from twitter.common.lang import AbstractClass

from ansible.module_utils.basic import *


class Module(AbstractClass):
  """The python code to be run on each host
  """
    def __init__(self, module):
    """Read through the given module parameters to customize actions

    :params module: The ansible module with specified flags
    :type module: AnsibleModule
    """
    self.module = module
    self.hostname = socket.gethostname()

    self.key_to_fill = module.params.get('key_to_fill')

  def execute(self):
    """Operate on the host at runtime depending upon module parameters."""
    raise NotImplementedError('Subclasses must implement execute')

    if self.key_to_fill = True:
      print("Execute a function here")


def main():
  """Setup when run on a host via the `class`ansible.runner.Runner"""
  module = AnsibleModule(argument_spec=dict(
      key_to_fill=dict(required=False, default=None),
  ))

  try:
    my_module = Module(module)
  except ValueError as e:
    return (False, "Could not create SchedulerModule: %s" % e)

  result, message = my_module.execute()
  my_module.module.exit_json(success=result, msg=message)


if __name__ == '__main__':
  main()