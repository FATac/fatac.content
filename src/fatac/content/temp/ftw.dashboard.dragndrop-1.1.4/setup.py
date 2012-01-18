from setuptools import setup, find_packages
import os

version = open("ftw/dashboard/dragndrop/version.txt").read().strip()

setup(name='ftw.dashboard.dragndrop',
      version=version,
      description="ftw.dashboard.dragndrop is product wich add dragndrop functionality to the dashboard",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='philippe gross, 4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='http://plone.org/products/ftw.dashboard.dragndrop/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.dashboard'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
