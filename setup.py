#!/user/bin/env python

import re

from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('cucco/__init__.py').read(),
    re.M).group(1)

setup(name='cucco',
      version=version,
      description='Python library for text normalization',
      author='David Moreno-Garcia',
      author_email='david.mogar@gmail.com',
      license='MIT',
      url='https://github.com/davidmogar/cucco',
      download_url='https://github.com/davidmogar/cucco/tarball/' + version,
      keywords=['normalization', 'language', 'text', 'manipulation'],
      packages=find_packages(exclude=['tests']),
      entry_points={
          'console_scripts': [
              'cucco=cucco.cli:cli'
          ]
      },
      include_package_data=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Topic :: Software Development :: Libraries',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ]
)
