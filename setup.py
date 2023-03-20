from setuptools import find_packages, setup

setup(
    name='clapp',
    packages=find_packages(include=['clapp']),
    version='0.1.0',
    description='A simple command line argument parser',
    author='Matthieu Legrand (legmatt0@gmail.com)',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)