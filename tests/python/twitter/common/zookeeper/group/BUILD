python_test_suite(
  name = 'group',
  dependencies = [
    pants(':test_group'),
  ],
)

python_library(
  name = 'test_base',
  sources = ['test_base.py'],
  dependencies = [
    pants('src/python/twitter/common/zookeeper:testing'),
  ]
)

python_library(
  name = 'test_group_lib',
  sources = ['test_group.py'],
  dependencies = [
    pants(':test_base'),
    pants('src/python/twitter/common/zookeeper:testing'),
  ]
)
python_tests(
  name = 'test_group',
  sources = ['test_active_group.py', 'test_group.py'],
  dependencies = [
    pants('3rdparty/python:kazoo'),
    pants('3rdparty/python:mock'),
    pants(':test_group_lib'),
    pants('src/python/twitter/common/zookeeper/group'),
  ],
  coverage = 'twitter.common.zookeeper.group.group'
)
