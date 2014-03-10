import time
import urllib2

from twitter.common import app, log
from twitter.common.app.modules.http import RootServer
from twitter.common.http import HttpServer
from twitter.common.log.options import LogOptions
from twitter.common.metrics import (
    AtomicGauge,
    Observable,
    RootMetrics)

app.configure('twitter.common.app.modules.http', enable=True)

SERVICE_B_PATH = 'localhost:8889'

class ServiceA(Observable):
  def __init__(self):
    self._incoming_requests = AtomicGauge('incoming_requests')
    self._service_b_queries = AtomicGauge('service_b_queries')
    self._service_b_errors = AtomicGauge('service_b_errors')
    self.metrics.register(self._incoming_requests)
    self.metrics.register(self._service_b_queries)
    self.metrics.register(self._service_b_errors)

  def post_message_and_read(self, message):
    self._service_b_queries.increment()
    request = urllib2.Request('http://%s/data' % SERVICE_B_PATH)
    try:
      data = urllib2.urlopen(request, message)
      return data.read()
    except urllib2.URLError as e:
      self._service_b_errors.increment()
      log.error('Could not post %s to %s: %s' %
          (message, SERVICE_B_PATH, e))
      return None

  @HttpServer.route("/gimmeh")
  @HttpServer.route("/gimmeh/:message")
  def gimmeh(self, message='yo'):
    self._incoming_requests.increment()
    return self.post_message_and_read('%s' % message)


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
