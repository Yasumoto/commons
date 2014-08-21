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

TEST_SERVER = ['test_server.py']

python_library(
  name = 'zookeeper',
  dependencies = [
    pants(':client'),
    pants('src/python/twitter/common/zookeeper/group'),
    pants('src/python/twitter/common/zookeeper/serverset'),
  ],
  provides = setup_py(
    name = 'twitter.common.zookeeper',
    version = commons_version(),
    description = "Implementations of Twitter's service discovery libraries on top of Kazoo.",
  )
)

python_library(
  name = 'client',
  sources = ['client.py'],
  dependencies = [
    pants('3rdparty/python:kazoo'),
    pants('src/python/twitter/common/metrics'),
  ]
)

python_library(
  name = 'testing',
  sources = TEST_SERVER,
  dependencies = [
    pants('src/python/twitter/common/contextutil'),
    pants('src/python/twitter/common/dirutil'),
    pants('src/python/twitter/common/rpc/finagle'),
    pants('src/thrift/com/twitter/common/zookeeper/testing/angrybird:py-thrift')
  ]
)
