# ==================================================================================================
# Copyright 2014 Twitter, Inc.
# --------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==================================================================================================

import threading
import time
import unittest

from twitter.common.zookeeper.client import TwitterClient
from twitter.common.zookeeper.test_server import ZookeeperServer

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
import mock


MAX_EVENT_WAIT_SECS = 30.0


class TwitterClientTest(unittest.TestCase):
  @mock.patch('threading._Event.wait', spec=threading._Event.wait)
  @mock.patch('kazoo.client.KazooClient.start_async', spec=KazooClient.start_async)
  def test_make(self, mock_start_async, mock_wait):
    zk = TwitterClient.make('localhost:1231')
    assert isinstance(zk, TwitterClient)
    mock_start_async.assert_called_once_with()
    mock_wait.assert_called_once_with()

  @mock.patch('kazoo.client.KazooClient.start', spec=KazooClient.start)
  def test_make_sync(self, mock_start):
    zk = TwitterClient.make('localhost:1231', async=False)
    assert isinstance(zk, TwitterClient)
    mock_start.assert_called_once_with()

  def test_observable_listener(self):
    """Ensure metrics are being incremented."""

    session_expirations = 'session_expirations'
    connection_losses = 'connection_losses'

    zk = TwitterClient('localhost:9001')
    assert zk.metrics.sample()[session_expirations] == 0
    assert zk.metrics.sample()[connection_losses] == 0

    zk._observable_listener(KazooState.LOST)
    assert zk.metrics.sample()[session_expirations] == 1
    assert zk.metrics.sample()[connection_losses] == 0

    zk._observable_listener(KazooState.SUSPENDED)
    assert zk.metrics.sample()[session_expirations] == 1
    assert zk.metrics.sample()[connection_losses] == 1

    zk._observable_listener(KazooState.LOST)
    assert zk.metrics.sample()[session_expirations] == 2
    assert zk.metrics.sample()[connection_losses] == 1

  def test_metrics(self):
    return True
    with ZookeeperServer() as server:
      event = threading.Event()
      def state_change(state):
        event.set()
        return True

      zk = TwitterClient('localhost:%d' % server.zookeeper_port)
      zk.start()
      zk.live.wait(timeout=MAX_EVENT_WAIT_SECS)
      zk.add_listener(state_change)
      sample = zk.metrics.sample()
      assert sample['session_id'] == zk._session_id
      assert sample['session_expirations'] == 0
      assert sample['connection_losses'] == 0
      old_session_id = zk._session_id

      server.expire(zk._session_id)
      event.wait(timeout=MAX_EVENT_WAIT_SECS)

      zk.live.wait(timeout=MAX_EVENT_WAIT_SECS)

      sample = zk.metrics.sample()
      assert sample['session_id'] == zk._session_id
      assert old_session_id != zk._session_id
      assert sample['session_expirations'] == 1
      assert sample['connection_losses'] > 0
