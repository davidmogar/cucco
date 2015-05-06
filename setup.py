#!/user/bin/env python

import re

from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('normalizr/__init__.py').read(),
    re.M).group(1)

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(name='normalizr',
      version=version,
      description='Python library for text normalization',
      long_description=long_description,
      author='David Moreno-Garcia',
      author_email='david.mogar@gmail.com',
      license='MIT',
      url='https://github.com/davidmogar/normalizr',
      download_url='https://github.com/davidmogar/normalizr/tarball/' + version,
      keywords=['normalize', 'text', 'manipulation'],
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ]
      )
