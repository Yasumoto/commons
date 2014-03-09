python_binary(
  name = 'service-a',
  source = 'service-a.py',
  dependencies = [
    pants('src/python/twitter/common/app'),
    pants('src/python/twitter/common/app/modules:http'),
    pants('src/python/twitter/common/app/modules:vars'),
    pants('src/python/twitter/common/http'),
    pants('src/python/twitter/common/log'),
    pants('src/python/twitter/common/metrics'),
  ],
)

python_binary(
  name = 'service-b',
  source = 'service-b.py',
  dependencies = [
    pants('src/python/twitter/common/app'),
    pants('src/python/twitter/common/app/modules:http'),
    pants('src/python/twitter/common/app/modules:vars'),
    pants('src/python/twitter/common/http'),
    pants('src/python/twitter/common/log'),
    pants('src/python/twitter/common/metrics'),
  ],
)
