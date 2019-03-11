from setuptools import setup

setup(
    name='Replay',
    version='1.0',
    py_modules=['replay', 'click_datetime', 'click_flexpath', 'helper_lib', 'test_replay', 'test_helper_lib'],
    install_requires=[
        'Click',
        'jsonlines',
        'functools32',
        'requests'
    ],
    entry_points='''
      [console_scripts]
      replay=replay:cli
    '''
)