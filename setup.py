from setuptools import setup

setup(
    name='kucoin',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        kuku=main:main
    ''',
)

