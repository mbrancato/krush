#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name='krush',
  version='0.1',
  description='Apply templated Kubernetes manifests',
  url='https://github.com/mbrancato/krush',
  author='Mike Brancato',
  keywords='template kubernetes deploy',
  packages=find_packages(),
  install_requires=[
      'jinja2',
      'docopt',
      'pyyaml'
    ],
  entry_points={  # Optional
      'console_scripts': [
          'krush=krush.krush:main',
    ],
  },
)
