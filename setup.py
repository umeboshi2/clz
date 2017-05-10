from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='clz',
      version=version,
      description="clz to file exchange",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Joseph Rawson',
      author_email='joseph.rawson.works@gmail.com',
      url='',
      license='UNLICENSED',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'beautifulsoup4',
          'lxml',
          'Mako',
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
