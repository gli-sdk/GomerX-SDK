from setuptools import setup, find_packages
import os
import sys

if sys.version_info < (3, 6, 5):
    sys.exit('GomerX SDK requires Python 3.6.5 or later')

dir_path = os.path.abspath(os.path.dirname(__file__))


def fetch_version():
    with open(os.path.join(dir_path, 'src', 'gomerx', 'version.py')) as f:
        ns = {}
        exec(f.read(), ns)
        return ns


ver = fetch_version()['__version__']

setup(
    name='gomerx',
    version=ver,
    description='GomerX Python SDK',
    author='GLI Software Team',
    url='http://www.glitech.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        'gomerx': ['LICENSE.txt', 'README.md']
    },
    install_requires=[
        'numpy >= 1.18.1',
        'opencv-python >= 4.2.0'
    ]
)