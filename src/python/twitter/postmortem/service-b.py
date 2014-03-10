import time
import urllib2

from twitter.common import app, log
from twitter.common.app.modules.http import RootServer
from twitter.common.http import HttpServer, request
from twitter.common.log.options import LogOptions
from twitter.common.metrics import (
    AtomicGauge,
    Observable,
    RootMetrics)

app.configure('twitter.common.app.modules.http', enable=True)

SERVICE_C_PATH = 'localhost:8890'

class ServiceB(Observable):
  def __init__(self):
    self._incoming_requests = AtomicGauge('incoming_requests')
    self._service_c_writes = AtomicGauge('service_c_writes')
    self._service_c_reads = AtomicGauge('service_c_reads')
    self._service_c_errors = AtomicGauge('service_c_errors')
    self.metrics.register(self._incoming_requests)
    self.metrics.register(self._service_c_writes)
    self.metrics.register(self._service_c_reads)
    self.metrics.register(self._service_c_errors)

  def read_messages(self):
    self._service_c_reads.increment()
    request = urllib2.Request('http://%s/read' % SERVICE_C_PATH)
    try:
      return urllib2.urlopen(request)
    except urllib2.URLError as e:
      self._service_c_errors.increment()
      log.error("Could not read messages from %s: %s" %
          (SERVICE_C_PATH, e))
      return None

  def write_message(self, message):
    self._service_c_writes.increment()
    request = urllib2.Request('http://%s/write' % SERVICE_C_PATH)
    try:
      urllib2.urlopen(request, message)
    except urllib2.URLError as e:
      self._service_c_errors.increment()
      log.error("Could not write message: %s to %s: %s" %
          (message, SERVICE_C_PATH, e))
      return False
    return True

  @HttpServer.route("/data")
  @HttpServer.route("/data", method='POST')
  def gimmeh(self):
    message = request.body.getvalue()
    self._incoming_requests.increment()
    self.write_message(message)
    return self.read_messages()


@app.default_command
def launch_service():
  service_b = ServiceB()
  RootServer().mount_routes(service_b)
  RootMetrics().register_observable('service_b', service_b)

  try:
    time.sleep(2**20)
  except KeyboardInterrupt:
    log.info('Shutting down.')

LogOptions.set_disk_log_level('NONE')
LogOptions.set_stderr_log_level('google:INFO')
app.main()
