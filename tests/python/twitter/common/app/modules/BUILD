python_test_suite(name = 'modules',
  dependencies = [
    pants(':test_serverset'),
  ],
)

python_tests(name = 'test_serverset',
  sources = ['test_serverset.py'],
  dependencies = [
    pants('src/python/twitter/common/app/modules:serverset'),
    pants('3rdparty/python:kazoo'),
    pants('3rdparty/python:mock'),
  ]
)
