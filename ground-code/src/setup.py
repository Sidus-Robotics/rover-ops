from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.10"',
    ],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='src',  # '.' by default
        include=['mypackage*'],  # ['*'] by default
        exclude=['mypackage.tests'],  # empty by default
    ),
    entry_points={
        'console_scripts': [
            'cli-name = mypkg.mymodule:some_func',
        ]
    }
)