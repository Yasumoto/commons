python_library(
  name = 'group_base',
  sources = ['group_base.py'],
  dependencies = [
    pants('src/python/twitter/common/concurrent'),
    pants('src/python/twitter/common/lang'),
  ]
)

python_library(
  name = 'group',
  sources = ['group.py'],
  dependencies = [
    pants(':group_base'),
    pants('src/python/twitter/common/concurrent'),
    pants('src/python/twitter/common/zookeeper:client'),
  ]
)

python_binary(
  name = 'kazoo_cli',
  source = 'kazoo_cli.py',
  dependencies = [
    pants('src/python/twitter/common/app'),
    pants(':group'),
  ]
)
