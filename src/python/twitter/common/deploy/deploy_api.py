from twitter.common.lang import AbstractClass

class DeployAPI(AbstractClass):
  """Each component which desires to have business logic must implement a `deploy` method.

  This enables functionality such as ordering of hosts, health checking, validation of success, and
  any other features that ensure a successful deployment.
  """

  def deploy():
    raise NotImplementedError("Subclassess must at least implement deploy")