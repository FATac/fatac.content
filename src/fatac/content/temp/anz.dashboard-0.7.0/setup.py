from setuptools import setup, find_packages
import os

version = '0.7.0'

setup(name='anz.dashboard',
      version=version,
      description="Plone netvibes like dashboard implementation",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone anz dashboard',
      author='jiangdongjin',
      author_email='eastxing@gmail.com',
      url='http://plone.org/products/anz.dashboard/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['anz'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'feedparser',
          'python-cjson'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
