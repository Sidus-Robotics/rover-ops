from setuptools import setup, find_packages

setup(
    name='ground-code',
    version='0.0.1',
    install_requires=[
        'pygame',
        'websockets',
    ],
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'ground-station = ground_station.controller:main',
        ],
        'console_scripts': [
            'ground-station = ground_station.controller:main',
        ]
    }
)