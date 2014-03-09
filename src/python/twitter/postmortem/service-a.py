import time

from twitter.common import app, log
from twitter.common.app.modules.http import RootServer
from twitter.common.http import HttpServer
from twitter.common.log.options import LogOptions
from twitter.common.metrics import (
    AtomicGauge,
    Observable,
    RootMetrics)

app.configure('twitter.common.app.modules.http', enable=True)

class ServiceA(Observable):
  def __init__(self):
    self._incoming_requests = AtomicGauge('incoming_requests')
    self._service_b_queries = AtomicGauge('service_b_queries')
    self.metrics.register(self._incoming_requests)
    self.metrics.register(self._service_b_queries)

  @HttpServer.route("/gimmeh")
  @HttpServer.route("/gimmeh/:message")
  def gimmeh(self, message='yo'):
    self._incoming_requests.increment()
    return '%s' % message


@app.default_command
def launch_service():
  service_a = ServiceA()
  RootServer().mount_routes(service_a)
  RootMetrics().register_observable('service_a', service_a)

  try:
    time.sleep(2**20)
  except KeyboardInterrupt:
    log.info('Shutting down.')

LogOptions.set_disk_log_level('NONE')
LogOptions.set_stderr_log_level('google:INFO')
app.main()
