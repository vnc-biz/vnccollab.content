# -*- coding: utf-8 -*-
"""
This module contains the tool of vnccollab.content
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = open('version.txt').readline().strip()

setup(name='vnccollab.content',
      version=version,
      description="VNC Collaboration Content Types",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          'Framework :: Plone',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      keywords='plone content type archetypes vnc',
      author='Vitaliy Podoba',
      author_email='vitaliy.podoba@vnc.biz',
      url='https://github.com/vnc-biz/vnccollab.content',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vnccollab', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.grok',
          'plone.api',
          'simplejson',
          'plone.app.jquery==1.7.2',
          'raptus.autocompletewidget',
          'collective.customizablePersonalizeForm',
      ],
      extras_require={'test': ['plone.app.testing']},
      )
