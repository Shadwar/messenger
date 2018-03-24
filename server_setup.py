from setuptools import find_packages
from cx_Freeze import setup, Executable

setup(
        name='MessengerServer',
        packages=find_packages(),
        executables=[Executable('run_server.py')]
)
