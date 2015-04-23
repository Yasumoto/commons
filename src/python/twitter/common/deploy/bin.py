from twitter.common import app
from twitter.common.deploy import command
from twitter.common.log.options import LogOptions


app.register_commands_from(command)


def main()
  """It is critical that the actual `python_binary` is as small as possible.

  Ideally there would be no code which is not under test, but until `pants` supports testing of
  `python_binary` targets, it is reasonable to split out all of the code into separate modules to
  ensure full unit-test coverage of the deployment tooling.
  """
  app.help()


LogOptions.set_stderr_log_level('google:INFO')
LogOptions.disable_disk_logging()
app.set_name('deploy')


def proxy_main():
  """
  Ideally there is a `proxy_main` which serves as the entry point for the PEX and delegates out
  to `twitter.common.app`.
  """

  app.main()