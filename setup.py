from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='fatac.content',
      version=version,
      description="fatac.content",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='fatac content',
      author='Ferran Pons',
      author_email='ferran.pons.sanche@upcnet.es',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fatac'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.dexterity [grok]',
          'plone.app.relationfield',
          'plone.namedfile [blobs]',
          'five.grok',
      ],
      extras_require={},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
