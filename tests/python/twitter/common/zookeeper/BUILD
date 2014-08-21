python_test_suite(
  name = 'all',
  dependencies = [
    pants(':client'),
    pants('tests/python/twitter/common/zookeeper/group'),
    pants('tests/python/twitter/common/zookeeper/serverset:all'),
  ],
)

python_tests(
  name = 'client',
  dependencies = [
    pants('src/python/twitter/common/log'),
    pants('src/python/twitter/common/zookeeper:client'),
    pants('src/python/twitter/common/zookeeper:testing'),
    pants('3rdparty/python:kazoo'),
    pants('3rdparty/python:mock'),
  ],
  sources = ['client_test.py'],
  coverage = 'twitter.common.zookeeper.client'
)
